import telebot, schedule, threading, time
from telebot import types
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
	key = types.ReplyKeyboardMarkup(True,False)
	key.row("Create", "View")
	send = bot.send_message(message.chat.id, "Choose your mode: ", reply_markup=key)
	
	RED_CRUD = TaskSniper()
	items_r = RED_CRUD.get_tasks(message, red_db)
	YELLOW_CRUD = TaskSniper()
	items_y = YELLOW_CRUD.get_tasks(message, yellow_db)
	GREEN_CRUD = TaskSniper()
	items_g = GREEN_CRUD.get_tasks(message, green_db)
	if items_r != None:
		send_notify(RED_CRUD.reminder, message, red_db)
	elif items_r == None and items_y != None:
		send_notify(YELLOW_CRUD.reminder, message, yellow_db)
	elif items_y == None and items_g != None:
		send_notify(GREEN_CRUD.reminder, message, green_db)

@bot.message_handler(func=lambda message: message.text == "Create")
def keyboard_handler(message):
	if message.text == "Create":
		send = bot.send_message(message.chat.id, "Mode Create!")
		bot.send_message(message.chat.id, "For priority RED! Write down your task '@<your_task> !")
		bot.send_message(message.chat.id, "For priority YELLOW! Write down your task '*<your_task> !")
		bot.send_message(message.chat.id, "For priority GREEN! Write down your task '$<your_task> !")

@bot.message_handler(func=lambda message: message.text[0] == "@")
def create_r(message):
	RED_CRUD = TaskSniper()
	RED_CRUD.new_task(message, red_db)
	
@bot.message_handler(func=lambda message: message.text[0] == "*")
def create_y(message):
	YELLOW_CRUD = TaskSniper()
	YELLOW_CRUD.new_task(message, yellow_db)

@bot.message_handler(func=lambda message: message.text[0] == "$")
def create_g(message):
	GREEN_CRUD = TaskSniper()
	GREEN_CRUD.new_task(message, green_db)

@bot.message_handler(func=lambda message: message.text == "View")	
def view(message):
	send = bot.send_message(message.chat.id, "Mode View!")
	key_priority_view = telebot.types.ReplyKeyboardMarkup(True,False)
	key_priority_view.row("View red", "View yellow", "View green")
	send = bot.send_message(message.chat.id, "Choose your priority: ", reply_markup=key_priority_view)

@bot.message_handler(func=lambda message: message.text == "View red")
def view_red(message):
	key = types.ReplyKeyboardMarkup(True,False)
	key.row("Create", "View")
	RED_CRUD = TaskSniper()
	items_r = RED_CRUD.get_tasks(message, red_db)
	items_red = telebot.types.ReplyKeyboardMarkup(True,False)
	if items_r != None:
		for i in items_r:
			items_red.add(i)
		send = bot.send_message(message.chat.id, "Choose task: ", reply_markup=items_red)
	else:
		send = bot.send_message(message.chat.id, "You haven't tasks", reply_markup=key)
	@bot.message_handler(func=lambda message: items_r != None and message.text in items_r)
	def delete_r(message):
		print("Red")
		RED_CRUD.done(message, red_db)
		send = bot.send_message(message.chat.id, "Choose your mode: ", reply_markup=key)

@bot.message_handler(func=lambda message: message.text == "View yellow")
def view_yellow(message):
	key = types.ReplyKeyboardMarkup(True,False)
	key.row("Create", "View")
	YELLOW_CRUD = TaskSniper()
	items_y = YELLOW_CRUD.get_tasks(message, yellow_db)
	items_yellow = telebot.types.ReplyKeyboardMarkup(True,False)
	if items_y != None:
		for i in items_y:
			items_yellow.add(i)
		send = bot.send_message(message.chat.id, "Choose task: ", reply_markup=items_yellow)
	else:
		send = bot.send_message(message.chat.id, "You haven't tasks", reply_markup=key)
	@bot.message_handler(func=lambda message: items_y != None and message.text in items_y)
	def delete_y(message):
		print("Yellow")
		YELLOW_CRUD.done(message, yellow_db)
		send = bot.send_message(message.chat.id, "Choose your mode: ", reply_markup=key)

@bot.message_handler(func=lambda message: message.text == "View green")
def view_green(message):
	key = types.ReplyKeyboardMarkup(True,False)
	key.row("Create", "View")
	GREEN_CRUD = TaskSniper()
	bot.send_message(message.chat.id, "Priority GREEN! Choose task for delete!")
	items_g = GREEN_CRUD.get_tasks(message, green_db)
	items_green = telebot.types.ReplyKeyboardMarkup(True,False)
	if items_g != None:
		for i in items_g:
			items_green.add(i)
		send = bot.send_message(message.chat.id, "Choose task: ", reply_markup=items_green)
	else:
		send = bot.send_message(message.chat.id, "You haven't tasks", reply_markup=key)
	@bot.message_handler(func=lambda message: items_g != None and message.text in items_g)
	def delete_g(message):
		print("GREEN")
		GREEN_CRUD.done(message, green_db)
		send = bot.send_message(message.chat.id, "Choose your mode: ", reply_markup=key)

def send_notify(job, message, db):
	schedule.every().hour.do(job, message=message, DB=db)
	kill_update = threading.Event()

	class SearchUpdateThread(threading.Thread):
		def run(self):
			while not kill_update.is_set():
				schedule.run_pending()
				time.sleep(10)
				
	searchThread = SearchUpdateThread()
	searchThread.setDaemon(True)
	searchThread.start()


### Create class for CRUD tasks ###
class TaskSniper:
	### create task 
	def new_task(self, message, DB):
		DB.setup()
		u_id = message.chat.id
		task = message.text[1:]
		if task == None:
			bot.send_message(u_id, "Invalid input!")
		else:
			DB.add_item(task, u_id)
			bot.send_message(u_id, "Task '{}' created!".format(task))
			
	### get tasks
	def get_tasks(self, message, DB):
		DB.setup()
		u_id = message.chat.id
		items = DB.get_items(u_id)
		if items != []:	
			return items
		else:
			pass
	### delete task
	def done(self, message, DB):
		DB.setup()
		u_id = message.chat.id
		items = DB.get_items(u_id)
		task = message.text
		if task == None:
			bot.send_message(message.chat.id, "Invalid input!")
		else:
			if items != []:
				if task in items:
					DB.delete_item(task, u_id)
					bot.send_message(message.chat.id, "Task '{}' deleted!".format(task))
				else:
					bot.send_message(message.chat.id, "You haven't task '{}'".format(task))
			else:
				bot.send_message(message.chat.id, "You haven't tasks")
				
	def reminder(self, message, DB):
		DB.setup()
		u_id = message.chat.id
		items = DB.get_items(u_id)
		if items != []:	
			bot.send_message(u_id, "You have task: " + str(items[0]))
		else:
			pass

bot.polling()

