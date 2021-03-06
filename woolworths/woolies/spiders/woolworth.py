import scrapy
from scrapy_splash import SplashRequest
#from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from woolies.items import WooliesItem
import urlparse as upar

"""
Crawlspider used to crawl woolworths. Splash is used as JS renderer. 
This is refered to as Spider 1, as this is what collects the urls. Spider 2, is what we use to 
the do the secondary scraping of images.
"""

#This is Spider 1
class Woolies(scrapy.Spider):
    name = "woolworths"
    start_urls = [] 
    allowed_domains = []

    """
    Function used to add the prodcuts onto start_urls (empty at the start)
    """
    def __init__(self):
        #Change path accordingly
        for line in open(r'woolworths_products_list.txt','r').readlines():
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
                endpoint = 'render.html',
                args = {'wait': 1,
                        'viewport':'1920x6000', 
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
                      },

                )
    """
    Parsing function, currently we are getting a list of url links to each prodcuts specific page. From there 
    we can scrape the images and info needed.
    """
    def parse(self, response):
        item = WooliesItem()
        links = response.css('.shelfProductTile-information a::attr(href)').extract() #note this gets the relative url, where as we want the absolute.
        item['link'] = links
        
        with open('woolworths_products_url_crawl.txt','a+') as f:
            for url in links:
                #Domain name is added on to make relative URL into absolute.
                f.write("https://www.woolworths.com.au" + url.strip() + "\n")
        
        next_page = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "_pagingNext", " " ))]/@href').extract_first()
        item['page'] = next_page
        try:
            next_page_abs = "https://www.woolworths.com.au" + next_page
        except:
            pass
        
        if next_page is not None:
            yield SplashRequest(next_page_abs, self.parse,
                endpoint = 'render.html',
                args = {'wait': 1,
                        'viewport':'1920x1080', 
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
                      },

                ) 
        
        yield item


"""
This is Spider 2. This spider is what scrapes the websites for the product info.
"""
class ProductSpider(scrapy.Spider):
    name = "prod_wool"
    start_urls = [] #URL link for the all the products.

    """
    Function used to add the prodcuts onto start_urls (empty at the start)
    """
    def __init__(self):
        for line in open(r'woolworths_products_url_crawl.txt','r').readlines():
            self.start_urls.append(line.strip())
        super(ProductSpider, self).__init__()


    def start_requests(self):
        for products_url in self.start_urls:
            yield SplashRequest(products_url, self.parse_products,
                endpoint = 'render.html',
                args = {'wait': 0.5,
                        'viewport':'1366x768', 
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36' 
                },

                )

    """
    Important: We will use csv to store the info for each image.
    """
    def parse_products(self,response):
        """
        This is the parseer for the products, we fill the 3 main item field, [name], [desc]ription and [img]. They will be outputted in the CSV format.
        """
        #Name extractor:
        item = WooliesItem()
        for name in response.css('.heading3::text').extract():
            item['name'] = name.strip()

        #Image url Extractor:
        item['image_urls'] = []
        for each_url in response.css('img').xpath('@src').extract():
            if each_url.__contains__("large"):
                item['image_urls'].append(each_url)

        #Description extrator:        
        description= []
        extracted_desc = response.css('.productDetail-detailsSection p::text').extract()            
        for descr in extracted_desc:
            description.append(descr.strip())
            item['desc'] = ' '.join(description)     
        if extracted_desc is None:
            item['desc'] = "Empty Description"

        yield item
        
"""
class kmart(scrapy.Spider):
    name = "kmart"
    allowed_domains = []
    start_urls = []
    #http://www.kmart.com/sweet-baby-ray-s-barbecue-sauce-award-winning-18/p-08731693000P?plpSellerId=Kmart&prdNo=29&blockNo=29&blockType=G29#
    """
    Function used to add the prodcuts onto start_urls (empty at the start)
    """
    def __init__(self):
        for line in open(r'kamrt_products_url_crawl.txt','r').readlines():
            self.start_urls.append(line.strip())
        super(ProductSpider, self).__init__()

    def start_requests(self):
        for products_url in self.start_urls:
            yield SplashRequest(products_url, self.parse_kmart_products,
                endpoint = 'render.html',
                args = {'wait': 0.5,
                        'viewport':'1366x768', 
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36' 
                },

                )

    def parse_kmart_products(self, response):
        item = WooliesItem()
        #image links of the images
        item['image_urls'] = response.css("#overview a::attr(href)").extract()

        #Name of the product.
        item['name'] = response.css(".title-2 ::text").extract()

        #Description of the product.
        descr = []
        description = response.css("#description p::text").extract()
        for desc in description:
            descr.append(desc.strip())
            item['']
















"""
################# To run Scrapy from script, rather that from CLI #########################
"""
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(ProductSpider)
process.crawl(Woolies)
process.start() # the script will block here until all crawling jobs are finished
"""
"""
Splash LUA script:
function main(splash, args)
  splash.private_mode_enabled = false
  splash:set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
  splash:set_viewport_size(1920,5000)
  assert(splash:go(args.url))
  assert(splash:wait(1))
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end
"""