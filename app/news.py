
import requests
import xml.etree.ElementTree as ET

from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from urllib.parse import quote_plus


# Broad coverage of the Indian startup and corporate ecosystem.
# Each query has a category for displaying news in the application.

NEWS_QUERIES = [
    ("India startup funding investment venture capital", "Startup Funding & Investment"),
    ("Indian startup raises funding seed series A series B", "Startup Funding & Investment"),
    ("India corporate merger acquisition takeover", "Mergers & Acquisitions"),
    ("India corporate startup partnership collaboration", "Corporate-Startup Collaborations"),
    ("Indian startup business expansion product launch", "Startup Business & Growth"),
    ("India startup layoffs shutdown bankruptcy", "Startup Challenges & Shutdowns"),
    ("India artificial intelligence fintech EV deep tech startup", "Technology & Innovation"),
    ("India healthcare climate technology startup innovation", "Technology & Innovation"),
    ("India corporate IPO stock market business expansion", "Corporate & IPO News"),
    ("India startup government policy RBI SEBI regulation", "Business Policy & Regulation"),
    ("Panasonic India Ignition startup Co.lab Portl Sensio", "Panasonic & Startup Ecosystem")
]


def fetch_news():

    articles = []

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=14)

    for query, category in NEWS_QUERIES:

        url = (
            "https://news.google.com/rss/search?"
            f"q={quote_plus(query)}"
            "&hl=en-IN&gl=IN&ceid=IN:en"
        )

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            root = ET.fromstring(response.content)

        except (requests.RequestException, ET.ParseError) as error:
            print(f"News retrieval failed for '{query}': {error}")
            continue

        for item in root.findall(".//item"):

            title = item.findtext("title", default="")
            link = item.findtext("link", default="")
            pub_date = item.findtext("pubDate", default="")

            source_element = item.find("source")

            source = ""

            if source_element is not None:
                source = source_element.text or ""

            try:
                article_date = parsedate_to_datetime(pub_date)

                if article_date.tzinfo is None:
                    article_date = article_date.replace(
                        tzinfo=timezone.utc
                    )

                article_date = article_date.astimezone(timezone.utc)

            except (ValueError, TypeError):
                continue

            # Retain only articles from the previous 14 days.
            if article_date < cutoff_date:
                continue

            if not title or not link:
                continue

            articles.append({
                "title": title,
                "link": link,
                "published": pub_date,
                "source": source,
                "category": category,
                "_date": article_date
            })

    # Remove duplicate articles across different searches.
    unique_articles = {}

    for article in articles:

        link = article["link"]

        if link not in unique_articles:
            unique_articles[link] = article

    articles = list(unique_articles.values())

    # Sort newest first.
    articles.sort(
        key=lambda article: article["_date"],
        reverse=True
    )

    # Remove internal sorting field before returning.
    for article in articles:
        article.pop("_date", None)

    return articles
