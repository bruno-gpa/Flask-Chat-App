import random


# checks if username is valid
def check_username(user):
	if user.replace(' ', '').isalpha():
		return True
	return False


# generates random code for new room
def generate_code(rooms):
	code = ''
	for i in range(4):
		code += str(random.choice(range(10)))
	if code not in rooms:
		return code
	else:
		return generate_code(rooms)


# checks if user is in another room
def check_online(rooms, code, user):
	for room in rooms:
		for person in rooms[room]:
			if person == user and code != room:
				return False
	return True


# checks if room code is valid
def check_valid(code):
	if code.isnumeric() and len(code) == 4:
		return True
	return False


# checks if room is empty
def check_empty(rooms, code):
	if rooms[code] == []:
		return True
	return False

