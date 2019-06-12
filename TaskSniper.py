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


bot.polling()

