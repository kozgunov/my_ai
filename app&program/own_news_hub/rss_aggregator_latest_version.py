import feedparser
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser

app = Flask(__name__)

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_full_text(self):
        return ''.join(self.text)


RSS_FEEDS = {
    'Yahoo Finance': 'https://finance.yahoo.com/news/rssindex',
    'Hacker News': 'https://news/ycombinator.com/rss',
    'Wall Street Joural': 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
    'CNBC': 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partherId=wrss01&id=15839069'
}

@app.route('/')
def index():
    articles = []
    for source, feed in RSS_FEEDS.items():
        parsed_feed = feedparser.parse(feed)
        entries = [(source, entry) for entry in parsed_feed.entries]
        articles.extend(entries)
    # articles = [article for article in articles if article[1].published_parsed and datetime(*article[1].published_parsed[:6]) >= month]
    articles = sorted(articles, key=lambda x: getattr(x[1], 'published_parsed', None), reverse=True)

    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_articles = len(articles)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_articles = articles[start:end]

    return render_template('index.html', articles=paginated_articles, page=page, total_pages = total_articles // per_page + 1)


@app.route('/search')
def search():
    query = request.args.get('q')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    sort_by = request.args.get('sort', 'date')  # default sorting is by date
    articles = []

    for source, feed in RSS_FEEDS.items():
        parsed_feed = feedparser.parse(feed)
        entries = [(source, entry) for entry in parsed_feed.entries]
        articles.extend(entries)

    # Filter by query
    results = [article for article in articles if query.lower() in article[1].title.lower()]

    # Filter by date
    if from_date:
        from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
        results = [article for article in results if article[1].published_parsed and datetime(*article[1].published_parsed[:6]) >= from_date_obj]

    if to_date:
        to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')
        results = [article for article in results if article[1].published_parsed and datetime(*article[1].published_parsed[:6]) <= to_date_obj]

    # Sort results
    if sort_by == 'date':
        results = sorted(results, key=lambda x: getattr(x[1], 'published_parsed', None), reverse=True)
    elif sort_by == 'source':
        results = sorted(results, key=lambda x: x[0].lower())  # Sort sources alphabetically, ignoring case

    return render_template('search_result.html', articles=results, query=query)


@app.route('/fetch_full_text', methods=['POST'])
def fetch_full_text():
    article_link = request.form.get('article_link')

    # parse the text form sources via class beautifulsoup4

    try:
        response = requests.get(article_link)  # show the text description of article
        response.raise_for_status()  # check for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')
        full_text = soup.get_text() # extract main content from the article

        return render_template('full_text.html', full_text=full_text)
    except requests.exceptions.RequestException as e:
        return f"Error fetching article: {str(e)}", 500

    # parse the text form sources via class myhtmlparser

    #try:
    #    response = requests.get(article_link)
    #    response.raise_for_status()  # Check for HTTP errors
    #    parser = MyHTMLParser() # Use HTMLParser to extract text from the HTML
    #    parser.feed(response.text)
    #    full_text = parser.get_full_text()
    #    return render_template('full_text.html', full_text=full_text, previous_page=request.referrer)
    #except requests.exceptions.RequestException as e:
    #    return f"Error fetching article: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)





