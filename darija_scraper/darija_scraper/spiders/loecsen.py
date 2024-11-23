# import scrapy

# class LoecsenSpider(scrapy.Spider):
#     name = "loecsen"
#     allowed_domains = ["loecsen.com"]
#     start_urls = ["https://www.loecsen.com/en/vocabulary-arabic-moroccan#essentials"]

#     def parse(self, response):
#         # Find all rows containing English, Arabic, and Pronunciation
#         rows = response.xpath('//ul[@class="col3"]/li')
        
#         for row in rows:
#             # Extract English, Arabic (Moroccan), and Pronunciation
#             english = row.xpath('.//div[@class="column-1"]/text()').get()
#             arabic = row.xpath('.//div[@class="column-2"]/text()').get()
#             pronunciation = row.xpath('.//div[@class="column-3"]/text()').get()

#             # Yield the extracted data
#             yield {
#                 'English': english,
#                 'Arabic (Moroccan)': arabic,
#                 'Pronunciation': pronunciation,
#             }

import scrapy


class LoecsenSpider(scrapy.Spider):
    name = "loecsen"
    allowed_domains = ["loecsen.com"]
    start_urls = ["https://www.loecsen.com/en/vocabulary-arabic-moroccan"]

    def parse(self, response):
        # Scraper la liste des catégories
        categories = response.xpath('//ul/li[@class="collapsible"]/a')
        for category in categories:
            category_name = category.xpath('text()').get()
            category_link = category.xpath('@href').get()

            # Créer une URL complète pour chaque catégorie
            full_link = response.urljoin(category_link)

            # Passer à la fonction de parsing des mots dans la catégorie
            yield scrapy.Request(
                url=full_link,
                callback=self.parse_category,
                meta={'category': category_name}  # Passer le nom de la catégorie
            )

    def parse_category(self, response):
        # Récupérer le nom de la catégorie depuis les métadonnées
        category_name = response.meta['category']

        # Scraper les mots de la catégorie
        rows = response.xpath('//tr[@data-id]')
        for row in rows:
            english = row.xpath('./td[1]/text()').get().strip().replace("🔊 ", "")
            arabic = row.xpath('./td[2]/text()').get().strip().replace("🔊 ", "")
            pronunciation = row.xpath('./td[3]/i/text()').get()

            # Retourner les données extraites
            yield {
                'Category': category_name,
                'English': english,
                'Arabic (Moroccan)': arabic,
                'Pronunciation': pronunciation,
            }
