import requests
from bs4 import BeautifulSoup

from django.core.management import BaseCommand

from products.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        url = 'https://www.citilink.ru/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        img_src_attrs_name = ["src", "data-src"]  # Возможные названия атрибутов которые хранят путь к картинке

        for c in soup.find_all('div', class_='CatalogMenu__category-items js--CatalogMenu__category-items'):
            try:
                name = c.find("a")['data-title']
                href = c.find("a")['href']

                category = Category.objects.create(
                    title=name,
                    href=href
                )
                category.save()
                parsing_children_category(href, category)

            except:
                pass


def parsing_children_category(href, parent):
    url = href
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    for c in soup.find_all('div', class_='CatalogCategoryCardWrapper__item-flex'):
        try:
            name = c.find("a").get_text()
            href = c.find("a")['href']

            category = Category.objects.create(
                title=name,
                href=href,
                parent=parent
            )
            category.save()
            parsing_children_category(href, category)

        except:
            pass