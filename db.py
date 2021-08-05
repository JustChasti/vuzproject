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
    
    
class Numeric(Base):
    __tablename__ = 'numericpar'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey(Link.id), nullable=False)
    price = Column(Integer, nullable=True)
    articul = Column(Integer, nullable=True)
    col_otz = Column(Integer, nullable=True)


user = config.base_user
passs = config.base_pass
name = config.base_name


engine = create_engine("postgresql://kscmpkdo:Ilx0eB0taA6_qe1ihCzlJGh_7eAEXOl0@batyr.db.elephantsql.com/kscmpkdo")
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
        upd.name = name
        if upd.price != int(price) or upd.articul != int(articul) or upd.col_otz != int(k_otz):
            num = Numeric(product_id=upd.id, price=int(price), articul=int(articul), col_otz=int(k_otz))
            session.add(num)
            upd.price = int(price)
            upd.articul = int(articul)
            upd.col_otz = int(k_otz)
        id = upd.id
        session.commit()
        session.close()
        update_reviews(id, rev_list)
    except Exception as e:
        print(link)


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
            if i.url == 'link1':
                pass
            else:
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
            if i.url == 'link1':
                pass
            else:
                try:
                    req['url'] = i.url
                    req['name'] = i.name
                    req['price'] = i.price
                    req['articul'] = i.articul
                    req['col_otz'] = i.col_otz
                    urls.append(req)
                except Exception as e:   
                    req['url'] = i.url
                    urls.append(req)
        session.close()
        return urls
    except Exception as e:
        session.close()
        return []


if __name__ == "__main__":
    update_link('https://www.wildberries.ru/catalog/16023993/detail.aspx?targetUrl=XS','Смартфон iPhone 11 128GB (новая комплектация), Apple', '54990', '16023993', '305',[])
    update_link('https://www.ozon.ru/product/15-6-noutbuk-lenovo-ideapad-l340-15api-amd-ryzen-3-3200u-2-6-ggts-ram-8-gb-256-gb-amd-266944297/','15.6" Ноутбук Lenovo IdeaPad L340-15API, AMD Ryzen 3 3200U (2.6 ГГц), RAM 8 ГБ, SSD 256 ГБ, AMD Radeon Vega 3, Windows 10 Home, (81LW00K0RU), синий', '16555', '228058566', '381',[])
 
