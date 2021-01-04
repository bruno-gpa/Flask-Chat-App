from flask import Flask, redirect, url_for, render_template, request
from datetime import datetime
from flask_socketio import SocketIO
from components.database import DataBase

# app and socket init
app = Flask(__name__)
app.secret_key = "3hf9yf98yf9fy9f3ifb"
socketio = SocketIO(app)

# database and globals init
db = DataBase()
users = []


# renders login page
@app.route("/", methods=["GET", "POST"])
def home():

	if request.method == 'POST':
		if request.form['user'] != '':
			user = request.form['user']
			db.create_table(user)
			return redirect(url_for("chat", user=user))

	return render_template("home.html")


# renders chat page
@app.route("/chat/<user>", methods=["GET", "POST"])
def chat(user):
	return render_template("chat.html", user=user)


# renders chat history page
@app.route("/chat/<user>/history", methods=["GET", "POST"])
def history(user):
	raw = db.get(user)
	messages = [(x[1], x[2]) for x in raw]

	if messages:
		messages.reverse()
		age = messages[len(messages)-1][1]
		count = len(messages)
	else:
		age, count = "N/A", "N/A"

	return render_template("history.html", user=user, messages=messages, age=age, count=count)


# deletes account and information
@app.route("/delete-account/<user>")
def delete(user):
	db.drop_table(user)

	return redirect(url_for("home"))


# method for socket broadcast
@socketio.on("message")
def handle_my_custom_event(json):
	global users
	dnow = datetime.now()

	if json["user"] not in users:
		users.append(json["user"])
		
		print(f"\n[Current connections] {len(users)}")
		print(f"[Current users] {users}\n")

	print(f"\n[Message received] {json}\n")

	if "data" in json:
		db.append(json["user"], json["data"], dnow.strftime("%d/%m/%Y %H:%M"))
		socketio.emit("relay", json)
	else:
		socketio.emit("online now", str(len(users)))


# method for socket disconnection
@socketio.on("disconnection")
def handle_disconnection(json):
	global users
	users.remove(json["user"])

	print("\n[User disconnected]")
	print(f"[Current connections] {len(users)}")
	print(f"[Current users] {users}\n")

	socketio.emit("online now", str(len(users)))


# SocketIO app run
if __name__ == "__main__":
	socketio.run(app, debug=True)
	