from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Numeric, Uuid
from sqlalchemy.orm import relationship

from app.infrastructure.adapters.alchemy.metadata import metadata, mapper_registry

buy_table = Table(
    "buy",
    metadata,
    Column("oid", Uuid, primary_key=True),
    Column("client_id", Uuid, ForeignKey("client.oid"), nullable=False),
    Column("buy_description", String, nullable=False),
)

genre_table = Table(
    "genre",
    metadata,
    Column("oid", Uuid, primary_key=True),
    Column("name", String, nullable=False),
)

buy_book_table = Table(
    "buy_book",
    metadata,
    Column("oid", Uuid, primary_key=True),
    Column("buy_id", Uuid, ForeignKey("buy.oid"), nullable=False),
    Column("book_id", Uuid, ForeignKey("book.oid"), nullable=False),
    Column("amount", Integer, nullable=False),
)

book_table = Table(
    "book",
    metadata,
    Column("oid", Uuid, primary_key=True),
    Column("title", String, nullable=False),
    Column("author_id", Uuid, ForeignKey("author.oid"), nullable=False),
    Column("genre_id", Uuid, ForeignKey("genre.oid"), nullable=False),
    Column("price", Numeric, nullable=False),
    Column("amount", Integer, nullable=False),
)

buy_step_table = Table(
    "buy_step",
    metadata,
    Column("oid", Uuid, primary_key=True),
    Column("buy_id", Uuid, ForeignKey("buy.oid"), nullable=False),
    Column("step_id", Uuid, ForeignKey("step.oid"), nullable=False),
    Column("date_step_begin", DateTime, nullable=False),
    Column("date_step_end", DateTime, nullable=False),
)

client_table = Table(
    "client",
    metadata,
    Column("oid", Uuid, primary_key=True),
    Column("name", String, nullable=False),
    Column("city_id", Uuid, ForeignKey("city.oid"), nullable=False),
    Column("email", String, nullable=False),
)

city_table = Table(
    "city",
    metadata,
    Column("oid", Uuid, primary_key=True),
    Column("name", String, nullable=False),
    Column("days_delivery", DateTime, nullable=False),
)

author_table = Table(
    "author",
    metadata,
    Column("oid", Uuid, primary_key=True),
    Column("name", String, nullable=False),
)

step_table = Table(
    "step",
    metadata,
    Column("oid", Uuid, primary_key=True),
    Column("name", Uuid, nullable=False),
)


def start_mappers() -> None:
    """
    Map all domain models to ORM models, for purpose of using domain models directly during work with the database,
    according to DDD.
    """
    from app.domain.entities.city import City
    from app.domain.entities.client import Client
    from app.domain.entities.book import Book
    from app.domain.entities.buy_book import BuyBook
    from app.domain.entities.buy_step import BuyStep
    from app.domain.aggregates.buy import Buy
    from app.domain.values.book import Genre, Author
    from app.domain.values.buy_step import Step

    mapper_registry.map_imperatively(City, city_table)
    mapper_registry.map_imperatively(Client, client_table, properties={
        "city": relationship(City, backref="clients")
    })
    mapper_registry.map_imperatively(Book, book_table, properties={
        "genre": relationship(Genre, backref="books"),
        "author": relationship(Author, backref="books"),
    })
    mapper_registry.map_imperatively(BuyBook, buy_book_table, properties={
        "book": relationship(Book, backref="buy_books")
    })
    mapper_registry.map_imperatively(BuyStep, buy_step_table, properties={
        "step": relationship(Step, backref="buy_step")
    })
    mapper_registry.map_imperatively(Buy, buy_table, properties={
        "client": relationship(Client, backref="buys"),
        "books": relationship(BuyBook, backref="buy"),
        "steps": relationship(BuyStep, backref="buy"),
    })
    mapper_registry.map_imperatively(Genre, genre_table)
    mapper_registry.map_imperatively(Author, author_table)
    mapper_registry.map_imperatively(Step, book_table)
