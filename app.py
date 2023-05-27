from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.ext import CallbackQueryHandler
from typing import Final
from botdata import TOKEN, BOT_USERNAME # crete a file name botdata.py in the root folder and
                                        # set TOKEN and BOT_USERNAME of the bot.

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
    meal_button_ON = InlineKeyboardButton("ON", callback_data='mbuttonON')
    meal_button_OFF = InlineKeyboardButton("OFF", callback_data='mbuttonOFF')

    # creating keyboard layout for the buttons. this way the buttons will appear
    keyboard_layout = [
        [meal_button_11, meal_button_10],
        [meal_button_01, meal_button_00],
        [meal_button_ON, meal_button_OFF]
    ]

    # creating an in line keyboard markup object
    reply_markup = InlineKeyboardMarkup(keyboard_layout)

    # sending a message with the buttons
    await update.message.reply_text("Choose Your Meal Plan: ", reply_markup=reply_markup)


# inner functions
async def managerPallob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This feature is still in developing phase. Contact Manager Pallob for manual setup")

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
    if button_clicked == 'mbuttonON':
        await managerPallob(update, context)
    if button_clicked == 'mbuttonOFF':
        await managerPallob(update, context)


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

    # message
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # error
    app.add_error_handler(error)

    #
    print("Polling.....")
    app.run_polling()
