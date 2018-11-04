# -*- coding: utf-8 -*-

import hashlib

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, ForeignKey, UniqueConstraint
from sqlalchemy import func, Column, Integer, CHAR, String, Text, DateTime


class CaseInsensitiveString(String):
    class comparator_factory(String.Comparator):
        def operate(self, op, other):
            return op(func.lower(self.expr), func.lower(other))

class Base(object):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

Model = declarative_base(cls=Base)


class Author(Model):
    __tablename__ = 'authors'
    name = Column(CaseInsensitiveString(255), unique=True, nullable=False)
    image_path = Column(String(255), nullable=True, default='')


QuoteTagAssoc= Table(
    'quote_tag_assoc',
    Model.metadata,
    Column('quote_id', Integer, ForeignKey('quotes.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class Tag(Model):
    __tablename__ = 'tags'
    name = Column(CaseInsensitiveString(255), unique=True, nullable=False)
    quotes = relationship('Quote', secondary=QuoteTagAssoc, back_populates='tags')


# https://docs.sqlalchemy.org/en/rel_1_0/core/defaults.html#context-sensitive-default-functions
def text_md5(context):
    text = context.current_parameters['text']
    return hashlib.md5(text.encode('utf-8')).hexdigest()

class Quote(Model):
    __tablename__ = 'quotes'
    text = Column(Text, nullable=False)
    text_hash = Column(CHAR(32), nullable=False, default=text_md5, onupdate=text_md5)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=True)
    author = relationship('Author', backref='quotes')
    tags = relationship('Tag', secondary=QuoteTagAssoc, back_populates='quotes')
    __table_args__ = (UniqueConstraint('text_hash', 'author_id'), )


if __name__ == '__main__':
    # Just demo
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    #engine = create_engine('sqlite:///quotesbot.db')
    engine = create_engine('mysql+mysqldb://root:@localhost/test?charset=utf8mb4')
    # engine = create_engine('postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]')
    Model.metadata.create_all(engine)
    session = Session(engine)
    quotes = [
        Quote(
            text='遗忘的剑被谁封印。',
            author=Author(name='fine'),
            tags=[Tag(name='me'), Tag(name='alone')]
        ),
        Quote(
            text='Making change',
            author=Author(name='jiansoung'),
            tags=[Tag(name='go go go...')]
        ),
    ]
    session.add_all(quotes)
    session.commit()
    session.close()
