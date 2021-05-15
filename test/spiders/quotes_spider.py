import scrapy
import csv

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://dmoztools.net/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'result-{page}.csv'

        rows = []
        full_category = response.css("aside").xpath('@class').getall()        
        for category in full_category:
            subcategory_names = response.xpath(f"//aside[@class={category!r}]//div//a/text()").getall()
            subcategory_url = response.xpath(f"//aside[@class={category!r}]//div//a").xpath('@href').getall()                                    
            enhanced_url = ['https://dmoztools.net' + url for url in subcategory_url]
            rows += [subcat + (category,) for subcat in list(zip(subcategory_names, enhanced_url))]         

        # schema = ["Website name", "Website URL", "Category"]
        # with open(filename, 'w', newline='') as f:
        #     writer = csv.writer(f, delimiter=',')
        #     writer.writerow(schema)
        #     for row in rows:
        #         writer.writerow(row)
        #     self.log(f'Saved file {filename}')