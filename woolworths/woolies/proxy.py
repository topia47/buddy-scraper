#!/usr/bin/python
#-*-coding:utf-8-*-

import random
import scrapy
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
"""
Used to cycle through the different Proxies in order to avoid TimoutErrors and to stop being kicked out
server.
"""

class RandomProxyMiddleware(HttpProxyMiddleware):
    def __init__(self, proxy_ip=''):
        self.proxy_ip = proxy_ip

    def process_request(self,request,spider):
        ip = random.choice(self.proxy_list)
        if ip:
            print ip
            request.meta['proxy']= ip

    #turns out only several ip works here, need to 
    #filter out the useless ones, via ping ?
    proxy_list = [  "http://206.109.4.94:8080"]
