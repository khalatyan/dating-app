import requests
from bs4 import BeautifulSoup

from django.core.management import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from products.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = Category.objects.all()

        for category in categories:
            children_category = Category.objects.filter(parent=category).first()
            if not children_category:
                parsing_products(category.href, category)


def parsing_products(href, category):
    url = href
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    next_page = soup.find('a', class_='PaginationWidget__arrow_right')
    for c in soup.find_all('div',
                           class_='product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing js--ProductCardInWishlist'):
        title = c.find('a', class_='ProductCardHorizontal__title').get_text()
        try:
            cost = c.find('span', class_='ProductCardHorizontal__price_current-price').contents[0].strip().replace(' ', '')
        except:
            cost = 0
        image_url = c.find('img', class_='ProductCardHorizontal__image')['src']
        image = get_image(image_url)

        product = Product.objects.create(
            category=category,
            title=title,
            cost=cost,
            photo=image
        )
        product.save()
    if next_page:
        parsing_products(category.href + "?p=" + next_page['data-page'], category)


def get_image(url):
    image_url = url
    file_name = image_url.split('/')[-1]
    request = requests.get(image_url, stream=True)

    lf = NamedTemporaryFile()

    for block in request.iter_content(1024 * 8):
        if not block:
            break
        try:
            lf.write(block)
        except Exception as e:
            lf.close()
            break

    if lf:
        file_obj = File(lf, name=file_name)
        return file_obj
    return None