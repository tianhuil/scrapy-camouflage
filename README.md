# scrapy-camouflage
Updates proxy and user agent if website is blocking [scrapy](https://scrapy.org/) spider.

## Install
To install, run
```bash
pip install -e git@github.com:tianhuil/scrapy-camouflage.git@latest
```

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
The only requirement on the priority is that it be less than that of `HttpProxyMiddleware` (default priority 750).  However, it is recommended that the priority be higher than that of `RedirectMiddleware` (default priority 600) if HTTP redirects are used to test for a block.

## TODOs
- Allow use fake user agent
