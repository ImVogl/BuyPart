from flask_sqlalchemy import SQLAlchemy
from application import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)
owner_room_table = db.Table('owner_room', db.Model.metadata,
    db.Column('owner_id', db.Integer, db.ForeignKey('owners.id'), primary_key=True),
    db.Column('room_id', db.Integer, db.ForeignKey('rooms.id'), primary_key=True)
)

class Part(db.Model):
    """
    Сведения о доле владения комнатой.
    """
    __tablename__ = 'parts'
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('owners.id'))
    room = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    part = db.Column(db.Float, nullable=False, default=0)

class Owner(db.Model):
    """
    Сведения о владельце имущества.
    """
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    rooms = db.relationship("Room", secondary=owner_room_table, back_populates='owners')
    parts = db.relationship('Part', backref=db.backref('owners', lazy=True))

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
    price = db.Column(db.Float)
    owners = db.relationship('Owner', secondary=owner_room_table, back_populates='rooms')
    repaiments = db.relationship('Repaiment', backref=db.backref('real_estate_object', lazy=True))
    parts = db.relationship('Part', backref=db.backref('rooms', lazy=True))

with app.app_context():
    db.create_all()

def init_owners():
    for owner in [Owner(name = "Roman"), Owner(name = "Uriy"), Owner(name = "Nuriya")]:
        db.session.add(owner)

    db.session.commit()

def init_room(price, parts):
    room = Room(price=price, parts=[])
    for owner in Owner.query.all():
        if owner.name not in parts:
            continue

        room.parts.append(Part(owner=owner.id, part=parts[owner.name]))
        room.owners.append(owner)
    
    db.session.add(room)
    db.session.commit()

def init_storage():
    """
    Инициализация хранилища.
    """
    rooms = Room.query.all()
    if rooms is None or len(rooms) != 4:
        init_owners()
        init_room(2625000, { "Roman": 0.35, "Uriy": 0.35, "Nuriya": 0.3 })
        init_room(3653000, { "Roman": 0.5, "Uriy": 0.5 })
        init_room(2713000, { "Roman": 0.5, "Uriy": 0.5 })
        init_room(2844000, { "Roman": 0.5, "Uriy": 0.5 })
