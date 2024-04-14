def start(message: types.Message):
    if not db.user_exists(message.from_user_id):
        start_command = message.text
        referrer_id = str(start_command[7:])
        if str(referrer_id) != "":
            if str(referrer_id) != str(message.from_user_id):
                db.add_user(message.from_user.id, referrer_id)
                try:
                    bot.send_message(referrer_id, "По вашей ссылку зарегистрировался новый пользователь!")
                except:
                    pass
            else:
                db.add_user(message.from_user.id)
                bot.send_message(message.from_user.id,'Нельзя регистрироваться по собственной реферально ссылке!')
        else:
        db.add_user(message.from_user.id)
    bot.send_message(message.from_user.id, "Добро пожаловать!", reply_markup=start_markup())
