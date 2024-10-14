import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .model import Article, Base, Category


class Storage:
    def __init__(self):
        load_dotenv()

        user = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')
        host = os.getenv('POSTGRES_HOST')
        database = os.getenv('POSTGRES_DB')
        port = os.getenv('POSTGRES_PORT')

        self.database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

        self.engine = create_engine(self.database_url)

        Base.metadata.create_all(self.engine)

        self.session_maker = sessionmaker(bind=self.engine)

    def save_article(self, article: Article):
        with self.session_maker() as session:

            article_categories = article.categories
            article.categories = []

            for name in article_categories:
                name = name.name
                existing_category = session.query(Category).filter_by(name=name).first()
                if existing_category is None:
                    category = Category()
                    category.name = name

                    session.add(category)
                    session.commit()

                    existing_category = session.query(Category).filter_by(name=name).first()

                article.categories.append(existing_category)

            session.add(article)
            session.commit()
