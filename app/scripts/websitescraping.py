from lxml import html
import requests


def get_bufale(number_of_pages):
    articles_dict = []
    #BUFALE.NET
    for pageNumber in range(1, number_of_pages):
        articles = []
        page = requests.get('https://www.bufale.net/bufala/page/{}/'.format(pageNumber))
        tree = html.fromstring(page.content)

        articles.extend(tree.xpath('//div[@class="single-archive-post"]/div/div/h2/a'))

        for i, art in enumerate(articles):
            a = {"id": int(hash(art.text)), "title": art.text, "link": art.attrib["href"]}
            page2 = requests.get(a["link"])
            tree2 = html.fromstring(page2.content)
            a["body"] = " ".join(tree2.xpath("//div[@class='text-article']//text()")[1:-11])
            articles_dict.append(a)

    return articles_dict


    # #BUTAC
    # for pageNumber in range(1,number_of_pages):
    #     page = requests.get('https://m.butac.it/category/bufala/page/{}/'.format(pageNumber))
    #     tree = html.fromstring(page.content)
    #
    #     articles_tmp.extend(tree.xpath('//div[@class="td-module-thumb"]/a/@title'))
    #     #articles = tree.xpath('//div[@class="item-details"]/h3/a/text()') #this do not list first articles
    #
    #     #print(articles)
    # articles = articles + articles_tmp
    # # for a in articles:
    # #     a = a.replace("“", '').replace("”",'')
    # return articles
