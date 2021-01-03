from flask import Flask, redirect, url_for, render_template, request
from datetime import datetime
from flask_socketio import SocketIO
from components.database import DataBase

# app and socket init
app = Flask(__name__)
app.secret_key = "3hf9yf98yf9fy9f3ifb"
socketio = SocketIO(app)

# database init
db = DataBase()


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
@app.route("/chat/<user>")
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
@socketio.on("my event")
def handle_my_custom_event(json):
	print(f"[Message received] {json}")
	dnow = datetime.now()

	if "user" in json:
		db.append(json["user"], json["data"], dnow.strftime("%d/%m/%Y %H:%M"))
	
	socketio.emit("my response", json)


# SocketIO app run
if __name__ == "__main__":
	socketio.run(app, debug=True)