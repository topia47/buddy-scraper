# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WooliesItem(scrapy.Item):
    page = scrapy.Field() #placeholder item
    link = scrapy.Field() #placeholder item
    image_urls = scrapy.Field() #Item used to store the image URL's
    image_paths = scrapy.Field() #used in the pipeline, to save the paths of the downloaded images.
    name = scrapy.Field() #Name of the product currently being scraped.
    desc = scrapy.Field() #Description of the current image.
    pass
