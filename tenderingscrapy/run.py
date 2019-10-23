# 对招投标网中政府采购中标货物价格列表进行数据获取保存到本地json文件
# 
# by LongFly
# 2019.10


from scrapy.cmdline import execute
import sys
import os
# 获取当前脚本路径
dirpath = os.path.dirname(os.path.abspath(__file__))
print(dirpath)
# 添加环境变量
sys.path.append(dirpath)
# 启动爬虫,第三个参数为爬虫name
execute(['scrapy','crawl','TenderingSpider'])
