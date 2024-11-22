import scrapy


class LoecsenSpider(scrapy.Spider):
    name = "loecsen"
    allowed_domains = ["loecsen.com"]
    start_urls = ["https://www.loecsen.com/en/vocabulary-arabic-moroccan#essentials"]

    def parse(self, response):
        # Sélectionner toutes les lignes du tableau
        rows = response.xpath('//tr[@data-id]')

        for row in rows:
            # Extraire les colonnes
            english = row.xpath('./td[1]/text()').get().strip().replace("🔊 ", "")
            arabic = row.xpath('./td[2]/text()').get().strip().replace("🔊 ", "")
            pronunciation = row.xpath('./td[3]/i/text()').get()

            # Retourner les données extraites
            yield {
                'English': english,
                'Arabic (Moroccan)': arabic,
                'Pronunciation': pronunciation,
            }



