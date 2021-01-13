from flask import Flask, redirect, url_for, render_template, request
from datetime import datetime
from flask_socketio import SocketIO
from components.database import DataBase
from components.utilities import *

# app and socket init
app = Flask(__name__)
app.secret_key = "3hf9yf98yf9fy9f3ifb"
socketio = SocketIO(app)

# database and globals init
db = DataBase()
rooms = {}


# renders login page
@app.route("/", methods=["GET", "POST"])
def home():

	if request.method == 'POST':
		if request.form['user'] != '':
			user = request.form['user'].capitalize()
			code = str(request.form['room'])

			if not check_valid(code):
				code = generate_code(rooms)

			if check_username(user) and check_online(rooms, code, user):
				db.create_table(user)
				code = f"{code}-{user}"
				return redirect(url_for("chat", code=code))

	return render_template("home.html")


# renders chat page
@app.route("/chat/<code>", methods=["GET", "POST"])
def chat(code):
	return render_template("chat.html", code=code)


# renders chat history page
@app.route("/chat/<code>/history", methods=["GET", "POST"])
def history(code):
	raw = db.get(code[5:])
	messages = [(x[1], x[2]) for x in raw]

	if messages:
		messages.reverse()
		age = messages[len(messages)-1][1]
		count = len(messages)
	else:
		age, count = "N/A", "N/A"

	return render_template("history.html", code=code, messages=messages, age=age, count=count)


# deletes account and information
@app.route("/delete-account/<user>")
def delete(user):
	db.drop_table(user)
	return redirect(url_for("home"))


# method for socket broadcast
@socketio.on("message")
def handle_my_custom_event(json):
	global rooms
	user, code = json["user"], json["room"]
	print(code)
	dnow = datetime.now()

	if code not in rooms:
		rooms[code] = []
	if user not in rooms[code]:
		rooms[code].append(user)
		
		print(f"\n[Current connections] {len(rooms[code])}")
		print(f"[Current users] {rooms[code]}\n")

	print(f"\n[Message received] {json}\n")

	if "data" in json:
		db.append(user, json["data"], dnow.strftime("%d/%m/%Y %H:%M"))
		socketio.emit("relay", json)
	else:
		socketio.emit("online now", str(len(rooms[code])))


# method for socket disconnection
@socketio.on("disconnection")
def handle_disconnection(json):
	global rooms
	user, code = json["user"], json["room"]
	rooms[code].remove(user)

	print("\n[User disconnected]\n")

	if check_empty(rooms, code):
		rooms.pop(code)
	else:
		print(f"\n[Current connections] {len(rooms[code])}")
		print(f"[Current users] {rooms[code]}\n")

		socketio.emit("online now", str(len(rooms[code])))


# SocketIO app run
if __name__ == "__main__":
	socketio.run(app, debug=True)
	
