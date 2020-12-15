from lxml import html
import requests

def get_bufale():
    articles, articles_tmp = [], []
    #BUFALE.NET
    for pageNumber in range(1,2):
        page = requests.get('https://www.bufale.net/bufala/page/{}/'.format(pageNumber))
        tree = html.fromstring(page.content)

        articles.extend(tree.xpath('//div[@class="single-archive-post"]/div/div/h2/a/text()'))

        #print(articles)

    #BUTAC
    for pageNumber in range(1,2):
        page = requests.get('https://m.butac.it/category/bufala/page/{}/'.format(pageNumber))
        tree = html.fromstring(page.content)

        articles_tmp.extend(tree.xpath('//div[@class="td-module-thumb"]/a/@title'))
        #articles = tree.xpath('//div[@class="item-details"]/h3/a/text()') #this do not list first articles

        #print(articles)
    articles = articles + articles_tmp
    # for a in articles:
    #     a = a.replace("“", '').replace("”",'')
    return articles
