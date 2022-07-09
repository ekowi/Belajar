import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMovieSpider(CrawlSpider):
    name = 'best_movie'
    allowed_domains = ['web.archive.org']
    start_urls = ['http://web.archive.org/web/20200715000935if_/https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3[@class="lister-item-header"]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[1]"))
    )

    def parse_item(self, response):
        yield {
            'title' : response.xpath('//div[@class="title_wrapper"]/h1/text()').get(),
            'year': response.xpath('//span[@id="titleYear"]/a/text()').get(),
            'durations': response.xpath("normalize-space((//time)[1]/text())").get(),
            'genre': response.xpath('//div[@class="subtext"]/a[1]/text()').get(),
            'rating': response.xpath('//span[@itemprop="ratingValue"]/text()').get(),
            'movie_url' : response.url
        }
