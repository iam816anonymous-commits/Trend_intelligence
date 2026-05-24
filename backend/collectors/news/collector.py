from newspaper import Article as NewspaperArticle
import datetime
import logging
from sqlalchemy.orm import Session
from backend.storage.models import Article, Source

logger = logging.getLogger(__name__)

class NewsScraper:
    def collect(self, db: Session, source: Source):
        logger.info(f"Scraping news from {source.url}")
        # In a real scraper, we would find links on the page first.
        # For simplicity, we assume source.url is the article URL for now
        # OR we use newspaper3k build for source URL.

        try:
            # Note: Newspaper3k works best on specific article URLs or via build()
            # Here we just implement the extraction logic
            article_data = NewspaperArticle(source.url)
            article_data.download()
            article_data.parse()

            existing = db.query(Article).filter(Article.url == source.url).first()
            if existing:
                return

            article = Article(
                title=article_data.title,
                body=article_data.text,
                source_name=source.name,
                url=source.url,
                timestamp=datetime.datetime.utcnow(),
                category=source.category,
                country=source.country,
                language=source.language,
                raw_data={"authors": article_data.authors, "publish_date": str(article_data.publish_date)}
            )
            db.add(article)
            db.commit()
        except Exception as e:
            logger.error(f"Error scraping {source.url}: {e}")
