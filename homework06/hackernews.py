from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    id = request.query["id"]
    label = request.query["label"]

    item = s.query(News).get(id)
    item.label = label
    s.commit()

    redirect("/news")


@route("/update")
def update_news():
    s = session()
    news = get_news('https://news.ycombinator.com/newest')

    for el in news:
        title = el['title']
        if not list(s.query(News).filter(News.title == title)):
            title = el['title'] if 'title' in el else ''
            author = el['author'] if 'author' in el else ''
            comments = el['comments'] if 'comments' in el else 0
            points = el['points'] if 'points' in el else 0
            url = el['url'] if 'url' in el else ''
            new_el = News(
                title=title,
                author=author,
                url=url,
                comments=comments,
                points=points)
            s.add(new_el)

    s.commit()

    redirect('/news')


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":
    run(host="localhost", port=1234)

