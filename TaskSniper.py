import telebot
from dbhelper import DBHelper


bot = telebot.TeleBot("")
bot.remove_webhook()

red_db = DBHelper("red_todo.sqlite")

yellow_db = DBHelper("yellow_todo.sqlite")

green_db = DBHelper("green_todo.sqlite")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Hey! I can help you with your tasks!")
	bot.send_message(message.chat.id, "My slogan is: One shot - one kill!")

### Create class for CRUD tasks ###
class TaskSniper:
	### create task 
	def new_task(self, message, DB):
		DB.setup()
		u_id = message.chat.id
		t = message.text.split(" ")
		t = t[1:]
		if t == []:
			bot.send_message(u_id, "Invalid input! Use /done_<priority> <your_task> !")
		else:
			task = ''
			for i in t:
				task += i + " "
			DB.add_item(task, u_id)
			bot.send_message(u_id, "Task '{}' created!".format(task))
			
	
	### get tasks
	def get_tasks(self, message, DB):
		DB.setup()
		u_id = message.chat.id
		items = DB.get_items(u_id)
		if items != []:	
			bot.send_message(u_id, "Your tasks: ")
			for item in items:
				bot.send_message(u_id, str(item))
		else:
			bot.send_message(u_id, "You haven't tasks")
		
			
	### delete task
	def done(self, message, DB):
		DB.setup()
		u_id = message.chat.id
		items = DB.get_items(u_id)
		t = message.text.split(" ")
		t = t[1:]
		if t == []:
			bot.send_message(message.chat.id, "Invalid input! Use /done_<priority> <your_task> !")
		else:
			task = ''
			for i in t:
				task += i + " "
			if items != []:
				if task in items:
					DB.delete_item(task, u_id)
					bot.send_message(message.chat.id, "Task '{}' deleted!".format(task))
				else:
					bot.send_message(message.chat.id, "You haven't task '{}'".format(task))
			else:
				bot.send_message(message.chat.id, "You haven't tasks")

### RED CRUD tasks ###
@bot.message_handler(commands=['new_red'])
def create(message):				
	RED_CRUD = TaskSniper()
	RED_CRUD.new_task(message, red_db)
	
@bot.message_handler(commands=['red'])
def get(message):				
	RED_CRUD = TaskSniper()
	RED_CRUD.get_tasks(message, red_db)

@bot.message_handler(commands=['done_red'])
def delete(message):				
	RED_CRUD = TaskSniper()
	RED_CRUD.done(message, red_db)

### YELLOW CRUD tasks ###
@bot.message_handler(commands=['new_yellow'])
def create(message):				
	YELLOW_CRUD = TaskSniper()
	YELLOW_CRUD.new_task(message, yellow_db)
	
@bot.message_handler(commands=['yellow'])
def get(message):				
	YELLOW_CRUD = TaskSniper()
	YELLOW_CRUD.get_tasks(message, yellow_db)

@bot.message_handler(commands=['done_yellow'])
def delete(message):				
	YELLOW_CRUD = TaskSniper()
	YELLOW_CRUD.done(message, yellow_db)
	
### GREEN CRUD tasks ###
@bot.message_handler(commands=['new_green'])
def create(message):				
	GREEN_CRUD = TaskSniper()
	GREEN_CRUD.new_task(message, green_db)
	
@bot.message_handler(commands=['green'])
def get(message):				
	GREEN_CRUD = TaskSniper()
	GREEN_CRUD.get_tasks(message, green_db)

@bot.message_handler(commands=['done_green'])
def delete(message):				
	GREEN_CRUD = TaskSniper()
	GREEN_CRUD.done(message, green_db)


bot.polling()

