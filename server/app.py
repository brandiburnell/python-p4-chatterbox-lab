from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages = [message.to_dict() for message in Message.query.order_by(Message.created_at).all()]
    if request.method == 'GET':
        return make_response(messages, 200)
    
    if request.method == 'POST':
        new_message = Message(
            body=request.form.get("body"),
            username=request.form.get("username")
        )

        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()

        return make_response(message_dict, 201)

@app.route('/messages/<int:id>')
def messages_by_id(id):
    return ''

if __name__ == '__main__':
    app.run(port=5555)
