from lxml import html
import requests

#BUFALE.NET
for pageNumber in range(1,5):
    page = requests.get('https://www.bufale.net/bufala/page/{}/'.format(pageNumber))
    tree = html.fromstring(page.content)

    articles = tree.xpath('//div[@class="single-archive-post"]/div/div/h2/a/text()')

    print(articles)

#BUTAC
for pageNumber in range(1,5):
    page = requests.get('https://m.butac.it/category/bufala/page/{}/'.format(pageNumber))
    tree = html.fromstring(page.content)

    articles = tree.xpath('//div[@class="td-module-thumb"]/a/@title')
    #articles = tree.xpath('//div[@class="item-details"]/h3/a/text()') #this do not list first articles

    print(articles)
