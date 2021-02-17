'''
   _____          __                       .__  .__              ________
  /  _  \   _____/  |_  ____   ____   ____ |  | |  |   ____      \______ \
 /  /_\  \ /    \   __\/  _ \ /    \_/ __ \|  | |  |  /  _ \      |    |  \
/    |    \   |  \  | (  <_> )   |  \  ___/|  |_|  |_(  <_> )     |    `   \
\____|__  /___|  /__|  \____/|___|  /\___  >____/____/\____/     /_______  / /\
        \/     \/                 \/     \/                              \/  \/


   ______  __  __                                          __  __
  / ____ \/ / / ________  _________  ____ _____ ___  ___  / / / ________  _________ ___  ____  _________
 / / __ `/ / / / ___/ _ \/ ___/ __ \/ __ `/ __ `__ \/ _ \/ / / / ___/ _ \/ ___/ __ `__ \/ __ \/ ___/ __ \
/ / /_/ / /_/ (__  /  __/ /  / / / / /_/ / / / / / /  __/ /_/ (__  /  __/ /  / / / / / / /_/ (__  / /_/ /
\ \__,_/\____/____/\___/_/  /_/ /_/\__,_/_/ /_/ /_/\___/\____/____/\___/_/  /_/ /_/ /_/\____/____/\____/
 \____/

                ___________    .__
  ____   ____   \__    ___/___ |  |   ____   ________________    _____
 /  _ \ /    \    |    |_/ __ \|  | _/ __ \ / ___\_  __ \__  \  /     \
(  <_> )   |  \   |    |\  ___/|  |_\  ___// /_/  >  | \// __ \|  Y Y  \
 \____/|___|  /   |____| \___  >____/\___  >___  /|__|  (____  /__|_|  /
            \/               \/          \/_____/            \/      \/

'''


'''
Attention!
This code is only to blacklist toxic people from ur group/groups.

If u find need help, dm me on telegram and i will help u.
'''

from pyrogram import Client, filters

import time
import sqlite3


'''
How to get api_id and api_hash?

0. Sign up for Telegram using any application.
1. Log in to your Telegram core: https://my.telegram.org.
2. Go to 'API development tools' and fill out the form.
3. You will get basic addresses as well as the api_id and api_hash parameters required for user authorization.
4. For the moment each number can only have one api_id connected to it.
'''
api_id = 111111 # put your api_id
api_hash = "" # put your api_hash
api_key = "" # paste your bot token given from @BotFather

with Client("my_account", api_id, api_hash, api_key) as app:
    pass

# this variable is needed to execute the commands: /block and /unblock
owner = [1234] # put your account telegram id here.

# define user target for /block and /unblock commands
target = app.get_users(message.command[1])

# when a user join in the group, the bot examine if a user is on the database, if yes, the user will be banned.
@app.on_message(filters.new_chat_members & filters.group)
def blacklist(client, message):
    # opening database (if u don't have created the database yet, u need to create one. (table name: "users", column name: "id", type: "TEXT".)
    database = sqlite3.connect("blacklist.db")

    # define cursor to edit the database
    cursor = database.cursor()

    # check if the user is on the database's blacklist.
    cursor.execute("""SELECT id
                                   FROM users
                                   WHERE id=?""",
                   (message.from_user.id,))

    result = cursor.fetchone()
    if result:
        app.kick_chat_member(message.chat.id, message.from_user.id)
        message.reply(
            f"<b>{message.from_user.first_name}</b> is on blacklist because its defined as dangerous, i have banned him.")
    else:
        pass

    # save database's edit
    database.commit()
    # close the database
    database.close()

#command to add a user in blacklist (/block @username)
@app.on_message(filters.command("block"))
def block_command(client, message):
    if message.user.id in owner:
        database = sqlite3.connect("blacklist.db")

        cursor = database.cursor()

        cursor.execute("""SELECT id
                                               FROM users
                                               WHERE id=?""",
                       (target.id,))

        result = cursor.fetchone()

        if result:
            message.reply(f"{target.first_name} is already on the blacklist.")
        else:
            # remove this comment if u want use SimpleBlacklist on single group   app.kick_chat_member(message.chat.id, message.command[1], int(time.time() + 604800)) # ban target for 1 week from group
            cursor.execute("INSERT INTO utenti VALUES (?)", (target.id,))
            message.reply(f"{target.first_name} is added on blacklist.")
            database.commit()
            database.close()
    else:
        message.reply("Permission denied.")


# command to remove a user from blacklist (/unblock @username)
@app.on_message(filters.command("unblock"))
def unblock_command(client, message):

    database = sqlite3.connect("blacklist.db")

    cursor = database.cursor()

    cursor.execute("""SELECT id
                                       FROM users
                                       WHERE id=?""",
                   (target.id,))
    result = cursor.fetchone()
    if result:
        cursor.execute("""DELETE FROM utenti WHERE id = ?""", (target.id,)) # remove the old blacklisted person from database.
        # remove this comment if u want use SimpleBlacklist in a single group app.unban_chat_member(message.chat.id, target.id) # unban the user from group
        message.reply(f"{target.first_name} has correctly removed from blacklist.")
        database.commit()
        database.close()
    else:
        message.reply(f"{target.first_name} not exists on database's blacklist.")




# run bot
app.run()