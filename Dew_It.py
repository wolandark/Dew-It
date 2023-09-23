import telebot
import sqlite3
from telebot import types
from telebot.types import Message

# API Token From BotFather
bot = telebot.TeleBot('6297070230:AAG0Hqnc5Bj1Sn7062uAXsZBDwuxPyH8LOM')

# /start command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str()
    bot.reply_to(message, "Welcome to the Todo List Bot!")
    user_id = message.from_user.id #Gets the tg user's id
    print(f"user_id is : {user_id}")
    try:
        sqliteConnection = sqlite3.connect(f"database_of_{user_id}.db")
        cursor = sqliteConnection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS UserData
            (TaskID        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Description   TEXT              
                                        );''')
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()
    except sqlite3.Error as error:
        print(f"An Error occurred with the Sqlite Connection : {error}")

# /todo command
@bot.message_handler(commands=['todo'])
def add_task(message):
    user_id = str()
    user_id = message.from_user.id #Gets the tg user's id
    # text after the /todo command as the task description
    task_description = message.text[6:].strip()
    if task_description:
        sqliteConnection = sqlite3.connect(f"database_of_{user_id}.db")
        cursor = sqliteConnection.cursor()
        cursor.execute(f'''INSERT INTO UserData(Description) VALUES ("{task_description}")''')
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()
        bot.reply_to(message, f"Added task: {task_description}") 
    else:
        bot.reply_to(message, "Please provide a task description after /todo command.")# /list command

@bot.message_handler(commands=['list'])
def list_tasks(message):
    user_id = str()
    user_id = message.from_user.id #Gets the tg user's id
    try:
        sqliteConnection = sqlite3.connect(f"database_of_{user_id}.db")
        cursor = sqliteConnection.cursor()
    except sqlite3.Error as error:
        print(f"An Error occurred with the Sqlite Connection : {error}")

    sqliteConnection.row_factory = sqlite3.Row
    cursor.execute('SELECT * FROM UserData')
    rows = cursor.fetchall()
    if rows:
        task_list = "\n".join([f"{row[0]}: {row[1]}" for row in rows])
        bot.reply_to(message, f"Current tasks:\n{task_list}")
    else:
        bot.reply_to(message, "There are no tasks in the list.")

# /done command
@bot.message_handler(commands=['done'])
def mark_task_as_done(message):
    user_id = str()
    user_id = message.from_user.id #Gets the tg user's id
    try:
        sqliteConnection = sqlite3.connect(f"database_of_{user_id}.db")
        cursor = sqliteConnection.cursor()
    except sqlite3.Error as error:
        print(f"An Error occurred with the Sqlite Connection : {error}")

    # text after the /done command as the task ID
    task_id_str = message.text[6:].strip()
    if task_id_str:
        try:
            # Convert the task ID to an integer
            task_id = int(task_id_str)
            # Check if the task ID is valid
            cursor.execute(f'SELECT * FROM UserData WHERE TaskID={task_id}')
            row = cursor.fetchone()
            if row:
                task_description = row[1]
                cursor.execute(f'DELETE FROM UserData WHERE TaskID={task_id}')
                sqliteConnection.commit()
                bot.reply_to(message, f"Task {task_id}: {task_description} marked as done and removed from the list.")
            else:
                bot.reply_to(message, f"Invalid task ID. Use /list command to see the list of tasks.")
        except ValueError:
            bot.reply_to(message, f"Invalid task ID. Use /list command to see the list of tasks.")
    else:
        bot.reply_to(message, "Please provide a task ID after /done command.")

# Preview Commands
commands = [
    types.BotCommand("/start", "Start the bot"),
    types.BotCommand("/todo", "Add a new task to the todo list"),
    types.BotCommand("/list", "List your tasks"),
    types.BotCommand("/done", "Mark a task as finished"),
    types.BotCommand("/help", "Show help message"),
]

# Set Previews & Start Bot
bot.set_my_commands(commands)

bot.polling()


