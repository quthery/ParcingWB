import requests
import re
import csv

from models import Items


class ParseWB:
    def __init__(self, url):
        self.brand_id = self.__get_brand_id(url)

    @staticmethod
    def __get_brand_id(url:str):
        regex = "(brands).+"
        brand_id = re.search(regex, url)[0]
        return brand_id

    def parse(self):
        i = 1
        self.__create_csv()
        while True:
            response = requests.get(
                f'https://catalog.wb.ru/brands/m/catalog?appType=1&brand=27445&curr=rub&dest=-1257786&page={i}&regions=80,38,4,64,83,33,68,70,69,30,86,75,40,1,66,110,22,31,48,71,114&sort=popular&spp=0&xsubject=3274',
            )
            i += 1
            items_info = Items.parse_obj(response.json()["data"])
            if not items_info.products:
                break
            self.__save_csv(items_info)

    def __create_csv(self):
        with open("wb_data.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'название', 'цена', 'бренд', 'продаж', 'рейтинг', 'В наличии'])

    def __save_csv(self, items):
        with open("wb_data.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for product in items.products:
                writer.writerow([product.id,
                                 product.name,
                                 product.salePriceU,
                                 product.brand,
                                 product.sale,
                                 product.volume])


if __name__ == "__main__":
    url = 'https://www.wildberries.ru/brands/msi'
    parser = ParseWB(url)
    parser.parse()