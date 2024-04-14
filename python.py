from telebot import types
import telebot
import tweepy
from db import Database
bot = telebot.TeleBot('7088931319:AAH2DG5rBSR4zD5-_Qc7U7QcgFx1-kX20sw')
db = Database('database.db')

CONSUMER_KEY = '9TxOVR0OCKwCiQnFTYm1NXECN'
CONSUMER_SECRET = '4GvKKhIU2bpuUCV83XOae6OvyQ78UsbiCapxNiOFe2VMxC25c3'
ACCESS_TOKEN = '1194608150311317504-vkUlgp5WUaDpk30b6r21PQXrvt1XSe'
ACCESS_TOKEN_SECRET = 'bOdJIfL8GVB62NMvShwUw1Lt9vRZcJurrEZQfqJPeU4Wg'

auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def process_repost_link(message):
    repost_link = message.text
    # Получаем id поста из ссылки
    tweet_id = repost_link.split('/')[-1].split('?')[0]
    try:
        tweet = api.get_status(tweet_id)
        retweets = api.retweets(tweet_id)
        # Проверяем, зарепостил ли пользователь этот пост
        reposted = any(retweet.user.id == message.from_user.id for retweet in retweets)
        if reposted:
            bot.send_message(message.chat.id, "Да, вы репостили этот пост.")
        else:
            bot.send_message(message.chat.id, "Нет, вы не репостили этот пост.")
    except tweepy.TweepError as e:
        bot.send_message(message.chat.id, "Произошла ошибка при проверке репоста.")


def start_markup():
    markup = types.InlineKeyboardMarkup(row_width=True)
    link_keyboard1 = types.InlineKeyboardButton(text="Канал", url="https://t.me/checkthepepebot")
    check_keyboard = types.InlineKeyboardButton(text="Проверить✅", callback_data="check")
    markup.add(link_keyboard1, check_keyboard)
    return markup


def main_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Колонка 1
    terms_button = types.KeyboardButton("Условия/Terms📑")
    balance_button = types.KeyboardButton("Баланс/Balance🐸")
    # Колонка 2
    wallet_button = types.KeyboardButton("Кошелек/Wallet👛")
    bonus_button = types.KeyboardButton("Twitter [BONUS]🐦")
    # Колонка 3
    english_terms_button = types.KeyboardButton("Terms [ENG]")

    markup.row(terms_button, balance_button)
    markup.row(wallet_button, bonus_button)
    markup.row(english_terms_button)

    return markup


@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name

    if not db.user_exists(message.from_user.id):
        start_command = message.text
        referrer_id = str(start_command[7:])
        if str(referrer_id) != "":
            if str(referrer_id) != str(chat_id):
                db.add_user(message.from_user.id, referrer_id)

                try:
                    bot.send_message(referrer_id, "По вашей ссылке зарегистрировался новый пользователь!\n")
                except:
                    pass
            else:
                db.add_user(message.from_user.id)

                bot.send_message(message.from_user.id, 'Нельзя регистрироваться по собственной реферальной ссылке!')
    else:

        bot.send_message(chat_id, f'Привет! {first_name}! \n'
                          f'Чтобы воспользоваться ботом, сначала подпишись на канал!', reply_markup=start_markup())



def check(call):
    status = ['creator', 'administrator', 'member']
    try:
        if bot.get_chat_member(chat_id='-1002129297743',
                               user_id=call.message.chat.id).status == 'creator' or bot.get_chat_member(
                chat_id='-1002129297743', user_id=call.message.chat.id).status == 'administrator' or bot.get_chat_member(
                chat_id='-1002129297743', user_id=call.message.chat.id).status == 'member':
            bot.send_message(call.message.chat.id, "🔝 Главное Меню")
            # Отправка третьего сообщения с изображением и описанием AIRDROP PEPE COIN
            bot.send_photo(call.message.chat.id, photo=open('photo_2024-04-13_14-02-45.jpg', 'rb'),
                           caption="AIRDROP PEPE COIN 🐸\n\n200 $PEPE - за одного приведенного друга ? 😱\n"
                                   "Это самые лучшие условия для масштабного AIRDOP !\n\n"
                                   "Ничего проще не бывает! Абсолютно каждый участник получит DROP от PEPE 🐸\n"
                                   "Жми на кнопу «условия», там все подробности! Вперед!\n\n"
                                   "@checkthepepebot", reply_markup=main_menu_markup())
        else:
            bot.send_message(call.message.chat.id, f'Вы не подписаны. Подпишитесь на канал!', reply_markup=start_markup())
    except Exception as e:
        print(f"Ошибка в функции check: {e}")



@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'check':
        check(call)

    elif call.data == 'terms':
        bot.answer_callback_query(call.id, text="Вы выбрали Условия/Terms📑")
    elif call.data == 'balance':
        bot.answer_callback_query(call.id, text="Вы выбрали Баланс/Balance🐸")
    elif call.data == 'wallet':
        bot.answer_callback_query(call.id, text="Вы выбрали Кошелек/Wallet👛")
    elif call.data == 'bonus':
        bot.answer_callback_query(call.id, text="Вы выбрали Twitter [BONUS]🐦")
    elif call.data == 'english_terms':
        bot.answer_callback_query(call.id, text="Вы выбрали Terms [ENG]")


# Добавим основное меню в обработчик команды /menu


def send_terms(message):
    # Отправка сообщения с изображением и текстом
    bot.send_photo(message.chat.id, photo=open('photo_2024-04-13_14-41-27.jpg', 'rb'),
                   caption="УСЛОВИЯ \ TERMS 📃\n\n"
                           "Условия участия в AIRDROP не были еще такими простыми 😱\n"
                           "Абсолютно каждый участник получит токены $PEPE 🔥\n\n"
                           "Чтобы участвовать, Вам необходимо:\n"
                           "1. Быть подписанным на канал: @checkthepepebot\n"
                           "2. Пригласить всех друзей\n\n"
                           "За каждого приведённого друга, вы получите 200 $PEPE\n"
                           "Чтобы удвоить реферальный баланс, выполните дополнительное бонусное условие во вкладке Twitter [BONUS]\n\n"
                           "Вы можете приглашать друзей по вашей персональной реферальной ссылке: "
                           f'https://t.me/Pepecryptocurrencybot?start={message.from_user.id}\n',

                   reply_markup=invite_friend_markup(message))

def send_terms_eng(message):
    # Отправка сообщения с изображением и текстом
    bot.send_photo(message.chat.id, photo=open('photo_2024-04-13_14-41-27.jpg', 'rb'),
                   caption="The conditions of participation in AIRDROP have never been so simple 😱\n"
                           "Absolutely every participant will receive $PEPE tokens 🔥\n\n"
                           "To participate, you need to:\n"
                           "1. be subscribed to the channel: @checkthepepebot\n"
                           "2. Invite all your friends\n\n"
                           "For each friend you refer, you will receive 200 $PEPE.\n"
                           "To double your referral balance, fulfill the additional bonus condition in the Twitter tab [BONUS].\n\n"
                           "You can invite friends via your personal referral link: "
                           f'https://t.me/Pepecryptocurrencybot?start={message.from_user.id}',
                   reply_markup=invite_friend_markup(message))
def send_balance(message):
    user_id = message.from_user.id
    repost_status = db.get_repost_status(user_id)
    #Если зарепостил то не удваивается
    if repost_status == 0:
        # Отправка сообщения с изображением и текстом
        bot.send_photo(message.chat.id, photo=open('photo_2024-04-13_15-05-13.jpg', 'rb'),
                       caption=f"Ваш баланс: {db.count_referrals(user_id) * 200} $PEPE\n1 ref. = 200 $PEPE\n\n"
                               "Чтобы умножить ваш баланс на х2, выполните простое условие во вкладке Twitter\n\n"
                               "Пригласить больше друзей 👇🏼",
                       reply_markup=invite_friend_markup(message))
    elif repost_status == 1:
        bot.send_photo(message.chat.id, photo=open('photo_2024-04-13_15-05-13.jpg', 'rb'),
                       caption=f"Ваш баланс: {db.count_referrals(user_id) * 200 * 2} $PEPE\n1 ref. = 200 $PEPE\n\n"
                               "Чтобы умножить ваш баланс на х2, выполните простое условие во вкладке Twitter\n\n"
                               "Пригласить больше друзей 👇🏼",
                       reply_markup=invite_friend_markup(message))

def send_cancel_button(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = types.KeyboardButton("❌Отмена")
    markup.add(cancel_button)
    bot.send_message(message.chat.id, "Вы можете нажать кнопку ❌Отмена, чтобы вернуться в главное меню.", reply_markup=markup)


def cancel(message, menu_function):

    bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=main_menu_markup())
    menu_function()


def process_cancel_or_twitter_id(message):
    if message.text == "❌Отмена":
        cancel(message, main_menu_markup)
    elif message.text.startswith("@"):
        process_twitter_id(message)


def send_bonus(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    bot.send_photo(message.chat.id, photo=open('photo_2024-04-13_15-11-53.jpg', 'rb'),
                   caption="Помножь баланс на 2, выполните бонусное условие, отправьте свой твиттер ID\n\n "
                           "Важно! Баланс умножится на 2 после окончания AIRDROP!\n\n"
                           "Пожалуйста, отправьте ваш Twitter ID (например, @example_username):",
                   reply_markup=markup)
    # Отправляем кнопку "Отмена"
    send_cancel_button(message)
    if message.text.startswith("@"):
        bot.register_next_step_handler(message, process_twitter_id)

    # Установить обработчик для получения Twitter ID пользователя
def process_twitter_id(message):
    user_id = message.from_user.id
    twitter_id = message.text
    db.set_twitter_id(user_id, twitter_id)
    bot.send_message(message.chat.id, f"Ваш Twitter ID {twitter_id} успешно сохранен.")
    db.set_repost_status(1,user_id)
    # После сохранения Twitter ID перенаправляем пользователя в главное меню
    bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=main_menu_markup())




def invite_friend_markup(message):
    link = f"https://t.me/Pepecryptocurrencybot?start={message.chat.id}"
    markup = types.InlineKeyboardMarkup(row_width=1)
    invite_button = types.InlineKeyboardButton(text="Пригласить друга/invite", switch_inline_query=link)
    markup.add(invite_button)
    return markup


# Обработка команды /invite
@bot.message_handler(commands=['invite'])
def invite_friend(message):
    bot.send_message(message.chat.id, "Нажмите на кнопку, чтобы пригласить друга:", reply_markup=invite_friend_markup())


def wallet_message(message):
    bot.send_message(message.chat.id, "На стадии разработки...")
@bot.message_handler(commands=["menu"])
def menu(message):
    bot.send_message(message.chat.id, "Основное меню", reply_markup=main_menu_markup())

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Условия/Terms📑":
        send_terms(message)
    elif message.text == "Пригласить друга/invite":
        invite_friend(message)
    elif message.text == "Terms [ENG]":
        send_terms_eng(message)
    elif message.text == "Баланс/Balance🐸":
        send_balance(message)
    elif message.text == "Кошелек/Wallet👛":
        wallet_message(message)
    elif message.text == "Twitter [BONUS]🐦":
        send_bonus(message)
    else:
        process_cancel_or_twitter_id(message)




@bot.message_handler(func=lambda message: message.text.startswith("https://x.com/"))
def handle_repost_link(message):
    bot.send_message(message.chat.id, "Вы отправили ссылку на репост. Проверяю...")
    process_repost_link(message)

bot.polling(none_stop=True)