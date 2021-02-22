import scrapy
from scrapy_splash import SplashRequest

class SplashLivecoinSpider(scrapy.Spider):
    name = 'splash_livecoin'
    
    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            headers = {
                ['User_Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
            }
            splash:set_custom_headers(headers)
            splash.plugins_enabled = true
            splash.indexeddb_enabled = true
            splash:set_viewport_full()
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(5))
            return splash:html()
        end

    '''

    def start_requests(self):
        yield SplashRequest(url= "https://coinmarketcap.com/",
                            callback = self.parse,
                            endpoint="execute",
                            args = {'lua_source' : self.script})

    def parse(self, response):
        
        for currency in response.xpath("//tr"):
            if currency.xpath(".//div[@class = 'sc-16r8icm-0 sc-1teo54s-0 gKtDwz']/div/p/text()").get() is not None:
                yield {
                    'currency pair' : currency.xpath(".//div[@class = 'sc-16r8icm-0 sc-1teo54s-0 gKtDwz']/div/p/text()").get(),
                    'Price' : currency.xpath(".//div[contains(@class, 'price___3rj7O ')]/a/text()").get()
                }
        
        pass
