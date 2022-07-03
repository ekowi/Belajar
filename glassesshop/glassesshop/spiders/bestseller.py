import scrapy


class BestsellerSpider(scrapy.Spider):
    name = 'bestseller'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['http://www.glassesshop.com/bestsellers']

    def parse(self, response):
        for product in response.xpath("//div[@id='product-lists']/div[@class='col-12 pb-5 mb-lg-3 col-lg-4 product-list-row text-center product-list-item']"):
            yield {
                "url" : product.xpath(".//div[@class='product-img-outer']/a[1]/@href").get(),
                "image_link" : product.xpath(".//div[@class='product-img-outer']/a[1]/img[1]/@data-src").get(),
                "product_name" : product.xpath(".//div[@class='p-title-block']/div[2]/div/div[1]/div/a/text()").get().strip(),
                "product_price" : product.xpath(".//div[@class='p-title-block']/div[2]/div/div[2]/div/div[1]/span/text()").get()
            }

        next_page = response.xpath("//main[@class='glasses-main']/div[3]/div[@class='container']/div/div/ul/li[6]").get()

        if next_page:
            yield scrapy.Request(url= next_page, callback= self.parse)


