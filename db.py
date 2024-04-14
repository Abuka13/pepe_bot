import sqlite3
class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exists(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self,user_id, referrer_id=None):
        with self.connection:
            if referrer_id != None:
                return self.cursor.execute("INSERT INTO `users` (`user_id`, `referrer_id`) VALUES (?, ?)", (user_id, referrer_id,))
                return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)",(user_id))

    def count_referrals(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(`id`) as count FROM `users` WHERE `referrer_id` = ?",(user_id,)).fetchone()[0]

    def set_repost_status(self,status,user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `status` = ? WHERE `user_id` = ?",
                                       (status, user_id))

    def get_repost_status(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `status` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchone()[0]

    def set_twitter_id(self, user_id, twitter_id):
        with self.connection:
            return self.cursor.execute("INSERT OR REPLACE INTO `users` (`user_id`, `twitter_id`) VALUES (?, ?)",
                                       (user_id, twitter_id))

    def get_twitter_id(self, user_id):
        self.cursor.execute("SELECT twitter_id FROM users WHERE user_id=?", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return None




