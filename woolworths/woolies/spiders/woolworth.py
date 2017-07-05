import scrapy
from scrapy_splash import SplashRequest
from scrapy.spiders import Rule, Crawlspider
from woolies.items import WooliesItems

"""
Crawlspider used to crawl woolworths. Splash is used as JS renderer.
"""

class Woolies(scrapy.spider):
    name = "woolworths"
    start_urls = [] #This would be a list of items we are searching for, eg milk, cookies.....

    def __init__(self):
        for line in open(r'C:\Users\Sanju Jacob\Documents\woolies\woolies\woolworths_products_list.txt','r').readlines():
            self.start_urls.append(line.strip())
        super(Woolies, self).__init__()


    def start_requests(self):
        for products in self.start_url:
            yield SplashRequest(products, self.parse,
                endpoint = 'render.html'
                args = {'wait':0.5,
                        'viewport':full,
                        'images':1,
                      },

                )
    def parse(self,response):
        item = WooliesItems()
        item['link'] = response.css('.shelfProductTile-descriptionLink ::text').extract()

        yield item



        
"""
 sudo ./provision.sh prepare_install install_msfonts install_extra_fonts install_deps install_flash install_qtwebkit_deps install_official_qt install_qtwebkit install_pyqt5 install_python_deps
"""