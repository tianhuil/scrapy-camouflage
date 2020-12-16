# scrapy-camouflage
Updates proxy and user agent if website is blocking [scrapy](https://scrapy.org/) spider.

## Install
To install, run
```bash
pip install https://github.com/tianhuil/scrapy-camouflage/archive/latest.tar.gz
```
or use a specific tag instead of `latest`.

## Use
Then create a subclass in `crawler/middlewares.py` and overwrite the `new_proxy` and `is_block` methods:
```py
class MyCamouflageMiddleware(CamouflageMiddleware):
    def new_proxy(self):
        return 'user{}:password@proxy.com'.format(randint(1000))

    def is_block(self, request, response, spider):
        return 'blocked' in response.text
```

You may optionally override the `new_user_agent` method
```py
    def new_user_agent(self):
        return 'Mozilla/5.0 (My Agent)'
```
The default is to use a hard-coded list of recent popular user agents.

Finally, add the following to `DOWNLOADER_MIDDLEWARES`:
```py
{
    DOWNLOADER_MIDDLEWARES = {
        'crawler.middlewares.MyCamouflageMiddleware': 610,
    }
}
```
The only requirement on the priority is that it be *lower* than that of `HttpProxyMiddleware` (default priority 750).  Optionally, the priority
- must be *higher* than that of `RedirectMiddleware` (default priority 600) if HTTP redirects are used to test for a block.
- must be *lower* than that of `HttpCompressionMiddleware` (default priority 590) if you want to use `response.text` (or even to correctly use `response.body`) to test for a block.  Use two middlewares if you want to test for both conditions.

## Configuration
You can configure the app by setting
```bash
CAMOUFLAGE_RETRY_TIMES=5
CAMOUFLAGE_DISABLE_PROXY=True  # for testing
```

## Dev
See the `Makefile` for dev dependencies and commands.  In particular `make pylint`.

## TODOs
- Allow use fake user agent (although some of their user agents belong to old browsers and are rejected by websites)
