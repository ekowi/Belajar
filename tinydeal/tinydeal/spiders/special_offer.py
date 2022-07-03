import scrapy


class SpecialOfferSpider(scrapy.Spider):
    name = 'special_offer'
    allowed_domains = ['www.web.archive.org']
    start_urls = ['https://web.archive.org/web/20190225123327/https://www.tinydeal.com/specials.html']

    def parse(self, response):
        for product in response.xpath("//ul[@class='productlisting-ul']/div/li"):
            yield {
                'tittle' : product.xpath(".//a[@class='p_box_title']/text()").get(),
                'url' : response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get()),
                'discount_price' : product.xpath(".//div[@class='p_box_price']/span[1]/text()").get(),
                'real_price': product.xpath(".//div[@class='p_box_price']/span[2]/text()").get()
            }

        next_page = response.xpath("//a[@class='nextPage']").get()

        if next_page:
            yield scrapy.Request(url= next_page, callback=self.parse)