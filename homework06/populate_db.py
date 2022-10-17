import db
from scraputils import get_news


def populate_db():
    news = get_news('https://news.ycombinator.com', 34)
    s = db.session()
    for el in news:
        title = el['title'] if 'title' in el else ''
        author = el['author'] if 'author' in el else ''
        comments = el['comments'] if 'comments' in el else 0
        points = el['points'] if 'points' in el else 0
        url = el['url'] if 'url' in el else ''
        news = db.News(
            title=title,
            author=author,
            url=url,
            comments=comments,
            points=points)
        s.add(news)
    s.commit()


if __name__ == '__main__':
    populate_db()
