from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config["SECRET_KEY"] = "3hf9yf98yf9fy9f3ifb"
socketio = SocketIO(app)

messages = []

@app.route("/")
def home():
	return render_template("test.html")

# relays message back to clients
@socketio.on('message')
def handle_message(msg):
	messages.append(msg)
	print(messages)
	send(msg, broadcast=True)


if __name__ == "__main__":
	socketio.run(app, debug=True)
