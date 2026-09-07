import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta


NEWS_QUERIES = [
    "Panasonic India startup",
    "Panasonic Ignition startup",
    "Panasonic Co.lab startup"
]


def fetch_news():

    articles = []

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=14)

    for query in NEWS_QUERIES:

        url = (
            "https://news.google.com/rss/search?"
            f"q={query.replace(' ', '+')}"
            "&hl=en-IN&gl=IN&ceid=IN:en"
        )

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.text)

        for item in root.findall(".//item"):

            title = item.findtext("title", default="")
            link = item.findtext("link", default="")
            pub_date = item.findtext("pubDate", default="")

            source_element = item.find("source")

            source = ""

            if source_element is not None:
                source = source_element.text or ""

            try:
                article_date = datetime.strptime(
                    pub_date,
                    "%a, %d %b %Y %H:%M:%S %Z"
                ).replace(tzinfo=timezone.utc)

            except ValueError:
                continue

            relevant_title = (
                "panasonic" in title.lower()
                and (
                    "startup" in title.lower()
                    or "co-creation" in title.lower()
                    or "co.lab" in title.lower()
                    or "ignition" in title.lower()
                )
            )

            if article_date >= cutoff_date and relevant_title:

                articles.append(
                    {
                        "title": title,
                        "link": link,
                        "published": pub_date,
                        "source": source
                    }
                )

    # Remove duplicate articles
    unique_articles = {}

    for article in articles:
        unique_articles[article["link"]] = article

    articles = list(unique_articles.values())

    # Sort newest first
    articles.sort(
        key=lambda article: article["published"],
        reverse=True
    )

    return articles