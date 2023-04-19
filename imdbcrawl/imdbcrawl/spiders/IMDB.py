# -*- coding: utf-8 -*-
import scrapy
from ..items import ImdbcrawlItem
from scrapy.selector import Selector

from scrapy.crawler import Crawler

class ImdbSpider(scrapy.Spider):
    name = 'IMDB'
    start_urls = ['https://www.imdb.com/search/title/']


    def parse(self, response):
        #select=scrapy.selector.Selector(response)

        ccode=response.css('select.countries option::attr(value)').extract()
        cname=response.css('select.countries option::text').extract()
        print(ccode.__len__(),'........',cname.__len__())
        # getting the country code and Name
        for (c,m) in zip(ccode,cname):
            #print(c,':',m)
            yield scrapy.Request(url='https://www.imdb.com/search/title/?countries='+c+'&adult=include&count=250',
                             callback=self.pdata,meta={'ccode':c,'cname':m})
    # scrapping movie details for each country.
    def pdata(self,response):
        #print(response.css('h3.lister-item-header a::text').extract())
        #select=Selector(response)
        domain = 'https://www.imdb.com'
        items = ImdbcrawlItem()
        ccode=response.meta['ccode']
        cname=response.meta['cname']
        all_Movies_List=response.css('div.lister-item-content')
        for Movies in all_Movies_List:
            Movie_Title=str(Movies.css('h3.lister-item-header a::text').extract_first()).strip()
            Movie_Year=str(Movies.css('span.lister-item-year.text-muted.unbold::text').extract_first()).strip('()')
            Movie_Genre=str(Movies.css('span.genre::text').extract_first()).strip()
            Movie_Rating=str(Movies.css('div.inline-block.ratings-imdb-rating::attr(data-value)').extract_first()).strip()
            Movie_Plot = str(Movies.css('.ratings-bar+ .text-muted::text').extract_first()).strip()
            #Movie_Director=str(Movies.css('p#text::text').extract_first()).strip()
            #Movie_Stars=str(Movies.css('div.inline-block.ratings-imdb-rating::attr(data-value)').extract_first()).strip()
            #print('Movie Name : ',Movie_Title,'Released on :',Movie_Year,'Genre :',Movie_Genre,'Rating :',Movie_Rating)
            # Items
            items['Title']=Movie_Title
            items['Year']=Movie_Year
            items['Genre']=Movie_Genre
            items['Rating']=Movie_Rating
            items['Plot']=Movie_Plot
            items['Country_Code']=str(ccode).upper()
            items['Country_Name']=str(cname).capitalize()
            yield items
            # scrapping available next page
        next_page= response.css('a.lister-page-next.next-page::attr(href)').get()
        print(next_page)
        if next_page is not None:
            full_page = domain + next_page
            yield response.follow(full_page,callback=self.pdata,meta={'ccode':ccode,'cname':cname})
        print(ccode,cname)
        #print(response.url)
        #yield response.follow()

