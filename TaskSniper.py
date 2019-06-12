import telebot

bot = telebot.TeleBot("")
RED = {}
YELLOW = {}
GREEN = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	#print(message.chat.id)
	bot.send_message(message.chat.id, "Hey! I can help you with your tasks!")
	bot.send_message(message.chat.id, "My slogan is: One shot - one kill!")


@bot.message_handler(commands=['new_red'])
def new_red(message):
	#bot.send_message(message.chat.id, message.text)
	t = message.text.split(" ")
	t = t[1:]
	if t == []:
		print("Invalid input! Use /new_red <your_task>")
		bot.send_message(message.chat.id, "Invalid input! Use /new_red <your_task>")
	else:
		task = ''
		for i in t:
			task += i + " "
		if RED == {}:
			RED[message.chat.id] = [task]
		else:
			RED[message.chat.id].append(task)
		#RED[message.chat.id] = 
		print("RED", RED)
		bot.send_message(message.chat.id, "Red task '{}' created".format(task))


@bot.message_handler(commands=['new_yellow'])
def new_yellow(message):
	#bot.send_message(message.chat.id, message.text)
	t = message.text.split(" ")
	t = t[1:]
	if t == []:
		print("Invalid input! Use /new_yellow <your_task>")
		bot.send_message(message.chat.id, "Invalid input! Use /new_yellow <your_task>")
	else:	
		task = ''
		for i in t:
			task += i + " "
		if YELLOW == {}:
			YELLOW[message.chat.id] = [task]
		else:
			YELLOW[message.chat.id].append(task)
		print("YELLOW", YELLOW)
		bot.send_message(message.chat.id, "Yellow 'task {}' created".format(task))


@bot.message_handler(commands=['new_green'])
def new_green(message):
	#bot.send_message(message.chat.id, message.text)
	t = message.text.split(" ")
	t = t[1:]
	if t == []:
		print("Invalid input! Use /new_green <your_task>")
		bot.send_message(message.chat.id, "Invalid input! Use /new_green <your_task>")
	else:
		task = ''
		for i in t:
			task += i + " "
		if GREEN == {}:
			GREEN[message.chat.id] = [task]
		else:
			GREEN[message.chat.id].append(task)
		print("GREEN", GREEN)
		bot.send_message(message.chat.id, "Green task '{}' created".format(task))	


### For get tasks ###

@bot.message_handler(commands=['red'])
def new_red(message):
	if RED != {}:
		if message.chat.id in RED.keys():
			if RED[message.chat.id] != []:
				bot.send_message(message.chat.id, "RED tasks: ")
				for i in RED[message.chat.id]:
					bot.send_message(message.chat.id, i)
			else:
				bot.send_message(message.chat.id, "You haven't RED tasks")
		else:
				bot.send_message(message.chat.id, "You haven't RED tasks")
	else:
		bot.send_message(message.chat.id, "You haven't RED tasks")


@bot.message_handler(commands=['yellow'])
def new_yellow(message):
	if YELLOW != {}:
		if message.chat.id in YELLOW.keys():
			if YELLOW[message.chat.id] != []:
				bot.send_message(message.chat.id, "YELLOW tasks: ")
				for i in YELLOW[message.chat.id]:
					bot.send_message(message.chat.id, i)
			else:
				bot.send_message(message.chat.id, "You haven't YELLOW tasks")
		else:
			bot.send_message(message.chat.id, "You haven't YELLOW tasks")
	else:
		bot.send_message(message.chat.id, "You haven't YELLOW tasks")


@bot.message_handler(commands=['green'])
def new_green(message):
	if GREEN != {}:
		if message.chat.id in RED.keys():
			if GREEN[message.chat.id] != []:
				bot.send_message(message.chat.id, "GREEN tasks: ")
				for i in GREEN[message.chat.id]:
					bot.send_message(message.chat.id, i)
			else:
				bot.send_message(message.chat.id, "You haven't GREEN tasks")
		else:
			bot.send_message(message.chat.id, "You haven't GREEN tasks")
	else:
		bot.send_message(message.chat.id, "You haven't GREEN tasks")


### for deleting tasks ###	


@bot.message_handler(commands=['done_red'])
def done_red(message):
	t = message.text.split(" ")
	t = t[1:]
	if t == []:
		bot.send_message(message.chat.id, "Invalid input! Use /done_red <your_task> !")
	else:
		task = ''
		for i in t:
			task += i + " "
		if RED != {}:
			if task in RED[message.chat.id]:
				RED[message.chat.id].remove(task)
				bot.send_message(message.chat.id, "RED task '{}' deleted!".format(task))
			else:
				bot.send_message(message.chat.id, "You haven't RED task '{}'".format(task))
		else:
			bot.send_message(message.chat.id, "You haven't RED tasks!")


@bot.message_handler(commands=['done_yellow'])
def done_yellow(message):
	t = message.text.split(" ")
	t = t[1:]
	if t == []:
		bot.send_message(message.chat.id, "Invalid input! Use /done_yellow <your_task> !")
	else:
		task = ''
		for i in t:
			task += i + " "
		if YELLOW != {}:
			if task in YELLOW[message.chat.id]:
				YELLOW[message.chat.id].remove(task)
				bot.send_message(message.chat.id, "YELLOW task '{}' deleted!".format(task))
			else:
				bot.send_message(message.chat.id, "You haven't YELLOW task '{}'".format(task))
		else:
			bot.send_message(message.chat.id, "You haven't YELLOW tasks!")


@bot.message_handler(commands=['done_green'])
def done_green(message):
	t = message.text.split(" ")
	t = t[1:]
	if t == []:
		bot.send_message(message.chat.id, "Invalid input! Use /done_green <your_task> !")
	else:
		task = ''
		for i in t:
			task += i + " "
		if GREEN != {}:
			if task in GREEN[message.chat.id]:
				GREEN[message.chat.id].remove(task)
				bot.send_message(message.chat.id, "GREEN task '{}' deleted!".format(task))
			else:
				bot.send_message(message.chat.id, "You haven't GREEN task '{}'".format(task))
		else:
			bot.send_message(message.chat.id, "You haven't GREEN tasks!")


bot.polling()

