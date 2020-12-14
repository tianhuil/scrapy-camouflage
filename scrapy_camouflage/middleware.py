from abc import ABC, abstractmethod

import logging
from scrapy.downloadermiddlewares.retry import RetryMiddleware

from .user_agent import random_user_agent

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

class CamouflageMiddleware(ABC):
  def __init__(self, settings):
    self.max_retry_times = settings.getint('CAMOUFLAGE_RETRY_TIMES')

  @classmethod
  def from_crawler(cls, crawler):
    return cls(crawler.settings)

  @abstractmethod
  def new_proxy(self):
    raise NotImplementedError

  @abstractmethod
  def is_block(self, request, response, spider):
    raise NotImplementedError

  def new_user_agent(self):  # pylint: disable=no-self-use
    return random_user_agent()

  def new_request(self, request, url=None):
    proxy = self.new_proxy()

    proxy_request = request.copy()
    proxy_request.meta['proxy'] = proxy
    # Set to None for HttpProxyMiddleware to parse credentials
    proxy_request.headers['Proxy-Authorization'] = None
    proxy_request.headers['User-Agent'] = self.new_user_agent()
    if url:
      return proxy_request.replace(url=url, dont_filter=True)

    return proxy_request.replace(dont_filter=True)

  def process_response(self, request, response, spider):
    if request.meta.get('dont_retry', False):
      return response

    if self.is_block(request, response, spider):
      logger.warning('Request to %s was blocked', request.url)
      # reset session but with original (prior to any redirect) url
      request = self.new_request(request, url=request.url)
      return self._retry(request, reason='blocked', spider=spider) or response

    return response

  def process_exception(self, request, exception, spider):
    if request.meta.get('dont_retry', False):
      return None

    if isinstance(exception, RetryMiddleware.EXCEPTIONS_TO_RETRY):
      logger.warning('Request to %s timed out', request.url)
      request = self.new_request(request, url=request.url)
      return self._retry(request, reason=repr(exception), spider=spider)
    return None

  def process_request(self, request, spider):  # pylint: disable=unused-argument
    # add proxy if no proxy already specified
    if 'proxy' not in request.meta:
      request = self.new_request(request)

  def _retry(self, request, reason, spider):
    retries = request.meta.get('retry_times', 0) + 1
    max_retry_times = request.meta.get('max_retry_times', self.max_retry_times)

    stats = spider.crawler.stats
    if retries <= max_retry_times:
      logger.debug(
        "Retrying %(request)s (failed %(retries)d/%(max_retry_times)d times): %(reason)s",
        {'request': request, 'retries': retries, 'reason': reason, 'max_retry_times': max_retry_times},
        extra={'spider': spider}
      )
      retry_req = request.copy()
      retry_req.meta['retry_times'] = retries
      retry_req.dont_filter = True

      stats.inc_value('camouflage_retry/count')
      stats.inc_value('camouflage_retry/reason_count/%s' % reason)
      return retry_req

    stats.inc_value('camouflage_retry/max_reached')
    logger.debug(
      "Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
      {'request': request, 'retries': retries, 'reason': reason},
      extra={'spider': spider}
    )
    return None
