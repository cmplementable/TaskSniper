#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  taskSniper.py
#  
#  Copyright 2020 cmplementable
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import logging

from aiogram import Bot, Dispatcher, executor, types

from dbhelper import DBHelper


TOKEN = 'your_token_here'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

#initialize Databases
red_db = DBHelper("red_todo.sqlite")
yellow_db = DBHelper("yellow_todo.sqlite")
green_db = DBHelper("green_todo.sqlite")


# "start/" handler 
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer("Hey! I can help you with your tasks! \nMy slogan is: One shot - one kill!")
    
    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Create", "View")
    
    await message.answer("What do you want, create or view tasks?", reply_markup=markup)
    
    '''
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
    '''
    
### "Create" mode handler
@dp.message_handler(lambda message: message.text == "Create")
async def keyboard_handler(message: types.Message):
    await message.answer("Mode: Create!")
    await message.answer("For priority RED! \nWrite down your task: @<your_task> !")
    await message.answer("For priority YELLOW! \nWrite down your task: *<your_task> !")
    await message.answer("For priority GREEN! \nWrite down your task: $<your_task> !")

# create new red task 
@dp.message_handler(lambda message: message.text[0] == "@")
async def create_r(message: types.Message):
    RED_CRUD = TaskSniper()
    await RED_CRUD.new_task(message, red_db)
# create new yellow task    
@dp.message_handler(lambda message: message.text[0] == "*")
async def create_y(message: types.Message):
    YELLOW_CRUD = TaskSniper()
    await YELLOW_CRUD.new_task(message, yellow_db)
# create new green task
@dp.message_handler(lambda message: message.text[0] == "$")
async def create_g(message: types.Message):
    GREEN_CRUD = TaskSniper()
    await GREEN_CRUD.new_task(message, green_db)

### "View" mode handler
@dp.message_handler(lambda message: message.text == "View")	
async def view(message: types.Message):
	await message.answer("Mode View!")
	key_priority_view = types.ReplyKeyboardMarkup(True,False)
	key_priority_view.row("View red", "View yellow", "View green")
	await message.answer("Choose your priority: ", reply_markup=key_priority_view)

@dp.message_handler(lambda message: message.text == "View red")
async def view_red(message: types.Message):
	key = types.ReplyKeyboardMarkup(True,False)
	key.row("Create", "View")
	RED_CRUD = TaskSniper()
	items_r = RED_CRUD.get_tasks(message, red_db)
	items_red = types.ReplyKeyboardMarkup(True,False)
	if items_r != None:
		for i in items_r:
			items_red.add(i)
		await message.answer("Choose task for deletion: ", reply_markup=items_red)
	else:
		await message.answer("You haven't tasks", reply_markup=key)
	@dp.message_handler(lambda message: items_r != None and message.text in items_r)
	async def delete_r(message: types.Message):
		await RED_CRUD.done(message, red_db)
		await message.answer("Choose your mode: ", reply_markup=key)

@dp.message_handler(lambda message: message.text == "View yellow")
async def view_yellow(message: types.Message):
	key = types.ReplyKeyboardMarkup(True,False)
	key.row("Create", "View")
	YELLOW_CRUD = TaskSniper()
	items_y = YELLOW_CRUD.get_tasks(message, yellow_db)
	items_yellow = types.ReplyKeyboardMarkup(True,False)
	if items_y != None:
		for i in items_y:
			items_yellow.add(i)
		await message.answer("Choose task for deletion: ", reply_markup=items_yellow)
	else:
		await message.answer("You haven't tasks", reply_markup=key)
	@dp.message_handler(lambda message: items_y != None and message.text in items_y)
	async def delete_y(message: types.Message):
		await YELLOW_CRUD.done(message, yellow_db)
		await message.answer("Choose your mode: ", reply_markup=key)

@dp.message_handler(lambda message: message.text == "View green")
async def view_green(message: types.Message):
	key = types.ReplyKeyboardMarkup(True,False)
	key.row("Create", "View")
	GREEN_CRUD = TaskSniper()
	items_g = GREEN_CRUD.get_tasks(message, green_db)
	items_green = types.ReplyKeyboardMarkup(True,False)
	if items_g != None:
		for i in items_g:
			items_green.add(i)
		await message.answer("Choose task for deletion: ", reply_markup=items_green)
	else:
		await message.answer("You haven't tasks", reply_markup=key)
	@dp.message_handler(lambda message: items_g != None and message.text in items_g)
	async def delete_g(message: types.Message):
		await GREEN_CRUD.done(message, green_db)
		await message.answer("Choose your mode: ", reply_markup=key)

### Create class for CRUD tasks
class TaskSniper:
    ### create task 
    async def new_task(self, message, DB):
        DB.setup()
        u_id = message.chat.id
        task = message.text[1:]
        if task == None:
            await message.answer("Invalid input!")
        else:
            DB.add_item(task, u_id)
            await message.answer("Task '{}' created!".format(task))
            
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
    async def done(self, message, DB):
        DB.setup()
        u_id = message.chat.id
        items = DB.get_items(u_id)
        task = message.text
        if task == None:
            await message.answer("Invalid input!")
        else:
            if items != []:
                if task in items:
                    DB.delete_item(task, u_id)
                    await message.answer("Task '{}' deleted!".format(task))
                else:
                    await message.answer("You haven't task '{}'".format(task))
            else:
                await message.answer("You haven't tasks")
                
    async def reminder(self, message, DB):
        DB.setup()
        u_id = message.chat.id
        items = DB.get_items(u_id)
        if items != []: 
            bot.send_message(u_id, "You have task: " + str(items[0]))
        else:
            pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
