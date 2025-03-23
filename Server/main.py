from models import Owner, Room, Repaiment, init_storage
from application import app

@app.route("/room/<int:room_id>", methods=['GET'])
def get_parts(room_id):
    room = Room.query.filter_by(id=room_id).first()
    if room is None:
        return "Room not found", 404
    
    output = "Owners:<br>"
    for owner in room.owners:
        output += f"{owner.name} owns this room. "

    output += "<br>Repaiments:<br>"
    for repaiment in room.repaiments:
        output += f"Repaiment: {repaiment.amount} for {repaiment.target}. "

    output += "<br>"
    
    return output

def pay():
    pass

if __name__ == '__main__':
    init_storage()
    app.run(port=3000, debug=True)
