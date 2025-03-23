from datetime import strptime
from models import db, Room, Repaiment, init_storage
from flask import request
from application import app


@app.route("/init", methods=['POST'])
def init():
    init_storage()
    return "Storage initialized"

@app.route("/repaiments", methods=['POST'])
def set_repaiments():
    data = request.json
    room_id = int(data.get('room_id'))
    owner_id = int(data.get('owner_id'))
    Repaiment.filter_by(room=room_id, owner=owner_id).delete()
    for repaiment in data.get('repaiments'):
        db.session.add(Repaiment(room=room_id, owner=owner_id, amount=0, target=repaiment['target'], date=strptime(repaiment['date'], '%Y-%m')))
    
    db.session.commit()
    return "Storage initialized"

@app.route("/room/<int:room_id>", methods=['GET'])
def get_parts(room_id):
    room = Room.query.filter_by(id=room_id).first()
    if room is None:
        return "Room not found", 404
    
    output = { "id": room.id, "price": room.price, "owners": [], "repaiments": [] }
    for owner in room.owners:
        output["owners"].append({"name": owner.name, "part": next((item.part for item in owner.parts if item.room == room_id), None) })

    for repaiment in room.repaiments:
        output["repaiments"].append({"amount": repaiment.amount, "target": repaiment.target })
    
    return output

@app.route("/pay", methods=['POST'])
def pay():
    data = request.json
    room_id = int(data.get('room_id'))
    owner_id = int(data.get('owner_id'))
    date = strptime(data.get('date'), '%Y-%m')
    retaiment = Repaiment.query.order_by(Repaiment.date.asc()).filter_by(room=room_id, owner=owner_id, date = date).first()
    if retaiment is None:
        return "No repaiments found", 404
    
    retaiment.amount += int(data.get('amount'))
    db.session.commit()

if __name__ == '__main__':
    app.run(port=3000, debug=True)
