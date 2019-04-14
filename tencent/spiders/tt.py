# -*- coding: utf-8 -*-
import scrapy
import urllib.parse


# from tencent.items import TencentItem


class TtSpider(scrapy.Spider):
	name = 'tt'
	allowed_domains = ['hr.tencent.com']
	start_urls = ['https://hr.tencent.com/position.php?&start=#a0']

	def parse(self, response):
		# 1.提取当前页面的数据
		# 先分组，在提取
		tr_list = response.xpath("//table[@class='tablelist']/tr")[1:-1]
		for tr in tr_list:
			# item = TencentItem()
			item = {}
			item["position_name"] = tr.xpath("./td[1]/a/text()").extract_first()
			item["position_href"] = tr.xpath("./td[1]/a/@href").extract_first()
			item["position_cate"] = tr.xpath("./td[2]/text()").extract_first()
			item["need_num"] = tr.xpath("./td[3]/text()").extract_first()
			item["location"] = tr.xpath("./td[4]/text()").extract_first()
			item["publish_date"] = tr.xpath("./td[5]/text()").extract_first()
			yield item

		# 2. 翻页，请求下一页
		next_url = response.xpath("//a[@id='next']/@href").extract_first()
		print(next_url)
		if next_url != "javascript:;":  # 判断是不是下一页
			# next_url = "https://hr.tencent.com/" + next_url
			# 通过urllib.parse.urljoin()进行url地址的拼接
			# next_url = urllib.parse.urljoin(response.url,next_u rl)
			# yield scrapy.Request(  #构造requests对象，通过yield叫个引擎
			#     next_url,
			#     callback=self.parse
			# )
			# 根据repsponse的url地址，对next_url进行url地址的拼接，构造请求
			yield response.follow(next_url, callback=self.parse)

	# 假设构造详情页的请求
