from lxml import html
import requests


def get_bufale(number_of_pages):
    articles_dict = []

    # BUFALE.NET
    for pageNumber in range(1, number_of_pages+1):
        articles = []
        page = requests.get('https://www.bufale.net/bufala/page/{}/'.format(pageNumber))
        tree = html.fromstring(page.content)

        articles.extend(tree.xpath('//div[@class="single-archive-post"]/div/div/h2/a'))

        for i, art in enumerate(articles):
            a = {"title": art.text, "url": art.attrib["href"]}
            page2 = requests.get(a["url"])
            tree2 = html.fromstring(page2.content)
            a["body"] = " ".join(tree2.xpath("//div[@class='text-article']//text()")[1:-11])
            articles_dict.append(a)

    # BUTAC
    for pageNumber in range(1, number_of_pages+1):
        articles = []
        page = requests.get('https://www.butac.it/bufala/page/{}/'.format(pageNumber))
        tree = html.fromstring(page.content)

        articles.extend(tree.xpath('//div[@class="title j-title"]/h3/a'))
        for i, art in enumerate(articles):
            a = {"title": art.text, "url": art.attrib["href"]}
            page2 = requests.get(a["url"])
            tree2 = html.fromstring(page2.content)
            a["body"] = " ".join(tree2.xpath("//div[@class='textArticle j-textArticle']//text()")[1:-15])
            articles_dict.append(a)

    return articles_dict


if __name__ =="__main__":
    d = get_bufale(2)
    for b in d:
        print(b)
