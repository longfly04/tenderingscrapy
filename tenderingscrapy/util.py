import scrapy
import time
# 配置常量、关键字、工具

KEYWORD = '监控'

def get_now():
    curdate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    return curdate