from flask_sqlalchemy import SQLAlchemy
from application import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)
owner_room_table = db.Table('owner_room', db.Model.metadata,
    db.Column('owner_id', db.Integer, db.ForeignKey('owners.id'), primary_key=True),
    db.Column('room_id', db.Integer, db.ForeignKey('rooms.id'), primary_key=True),
    db.Column('part', db.Float, nullable=False, default=0)
)

class Owner(db.Model):
    """
    Сведения о владельце имущества.
    """
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    rooms = db.relationship("Room", secondary=owner_room_table, back_populates='owners')

class Repaiment(db.Model):
    """
    Сведения о платежах по кредиту.
    """
    __tablename__ = 'repaiments'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    target = db.Column(db.Float)
    date = db.Column(db.DateTime)
    room = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    owner = db.Column(db.Integer, db.ForeignKey('owners.id'))

class Room(db.Model):
    """
    Сведения о комнате.
    """
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    owners = db.relationship('Owner', secondary=owner_room_table, back_populates='rooms')
    repaiments = db.relationship('Repaiment', backref=db.backref('real_estate_object', lazy=True))

with app.app_context():
    db.create_all()

def init_owners():
    for owner in [Owner(name = "Roman"), Owner(name = "Uriy"), Owner(name = "Nuriya")]:
        db.session.add(owner)

    db.session.commit()

def init_first():
    room = Room()
    room.owners.append(Owner(name='Owner1'))
    db.session.add(room)
    db.session.commit()


def init_storage():
    """
    Инициализация хранилища.
    """
    rooms = Room.query.all()
    if rooms is None or len(rooms) != 4:
        room1 = Room()
        room2 = Room()
        db.session.add(room1)
        db.session.add(room2)
        db.session.commit()
        
        owner1 = Owner(name='Owner1')
        owner2 = Owner(name='Owner2')
        db.session.add(owner1)
        db.session.add(owner2)
        db.session.commit()
        
        room1.owners.append(owner1)
        room2.owners.append(owner2)
        db.session.commit()
        
        repaiment1 = Repaiment(amount=100, target=1, date='2020-01-01', room=1, owner=1)
        repaiment2 = Repaiment(amount=200, target=2, date='2020-01-02', room=2, owner=2)
        db.session.add(repaiment1)
        db.session.add(repaiment2)
        db.session.commit()