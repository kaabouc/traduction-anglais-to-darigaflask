import scrapy

class GlosbeSpider(scrapy.Spider):
    name = "glosbe"
    allowed_domains = ["glosbe.com"]
    start_urls = [
        "https://glosbe.com/ary/en/"  # URL de base contenant des mots en Darija et en anglais
    ]

    def parse(self, response):
        # Scraper les mots depuis les sections de la page
        for row in response.xpath("//div[@class='phrase']"):
            yield {
                'english': row.xpath(".//div[@class='translation']/text()").get(),
                'darija': row.xpath(".//div[@class='source']/text()").get(),
            }

        # Pagination : aller à la page suivante
        next_page = response.xpath("//a[@class='next']/@href").get()
        if next_page:
            yield response.follow(next_page, self.parse)
