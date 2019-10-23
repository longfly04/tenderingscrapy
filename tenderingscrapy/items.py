# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TenderingscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ProjectItem(scrapy.Item): 
    project_name = scrapy.Field() # 项目名称
    project_id = scrapy.Field() # 项目编号
    project_site = scrapy.Field() # 项目网址
    project_keyword = scrapy.Field() # 项目搜索关键字
    project_price = scrapy.Field()  # 项目总价格
    project_goods = scrapy.Field()  # 项目成交列表

class GoodsItem(ProjectItem):
    goods_name = scrapy.Field() # 商品名称
    goods_brand = scrapy.Field() # 商品品牌
    goods_origin = scrapy.Field() # 商品产地
    goods_type = scrapy.Field() # 商品规格
    goods_quantity = scrapy.Field() # 商品数量/单位
    goods_price = scrapy.Field() # 商品单价/优惠率
