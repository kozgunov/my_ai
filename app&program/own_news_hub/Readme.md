 RSS News Hub

RSS News Hub is a Flask-based web application that aggregates articles from multiple RSS feeds, allowing users to search, filter, and view full content for the last month's news. The application supports search by keyword, filter by date, sorting by source or date, and pagination of results.

## Features

- Fetches news from multiple RSS feeds.
- Displays articles from the last 30 days.
- Search functionality with keyword filtering.
- Date filtering (choose a date range to refine search results).
- Sorting options (sort articles by date or source).
- Pagination for easier navigation through large result sets.
- "Get Full Text" button for each article to fetch the full content of the linked article.
- Responsive and clean design with CSS styling.

## Technologies Used

- **Flask**: Backend framework.
- **Feedparser**: Python library for parsing RSS feeds.
- **Requests**: Python library for fetching content from external websites.
- **HTML & Jinja2**: Template rendering.
- **CSS**: Styling for the user interface.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/rss-news-hub.git
cd rss-news-hub
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On Mac/Linux:
  ```bash
  source venv/bin/activate
  ```

### 3. Install the required dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

The application will be served at `http://127.0.0.1:5000/` by default.

### 5. Open the application in your browser

Go to the following URL to see the web application:

```
http://127.0.0.1:5000/
```

## Usage

### Homepage

- Displays articles from the configured RSS feeds.
- Use the **search bar** to search for keywords in the articles.
- Use the **date range** picker to filter articles within a specific time frame.
- Use the **sort dropdown** to sort articles by date or source.
- Click on **"Get Full Text"** to view the full content of an article.

### Search Results

- The search results page will display articles that match your search query, with options for further sorting and filtering.
- Click **"Back"** to return to the previous page without losing your search results.

## Adding New RSS Feeds

To add new RSS feeds, edit the `app.py` file. Locate the `RSS_FEEDS` dictionary and add new entries:

```python
RSS_FEEDS = {
    'Yahoo Finance': 'https://finance.yahoo.com/news/rssindex',
    'Hacker News': 'https://news.ycombinator.com/rss',
    'Wall Street Journal': 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
    'CNBC': 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839069'
}
```

## Project Structure

```bash
rss-news-hub/
├── app.py                # Main application file
├── requirements.txt      # Dependencies for the project
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── search_result.html# Search results page
│   └── full_text.html    # Full article content page
├── static/               # Static assets (CSS)
│   └── styles.css        # Stylesheet
└── README.md             # Project documentation
```

## Dependencies

- Flask
- Feedparser
- Requests
- HTMLParser (or BeautifulSoup)

To install all dependencies, run:

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the SPBU License. See the `LICENSE` file for details.
