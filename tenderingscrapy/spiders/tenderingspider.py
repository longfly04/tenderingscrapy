import scrapy
import copy
from tenderingscrapy.util import *
from tenderingscrapy.items import *

class TenderingSpider(scrapy.Spider):
	"""
	对招投标网中标信息进行爬取
	"""
	name = "TenderingSpider"
	allowed_domains = ["https://ggzy.qingdao.gov.cn"]
	start_urls = [
				  "https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/1-1-2?ProjectName=" + KEYWORD + "&ArryCode=&Time=&ClassId=&ZBFlag="
				 ]
	def parse(self, response):
		# 解析索引页
		print('-----------Response Status------------')
		if response.status == 200:
			print("索引页正常返回...") 
		else:
			print("索引页出现故障")
		
		pages = response.xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[2]/div/table//a')
		total_links = response.xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[3]/div/span/text()').get()
		title = response.xpath('/html/body/div[2]/div/div/div[1]/a[3]/text()').get()
		total_links = int(total_links[4:])
		next_page = response.xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[3]/div//a[text()="下一页"]/@href').extract_first()
		print('-----------Search Result------------')
		print('在 %s 中关于关键字 \"%s\" 共找到 %d 个结果。' %(title, KEYWORD, total_links))

		for page in pages:
			"""
			处理索引页的索引名称和链接
			"""
			project_item = ProjectItem()
			project_item['project_site'] = page.xpath('./@href').get()
			project_item['project_name'] = page.xpath('./@title').get()
			project_item['project_keyword'] = KEYWORD

			# 对详情页发起请求
			detail_href = "https://ggzy.qingdao.gov.cn" + project_item['project_site']
			yield scrapy.Request(detail_href, callback=self.parse_detail, meta=project_item, dont_filter=True)

		if next_page:
			# 对下一页发起请求
			next_page_href = "https://ggzy.qingdao.gov.cn" + next_page
			yield scrapy.Request(next_page_href, callback=self.parse, dont_filter=True)

	def parse_detail(self, response):
		# 解析详情页
		project_item = response.meta
		print('-----------Response Status------------')
		if response.status == 200:
			print("详情页正常返回...") 
		else:
			print("详情页出现故障")

		goods_list = response.xpath('/html/body/div[2]/div/div/table/tr[1]/td/div/table/tr[11]/td/table//tr')
		project_price = response.xpath('/html/body/div[2]/div/div/table/tr[1]/td/div/table/tr[7]/td[4]/text()').get()
		project_id = response.xpath('/html/body/div[2]/div/div/table/tr[1]/td/div/table/tr[2]/td[2]/text()').get()
		project_item['project_price'] = int(project_price)
		project_item['project_id'] = project_id
		
		goods_item = GoodsItem()
		goods_item_list = []
		for row in goods_list:
			if row is not 'None':
				info_list = row.xpath('.//td')
				if len(info_list) == 6:
					# 名称	品牌	产地	规格要求	数量/单位	单价（元）/优惠率
					goods_item['goods_name'] = info_list[0].xpath('./text()').get()
					goods_item['goods_brand'] = info_list[1].xpath('./text()').get()
					goods_item['goods_origin'] = info_list[2].xpath('./text()').get()
					goods_item['goods_type'] = info_list[3].xpath('./text()').get()
					goods_item['goods_quantity'] = info_list[4].xpath('./text()').get()
					goods_item['goods_price'] = info_list[5].xpath('./text()').get()

					goods_item['goods_brand'] = goods_item['goods_brand'] if goods_item['goods_brand'] is None else goods_item['goods_brand'].strip()
					goods_item['goods_type'] = goods_item['goods_type'] if goods_item['goods_type'] is None else goods_item['goods_type'].strip()
					goods_item['goods_name'] = goods_item['goods_name'] if goods_item['goods_name'] is None else goods_item['goods_name'].strip()
					goods_item['goods_origin'] = goods_item['goods_origin'] if goods_item['goods_origin'] is None else goods_item['goods_origin'].strip()
					goods_item['goods_quantity'] = goods_item['goods_quantity'] if goods_item['goods_quantity'] is None else goods_item['goods_quantity'].strip()
					goods_item['goods_price'] = goods_item['goods_price'] if goods_item['goods_price'] is None else goods_item['goods_price'].strip()
				
					# 将item深拷贝到列表中，否则只拷贝引用
					goods_item_list.append(copy.deepcopy(dict(goods_item)))

		project_item['goods_list'] = copy.deepcopy(goods_item_list)
		yield project_item






