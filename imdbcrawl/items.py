# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    Title = scrapy.Field()
    Year = scrapy.Field()
    Genre = scrapy.Field()
    Rating = scrapy.Field()
    Plot = scrapy.Field()
    Country_Code=scrapy.Field()
    Country_Name=scrapy.Field()
