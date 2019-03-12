# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field 


class SilmspiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # Instore category, article and url
    huiji_categories = Field()
    huiji_articles = Field()
    huiji_url = Field()
