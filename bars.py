# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib.parse import urljoin


def product_info(response, value):
    return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract_first()

class BarsSpider(scrapy.Spider):
    name = 'bars'
    allowed_domains = ['yelp.com']
    start_urls = ['http://www.yelp.com/search?find_desc=Tapas%2FSmall%20Plates&find_loc=Seattle%2C%20WA']

    def parse(self, response):
        listings = response.xpath('//*[@class="lemon--span__373c0__3997G text__373c0__26Xrb text-color--black-regular__373c0__B5jQ9 text-align--left__373c0__Rrl_f text-weight--bold__373c0__20M7i text-size--inherit__373c0__dzW7L"]/a/@href').extract()
        for listing in listings:
            print(listing)
            absolute_url = urljoin('http://www.yelp.com/',listing)
            yield Request(absolute_url, callback=self.parse_book)

        # process next page
        next_page_url = response.xpath('//*[@class="lemon--a__373c0__IEZFH link__373c0__2MnoO next-link navigation-button__373c0__23BAT link-color--inherit__373c0__23vKF link-size--inherit__373c0__cQmDm"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url)

    def parse_book(self, response):
        title = response.xpath('//*[@class="lemon--h1__373c0__2ZHSL heading--h1__373c0__1VUMO heading--no-spacing__373c0__1PzQP heading--inline__373c0__1F-Z6"]/text()').extract_first()
        rating = response.xpath('//*[@class="lemon--div__373c0__1mboc arrange__373c0__UHqhV gutter-6__373c0__zqA5A vertical-align-middle__373c0__2TQsQ u-space-b1 border-color--default__373c0__2oFDT"]/div/span/div/@aria-label').extract_first()
        rating = rating.replace('star rating', '')
        count = response.xpath('//*[@class="lemon--p__373c0__3Qnnj text__373c0__2pB8f text-color--mid__373c0__3G312 text-align--left__373c0__2pnx_ text-size--large__373c0__1568g"]/text()').extract_first()
        type = response.xpath('//*[@class="lemon--span__373c0__3997G text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_ text-size--large__373c0__1568g"]/a/text()').extract()

        yield {
            'title': title,
            'rating': rating,
            'count': count,
            'type': type
        }
