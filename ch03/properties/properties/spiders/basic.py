import datetime
import urlparse
import socket
import scrapy

from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader

from properties.items import PropertiesItem


class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["localhost"]

    # Start on a property page
    start_urls = (
        'http://localhost:9312/properties/property_000000.html',
    )

    def parse(self, response):
        """ This function parses a property page.

        @url http://web:9312/properties/property_000000.html
        @returns items 1
        @scrapes title price description address image_urls
        @scrapes url project spider server date
        """
        
        """
        #1. First method
        item = PropertiesItem()
        item['title'] = response.xpath('//*[@itemprop="name"][1]/text()').extract()
        item['price'] = response.xpath('//*[@itemprop="price"][1]/text()').re('[.0-9]+')
        item['description'] = response.xpath('//*[@itemprop="description"][1]/text()').extract()
        item['address'] = response.xpath(
            '//*[@itemtype="http://schema.org/'
            'Place"][1]/text()').extract()
        item['image_urls'] = response.xpath('//*[@itemprop="image"][1]/@src').extract()
        return item
        """
        
        #2. Secode method
        l = ItemLoader(item=PropertiesItem(), response=response)
        
        l.add_xpath('title', '//*[@itemprop="name"][1]/text()')
        l.add_xpath('price', '//*[@itemprop="price"][1]/text()', re('[.0-9]+')
        l.add_xpath('description', '//*[@itemprop="description"][1]/text()')
        l.add_xpath('address', '//*[@itemtype="http://schema.org/Place"][1]/text()')
        l.add_xpath('image_urls', '//*[@itemprop="image"][1]/@src')
        
        return l.load_item()
        
        
        """
        # Create the loader using the response
        l = ItemLoader(item=PropertiesItem(), response=response)

        # Load fields using XPath expressions
        l.add_xpath('title', '//*[@itemprop="name"][1]/text()',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('price', './/*[@itemprop="price"][1]/text()',
                    MapCompose(lambda i: i.replace(',', ''), float),
                    re='[,.0-9]+')
        l.add_xpath('description', '//*[@itemprop="description"][1]/text()',
                    MapCompose(unicode.strip), Join())
        l.add_xpath('address',
                    '//*[@itemtype="http://schema.org/Place"][1]/text()',
                    MapCompose(unicode.strip))
        l.add_xpath('image_urls', '//*[@itemprop="image"][1]/@src',
                    MapCompose(lambda i: urlparse.urljoin(response.url, i)))

        # Housekeeping fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()
        """