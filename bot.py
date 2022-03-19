from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from settings import get_tg_token
from main import gen_pass


def get_keyboard(data, type_keyboard='main'):
    if type_keyboard == 'main':
        inline_keyboard = [
            [
                InlineKeyboardButton(text=' 🔄 Новые', callback_data='new'),
                InlineKeyboardButton(text=' 💾 Сохранить', callback_data='save'),
            ],
            [
                InlineKeyboardButton(text=f'{"»"if data["len_pass"] == 4 else ""}4 Симв',
                                     callback_data='len_4'),
                InlineKeyboardButton(text=f'{"»"if data["len_pass"] == 8 else ""}8 Симв',
                                     callback_data='len_8'),
                InlineKeyboardButton(text=f'{"»"if data["len_pass"] == 16 else ""}16 Симв',
                                     callback_data='len_16'),
                InlineKeyboardButton(text='✏ Симв', callback_data='len_wright'),
            ],
            [
                InlineKeyboardButton(text=f'Прописные {"✅" if data["upper"] else "❌"}',
                                     callback_data='upper'),
                InlineKeyboardButton(text=f'Строчные  {"✅" if data["lower"] else "❌"}',
                                     callback_data='lower'),
            ],
            [
                InlineKeyboardButton(text=f'Цифры {"✅" if data["num"] else "❌"}',
                                     callback_data='num'),
                InlineKeyboardButton(text=f'Спецсимволы {"✅" if data["other_symb"] else "❌"}',
                                     callback_data='other_symb'),
            ]
        ]
    return InlineKeyboardMarkup(inline_keyboard)


def msg_txt_handler(update: Update, context: CallbackContext):
    check_pass_settings(update, context)
    pass_settings = context.chat_data['pass_settings']
    msg_txt = update.message.text

    if pass_settings['len_pass'] == 'X':
        if msg_txt.isnumeric() and int(msg_txt) <= 100:
            pass_settings['len_pass'] = int(msg_txt)
        else:
            context.bot.send_message(update.effective_user.id,
                                     text='Введите длинну пароля числом. Max:100'
                                     )
    send_pass(update, context)


def callback_handler(update: Update, context: CallbackContext):
    callback_data = update.callback_query.data
    pass_settings = context.chat_data['pass_settings']

    if callback_data in ['upper', 'lower', 'num', 'other_symb']:
        pass_settings[callback_data] = not pass_settings[callback_data]

        if pass_settings['upper'] == \
                pass_settings['lower'] == \
                pass_settings['num'] == \
                pass_settings['other_symb'] is False:
            pass_settings['lower'] = True

    if callback_data in ['upper', 'lower', 'num', 'other_symb', 'new']:
        update.callback_query.edit_message_text(text=get_passwords(update, context),
                                                reply_markup=get_keyboard(context.chat_data['pass_settings']))

    elif callback_data == 'save':
        update.callback_query.edit_message_reply_markup(reply_markup=None)
        send_pass(update, context)

    elif callback_data.startswith('len_'):
        if callback_data[4:] != 'wright':
            pass_settings['len_pass'] = int(callback_data[4:])
            keyboard = get_keyboard(context.chat_data['pass_settings'])

            update.callback_query.edit_message_text(text=get_passwords(update, context), reply_markup=keyboard)
        elif callback_data[4:] == 'wright':
            update.callback_query.delete_message()
            pass_settings['len_pass'] = 'X'
            context.bot.send_message(update.effective_user.id,
                                     text='Введите длинну пароля числом. Max:100'
                                     )


def send_pass(update: Update, context: CallbackContext):
    check_pass_settings(update, context)

    context.bot.send_message(update.effective_user.id,
                             text=get_passwords(update, context),
                             reply_markup=get_keyboard(context.chat_data['pass_settings'])
                             )


def check_pass_settings(update: Update, context: CallbackContext):
    try:
        print(context.chat_data['pass_settings'])
    except:
        context.chat_data['pass_settings'] = {'upper': True,
                                              'lower': True,
                                              'num': True,
                                              'other_symb': True,
                                              'len_pass': 8}


def get_passwords(update: Update, context: CallbackContext):
    pass_settings = context.chat_data['pass_settings']

    pass_lst = gen_pass(len_pass=pass_settings['len_pass'],
                        use_nums=pass_settings['num'],
                        use_other_symb=pass_settings['other_symb'],
                        use_uppercase=pass_settings['upper'],
                        use_low=pass_settings['lower'])
    return pass_lst


def start(update: Update, context: CallbackContext):
    send_pass(update, context)


def main():
    updater = Updater(
        token=get_tg_token(), use_context=True
    )

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, msg_txt_handler))  # обработчик текстовых сообщений
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))

    # Начать бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
