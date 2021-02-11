import scrapy

from scrapy.loader import ItemLoader
from ..items import BancadelsudItem
from itemloaders.processors import TakeFirst


class BancadelsudSpider(scrapy.Spider):
	name = 'bancadelsud'
	start_urls = ['https://www.bancadelsud.com/it/eventi-e-comunicazioni/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="news-listing-block pull-left"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@title="Vai alla pagina successiva"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//div[@class="social-likes-label pull-left people-column"]//h3/text()').get()
		description = response.xpath('//div[@class="content-column pull-left"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="social-likes-label pull-left people-column"]//h4/text()').get()

		item = ItemLoader(item=BancadelsudItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
