from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.ext import CallbackQueryHandler
from typing import Final
from botdata import TOKEN, BOT_USERNAME # crete a file name botdata.py in the root folder and
                                        # set TOKEN and BOT_USERNAME of the bot.
from datetime import datetime, timedelta

# user defined modules
from meal import Meal

# members
allmembers = ['Adil', 'Elias', 'Labib', 'Nahid', 'Nurul', 'Pallob', 'Prottus', 'Swadhin']

# command functions
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    '/start'
    called at the start of the bot
    """
    await update.message.reply_text("Welcome to loser's Point meal system.")


async def members_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    '/members'
    show members in out flat
    """
    members_mess: list = allmembers
    for nm in members_mess:
        await update.message.reply_text(nm)


async def meal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    '/meal'
    handle meals
    """
    # button creating
    meal_button_11 = InlineKeyboardButton("1 1", callback_data='mbutton11')
    meal_button_10 = InlineKeyboardButton("1 0", callback_data='mbutton10')
    meal_button_01 = InlineKeyboardButton("0 1", callback_data='mbutton01')
    meal_button_00 = InlineKeyboardButton("0 0", callback_data='mbutton00')

    # creating keyboard layout for the buttons. this way the buttons will appear
    keyboard_layout = [
        [meal_button_11, meal_button_10],
        [meal_button_01, meal_button_00]
    ]

    # creating an in line keyboard markup object
    reply_markup = InlineKeyboardMarkup(keyboard_layout)

    # sending a message with the buttons
    await update.message.reply_text("Choose Your Meal Plan: ", reply_markup=reply_markup)

# manage meal button clicks
async def manage_meal_button_clicks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # incoming callback query from a user
    query = update.callback_query
    clicked_by = query.from_user  # user
    button_clicked = query.data  # callback_data

    # handle indivitual button activity
    if button_clicked == 'mbutton11':
        await query.answer("Choosed Plan: Lunch(1) Dinner(1)")
        await managerPallob(update, context)
    if button_clicked == 'mbutton10':
        await query.answer("Choosed Plan: Lunch(1) Dinner(0)")
        await managerPallob(update, context)
    if button_clicked == 'mbutton01':
        await query.answer("Choosed Plan: Lunch(0) Dinner(1)")
        await managerPallob(update, context)
    if button_clicked == 'mbutton00':
        await query.answer("Choosed Plan: Lunch(0) Dinner(0)")
        await managerPallob(update, context)

# run when /todayallmeals will be pressed
async def todayallmeals_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    '/todayallmeals
    show all meals for today
    """
    todate = datetime.today().date() # for showing present date
    
    # reading data
    # Meal class handle all the meal related operations
    meal_read = Meal('mealdata copy.xlsx')
    # readMeal read meal info from xlsx file and return a dict of the data
    todays_all_meals = await meal_read.readMeal(datetime.today().date())
    
    # print(todays_all_meals)
    todays_all_meals_str = "" # store all the user's present date meal info
    total_lunch = 0 # total lunch meal today
    total_dinner = 0 # total dinner meal today

    # organizing the users meal before display
    for nm, ml in todays_all_meals.items():
        number_of_ones = ml.count('1')
        # 2 meal booked
        if number_of_ones == 2:
            total_dinner += 1
            total_lunch += 1
            ml = 2 # 11 -> 2(insted of using 11 use 2 for better user understanding)
        elif number_of_ones == 1:
            ml = 1
            # lunch booked
            if ml == '10':
                total_lunch += 1
            # dinner booked
            else:
                total_dinner += 1
        # no meal booked
        else:
            ml = 0
        todays_all_meals_str += (str(nm) + "  :  " + str(ml) + "\n") # appending line by line
        # handle lunch and dinner
    
    #display the today meal data
    await update.message.reply_text(f"{todate}\n-----------------\nLunch: {total_lunch}, Dinner: {total_dinner}\n Total: {total_dinner + total_lunch}\n-----------------\n{todays_all_meals_str}")


# async def 
# inner functions
async def managerPallob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This feature is still in developing phase. Contact Manager Pallob for manual setup")


# handle responses
def handle_responses(text: str) -> str:
    text = text.lower()
    if 'alu' in text:
        return 'alu 40 taka kg. alu nia kono kotha hobe na'

# handle message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text_message: str = update.message.text

    print(f"user({update.message.chat.id}) in {message_type}: {text_message}")

    if message_type == 'group':
        if BOT_USERNAME in text_message:
            next_text_message: str = text_message.replace(BOT_USERNAME, "")
            response: str = handle_responses(next_text_message)
        else:
            pass
    else:
        response: str = handle_responses(text_message)
    print("Bot:", response)
    await update.message.reply_text(response)


# show relavent error message
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} causes error {context.error}")

if __name__ == '__main__':
    print("Starting bot:")
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('members', members_command))

    app.add_handler(CommandHandler('meal', meal_command))
    app.add_handler(CallbackQueryHandler(manage_meal_button_clicks))

    app.add_handler(CommandHandler('todayallmeals', todayallmeals_command))
    # message
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # error
    app.add_error_handler(error)

    #
    print("Polling.....")
    app.run_polling()
