from flask import Flask, jsonify, request
import traceback
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Table, Text, Sequence
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)


Base = declarative_base()
metadata = Base.metadata


class Hat(Base):
    __tablename__ = 'hat'
    upc = Column(Integer, Sequence('hat_upc_seq'), primary_key=True)
    capacity = Column(String(127), nullable=True)
    description = Column(Text(), nullable=True)
    stock = Column(Integer)
    # image_link = Column(Text(), nullable=True)

    def to_dict(self):
        return {
            'upc': self.upc,
            'capacity': self.capacity,
            'description': self.description,
            'stock': self.stock,
        }


try:
    engine = create_engine(os.getenv(
        'DB_URI',
        'postgresql://howdy:partner@localhost:5432/howdy',
    ))
    db_session = sessionmaker(bind=engine)
except Exception as e:
    traceback.print_exc()
    print(repr(e))


@app.route('/inventory')
def get_hats():
    session = db_session()
    hats = [
        h.to_dict() for h in session.query(Hat).all()
    ]
    session.close()
    return jsonify({'inventory': hats})


@app.route('/inventory', methods=['POST'])
def add_hat():
    incoming = request.get_json()
    h = Hat(
        capacity=incoming.get('capacity', ''),
        description=incoming.get('description', ''),
        stock=incoming['stock'],
    )
    session = db_session()
    session.add(h)
    session.commit()
    session.close()
    return '', 204


@app.route('/inventory/<int:hat_id>', methods=['DELETE'])
def delete_hat(hat_id):
    session = db_session()
    to_delete = session.query(Hat).filter_by(upc=int(hat_id)).one()
    if to_delete:
        session.delete(to_delete)
        session.commit()
    else:
        session.close()
        return '', 404
    session.close()
    return '', 200


@app.route('/healthcheck')
def health():
    return jsonify({'happy': True})


if __name__ == '__main__':
    app.run('0.0.0.0')
