import datetime

import scrapy
from scrapy.exceptions import CloseSpider

from scrapy.loader import ItemLoader
import re

from ..items import DobrichkaItem


class DobrichkaSpider(scrapy.Spider):
	name = 'dobrichka'
	start_urls = ['http://dobrichka.bg/bg/news']
	last_year = 2011
	year = int(datetime.datetime.now().year)
	month = 1

	def parse(self, response):
		post_links = response.xpath('//div[@class="page-content"]/ul/li/a/@href')
		yield from response.follow_all(post_links, self.parse_post)

		pagination_links = f'http://dobrichka.bg/bg/news/{self.year}/{self.month}'
		self.month += 1
		if self.month == 13 and self.year == self.last_year:
			raise CloseSpider('no more pages')
		if self.month == 13:
			self.month = 1
			self.year -= 1

		yield response.follow(pagination_links, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		if not title:
			return
		description = response.xpath('//div[@class="page-text"]/descendant-or-self::*/text()').getall()
		description = [re.sub(' ', '', p).strip() for p in description[5:]]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="news-date"]/text()').get()
		print(date)

		item = ItemLoader(item=DobrichkaItem(), response=response)
		item.add_value('title', title.strip())
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
