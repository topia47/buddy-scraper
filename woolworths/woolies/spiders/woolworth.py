import scrapy
from scrapy_splash import SplashRequest
from scrapy.spiders import Rule, Crawlspider
from woolies.items import WooliesItems

"""
Crawlspider used to crawl woolworths. Splash is used as JS renderer. 
This is refered to as Spider 1, as this is what collects the urls. Spider 2, is what we use to 
the do the actual scraping.
"""

class Woolies(scrapy.spider):
    name = "woolworths"
    start_urls = [] #This would be a list of items we are searching for, eg milk, cookies.....

    """
    Function used to add the prodcuts onto start_urls (empty at the start)
    """
    def __init__(self):
        for line in open(r'C:\Users\Sanju Jacob\Documents\woolies\woolies\woolworths_products_list.txt','r').readlines():
            self.start_urls.append(line.strip())
        super(Woolies, self).__init__()

    """
    Requests being sent to the Splash Server. We set the arguments for the renderer, which in our case
    is 'render.html'. The function also has a callback to parse, which process' the info. Arg = veiwport:full
    should show the entire list of products. #Still to be tested.
    """
    def start_requests(self):
        for products in self.start_urls:
            yield SplashRequest(products, self.parse,
                endpoint = 'render.html'
                args = {'wait':0.5,
                        'viewport':full, 
                        'images':1,
                      },

                )

    """
    Parsing function, currently we are getting a list of url links to each prodcuts specific page. From there 
    we can scrape the images and info needed.
    """
    def parse(self,response):
        item = WooliesItems()
        item['link'] = response.css('.shelfProductTile-descriptionLink ::text').extract()

        yield item


"""
This is Spider 2. This spider is what scrapes the images for the 300x300 image of each product.
"""
class ProductSpider(scrapy.spider):

    name = "prod_spider"
    start_urls = [] #URL link for the all the products.

    """
    Function used to add the prodcuts onto start_urls (empty at the start)
    """
    def __init__(self):
        for line in open(r'C:\Users\Sanju Jacob\Documents\woolies\woolies\woolworths_products_url.txt','r').readlines():
            self.start_urls.append(line.strip())
        super(Woolies, self).__init__()


   def start_requests(self):
    for products_url in self.start_urls:
        yield SplashRequest(products_url, self.parse_products,
            endpoint = 'render.html'
            args = {},

            )

    """
    Important: We will use csv to store the info for each image.
    Will have to 2 colums, Column 1 = Description (Pauls Full Cream Milk 300ml)
    while Column 2 = Images (path/url) *For now we will stick to url, since its easier.

    """
    def parse_products(self,response):
        """
        This is the parseer for the products, we can further 'complicate' it by adding further site implmentation.
        """
        item = WooliesItems()
        item['name'] = response.css('.heading3').extract().strip()
        item['img'] = response.css('.productDetail-imageContainer a::attr(href)')
        yield item




################# To run Scrapy from script, rather that from CLI #########################
"""
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(ProductSpider)
process.crawl(Woolies)
process.start() # the script will block here until all crawling jobs are finished
"""