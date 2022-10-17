import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    table = parser.findAll('table')[2]
    rows = table.findAll('tr')
    i = 0
    for row in rows:
        tds = row.findAll('td')
        for td in tds:
            if not td.has_attr('class'):
                continue

            if td['class'][0] == 'title':
                if not td.span:
                    break
                if td.span.a:
                    news_list.append({})
                    news_list[i]['title'] = td.span.a.contents[0]
                if td.span.span and td.span.span.a:
                    news_list[i]['url'] = 'http://' + td.span.span.a.span.contents[0]

            if td['class'][0] == 'subtext':
                if not td.span:
                    break
                if td.span.a:
                    news_list[i]['author'] = td.span.a.contents[0]
                anchor = td.span.findAll('a')[-1]
                if anchor and not anchor.parent['class'][0] == 'age':
                    news_list[i]['comments'] = int(anchor.contents[0].split('\xa0')[0])
                if td.span.span:
                    news_list[i]['points'] = int(td.span.span.contents[0].split(' ')[0])
                    i += 1
    del news_list[-1]

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    anchors = parser.findAll('a')
    for anchor in anchors:
        if anchor.has_attr('class') and anchor['class'][0] == 'morelink':
            return anchor['href']


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


if __name__ == '__main__':
    get_news('https://news.ycombinator.com', 1)