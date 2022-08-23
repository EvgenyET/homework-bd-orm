import json
import sqlalchemy
import os
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = "postgresql://postgres:321678@localhost:5432/homework6"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()


def init_db(session):
    with open('tests_data.json', 'r') as fd:
        data = json.load(fd)
        for record in data:
            model = {
                'publisher': Publisher,
                'shop': Shop,
                'book': Book,
                'stock': Stock,
                'sale': Sale
            }[record.get('model')]
            session.add(model(id=record.get('pk'), **record.get('fields')))
        session.commit()

def serch_shop(publisher):
    results = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.name == publisher).all()
    for s in results:
        print(f'Shop: {s.id}, {s.name}')


def serch_publisher(name_id):
    for publisher in session.query(Publisher).all():
        if publisher.name == name_id:
            return print(publisher)
        elif name_id.isdigit() and int(name_id) == publisher.id:
            return publisher
    else:
        return "Ни чего не нашлось"


if __name__ == "__main__":
    init_db(session)
    publisher = input("Ведите имя издателя для поиска магазина: ")
    serch_shop(publisher)