import scrapy
from re import sub
from decimal import Decimal

# command to run this spider: runspider my_spider.py -o olx-apartamentos.json

class BomNegocioSpider(scrapy.Spider):
    name = 'bomNegocioSpider'
    start_urls = ['http://pb.bomnegocio.com/paraiba/joao-pessoa/imoveis/venda/apartamentos?sd=4806&sd=4838&sd=4811&sd=4837&sd=4803&sd=4820&sd=4817&sd=4819&sd=4821&sd=4839&sd=4841']

    def parse(self, response):
        for href in response.css('.adBN a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_post)

    def parse_post(self, response):
        yield {
	    'id': int(response.xpath('//div[@class="OLXad-id"]/p/strong/text()').extract()[0]),
            'tamanho': int(sub(r'[^\d]', '', response.css('.description').extract()[1])),
            'preco': int(sub(r'[^\d]', '', response.xpath('//span[@class="actual-price"]/text()').extract()[0])),
	    'bairro': response.xpath('//div[contains(@class, "OLXad-location")]//ul/li[3]/p/strong/text()').extract()[0].strip(),
            'link': response.url
        }
