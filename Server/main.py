from datetime import datetime
from models import db, Room, Repaiment, init_storage, Owner
from flask import request
from application import app

koeff = 0.8

@app.route("/init", methods=['POST'])
def init():
    init_storage()
    return "Storage initialized"

@app.route("/repaiments", methods=['POST'])
def set_repaiments():
    data = request.json
    room_id = int(data.get('room_id'))
    owner_id = int(data.get('owner_id'))
    Repaiment.query.filter_by(room=room_id, owner=owner_id).delete()
    room = Room.query.get(room_id)
    if room is None:
        return "Room not found", 404
    
    owner = Owner.query.filter_by(name = "Uriy").first()
    if owner is None:
        return "Owner 'Uriy' not found", 404

    part = next((item.part for item in owner.parts if item.room == room_id), None)
    if part is None:
        return "Uriy's part is not found", 404

    total = koeff * part * room.price
    sum = 0
    for repaiment in sorted(data.get('repaiments'), key=lambda repaiment: repaiment['date'], reverse=False):
        if (sum + repaiment['target'] < total):
            db.session.add(Repaiment(room=room_id, owner=owner_id, amount=0, target=repaiment['target'], date=datetime.strptime(repaiment['date'], '%Y-%m')))
            sum += repaiment['target']
        elif (sum < total):
            db.session.add(Repaiment(room=room_id, owner=owner_id, amount=0, target=round(total - sum, 2), date=datetime.strptime(repaiment['date'], '%Y-%m')))
            sum = total
        else:
            break
    
    if sum < total:
        return f'Not enough repaiments ({total - sum:.2f})', 400

    db.session.commit()
    return "Storage initialized"

@app.route("/room/<int:room_id>", methods=['GET'])
def get_parts(room_id):
    room = Room.query.filter_by(id=room_id).first()
    if room is None:
        return "Room not found", 404
    
    output = { "id": room.id, "price": room.price, "owners": [], "repaiments": [] }
    for owner in room.owners:
        part = next((item.part for item in owner.parts if item.room == room_id), None)
        output["owners"].append({"name": owner.name, "part": part, "value": round(koeff * part * room.price, 2) })

    for repaiment in room.repaiments:
        output["repaiments"].append({"amount": repaiment.amount, "target": repaiment.target })
    
    return output

@app.route("/pay", methods=['POST'])
def pay():
    data = request.json
    room_id = int(data.get('room_id'))
    owner_id = int(data.get('owner_id'))
    date = datetime.strptime(data.get('date'), '%Y-%m')

    repaiments = Repaiment.query.filter_by(room=room_id, owner=owner_id).all()
    target = sum([int(item.target) for item in repaiments])
    total = sum([int(item.amount) for item in repaiments])
    if total + int(data.get('amount')) > target:
        return f"Summary payment can't be more than price of part. Overpayment {int(data.get('amount')) - (target - total)}", 400

    retaiment = Repaiment.query.filter_by(room=room_id, owner=owner_id, date = date).first()
    if retaiment is None:
        return "No repaiments found", 404
    
    retaiment.amount += int(data.get('amount'))
    db.session.commit()
    return "Payment accepted", 200

if __name__ == '__main__':
    app.run(port=3000, debug=True)
