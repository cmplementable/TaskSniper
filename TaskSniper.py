import telebot

bot = telebot.TeleBot("")
RED = {}
YELLOW = {}
GREEN = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Hey! I can help you with your tasks!")
	bot.send_message(message.chat.id, "My slogan is: One shot - one kill!")

### Create class for CRUD tasks ###
class TaskSniper:
	### create task 
	def new_task(self, message, DCT):
		t = message.text.split(" ")
		t = t[1:]
		if t == []:
			bot.send_message(message.chat.id, "Invalid input! Use /new_<priority> <your_task>")
		else:
			task = ''
			for i in t:
				task += i + " "
			if DCT == {}:
				DCT[message.chat.id] = [task]
			else:
				DCT[message.chat.id].append(task)
			print("{}".format(DCT))
			bot.send_message(message.chat.id, "Task '{}' created".format(task))
	
	### get tasks
	def get_tasks(self, message, DCT):
		if DCT != {}:
			if message.chat.id in DCT.keys():
				if DCT[message.chat.id] != []:
					bot.send_message(message.chat.id, "Tasks: ")
					for i in DCT[message.chat.id]:
						bot.send_message(message.chat.id, i)
				else:
					bot.send_message(message.chat.id, "You haven't tasks")
			else:
					bot.send_message(message.chat.id, "You haven't tasks")
		else:
			bot.send_message(message.chat.id, "You haven't tasks")
			
	### delete task
	def done(self, message, DCT):
		t = message.text.split(" ")
		t = t[1:]
		if t == []:
			bot.send_message(message.chat.id, "Invalid input! Use /done_<priority> <your_task> !")
		else:
			task = ''
			for i in t:
				task += i + " "
			if DCT != {}:
				if task in DCT[message.chat.id]:
					DCT[message.chat.id].remove(task)
					bot.send_message(message.chat.id, "Task '{}' deleted!".format(task))
				else:
					bot.send_message(message.chat.id, "You haven't task '{}'".format(task))
			else:
				bot.send_message(message.chat.id, "You haven't tasks!")

### RED CRUD tasks ###
@bot.message_handler(commands=['new_red'])
def create(message):				
	RED_CRUD = TaskSniper()
	RED_CRUD.new_task(message, RED)
	
@bot.message_handler(commands=['red'])
def get(message):				
	RED_CRUD = TaskSniper()
	RED_CRUD.get_tasks(message, RED)

@bot.message_handler(commands=['done_red'])
def delete(message):				
	RED_CRUD = TaskSniper()
	RED_CRUD.done(message, RED)

### YELLOW CRUD tasks ###
@bot.message_handler(commands=['new_yellow'])
def create(message):				
	YELLOW_CRUD = TaskSniper()
	YELLOW_CRUD.new_task(message, YELLOW)
	
@bot.message_handler(commands=['yellow'])
def get(message):				
	YELLOW_CRUD = TaskSniper()
	YELLOW_CRUD.get_tasks(message, YELLOW)

@bot.message_handler(commands=['done_yellow'])
def delete(message):				
	YELLOW_CRUD = TaskSniper()
	YELLOW_CRUD.done(message, YELLOW)
	
### GREEN CRUD tasks ###
@bot.message_handler(commands=['new_green'])
def create(message):				
	GREEN_CRUD = TaskSniper()
	GREEN_CRUD.new_task(message, GREEN)
	
@bot.message_handler(commands=['green'])
def get(message):				
	GREEN_CRUD = TaskSniper()
	GREEN_CRUD.get_tasks(message, GREEN)

@bot.message_handler(commands=['done_green'])
def delete(message):				
	GREEN_CRUD = TaskSniper()
	GREEN_CRUD.done(message, GREEN)

bot.polling()

