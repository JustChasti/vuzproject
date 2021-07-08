import sys
import os
import create_base
import psycopg2
import config

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update


Base = declarative_base()


class Link(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    url = Column(String(512), nullable=False)
    name = Column(String(256), nullable=True)
    price = Column(Integer, nullable=True)
    articul = Column(Integer, nullable=True)
    col_otz = Column(Integer, nullable=True)


class Review(Base):
    __tablename__ = 'rewiews'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey(Link.id), nullable=False)
    user = Column(String(64), nullable=False)
    mark = Column(Integer, nullable=False)
    comment = Column(String(10000), nullable=False)


user = config.base_user
passs = config.base_pass
name = config.base_name


try:
    engine = create_engine("postgresql+psycopg2://" + user + ":" + passs + "@localhost/" + name)
    engine.connect()
except Exception as e:
    create_base.create(user, passs, name)
    engine = create_engine("postgresql+psycopg2://" + user + ":" + passs + "@localhost/" + name)
    engine.connect()
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine


Session = sessionmaker(bind=engine)


def append_link(link):
    session = Session()
    try:
        link = Link(url=link)
        session.add(link)
        session.commit()
    except Exception as e:
        create_tabless(user, passs, name)
        link = Link(url=link)
        session.add(link)
        session.commit()
    session.close()


def update_link(link, name, price, articul, k_otz, rev_list):
    session = Session()
    try:
        upd = session.query(Link).filter(Link.url == link).one()
    except Exception as e:
        print(link)
    upd.name = name
    upd.price = int(price)
    upd.articul = int(articul)
    upd.col_otz = int(k_otz)
    id = upd.id
    session.commit()
    session.close()
    update_reviews(id, rev_list)


def update_reviews(link_id, rev_list):
    session = Session()
    for i in rev_list:
        try:
            review = session.query(Review).filter(Review.product_id == link_id, Review.comment == i['Com']).one()
        except Exception as e:
            review = Review(product_id=link_id, user=i['Name'], mark=int(i['Mark']), comment=i['Com'])
            session.add(review)
    session.commit()
    session.close()


def get_links():
    session = Session()
    try:
        links = session.query(Link).all()
        urls = []
        for i in links:
            req = {}
            req['link'] = i.url
            urls.append(req)
        return urls
    except Exception as e:
        return []
    session.close()


def get_all():
    session = Session()
    try:
        links = session.query(Link).all()
        urls = []
        for i in links:
            req = {}
            req['url'] = i.url
            req['name'] = i.name
            req['price'] = i.price
            req['articul'] = i.articul
            req['col_otz'] = i.col_otz
            urls.append(req)
        return urls
    except Exception as e:
        return []


if __name__ == "__main__":
    print(get_links())
