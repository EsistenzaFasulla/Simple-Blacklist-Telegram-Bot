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
If u need help, dm me on telegram and i will help u.
'''

from pyrogram import Client, filters

import asyncio
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





# SETTINGS

ban = True # if set true the bot will ban the user blacklisted when will join in the group, turn False if you don't want him banned.

# this variable is needed to execute the commands: /block and /unblock
owner = [1234567890] # put your account telegram id here.









# when a user join in the group, the bot examine if a user is on the database, if yes, the user will be banned.
@app.on_message(filters.new_chat_members & filters.group)
async def blacklist(client, message):
    # opening database (if u don't have created the database yet, u need to create one. (table name: "users", column name: "id", type: "TEXT".)
    database = sqlite3.connect("blacklist.db")

    # define cursor to edit the database
    c = database.cursor()

    # check if the user is on the database's blacklist.
    exists = c.execute(f"select id from users where id='{message.from_user.id}'").fetchone()
    if exists:
        if ban: await app.ban_chat_member(message.chat.id, message.from_user.id)
        await message.reply(
            f"<b>{message.from_user.first_name}</b> is on blacklist because its defined as dangerous.")

    # save database's edit
    database.commit()
    # close the database
    database.close()

#command to add a user in blacklist (/block @username)
@app.on_message(filters.command("block"))
async def block_command(client, message):
    #if message.from_user.id in owner:
    database = sqlite3.connect("blacklist.db")
    c = database.cursor()
    isadmin = c.execute(f"select id from admins where id='{message.from_user.id}'").fetchone()
    if isadmin or message.from_user.id in owner:
        target = await app.get_users(message.command[1])

        exists = c.execute(f"select id from users where id='{target.id}'").fetchone()
        if exists:
            await message.reply(f"{target.first_name} is already on the blacklist.")
        else:
            # remove this comment if u want use SimpleBlacklist on single group   app.kick_chat_member(message.chat.id, message.command[1], int(time.time() + 604800)) # ban target for 1 week from group
            c.execute(f"INSERT INTO users VALUES ('{target.id}')")
            database.commit()
            await message.reply(f"{target.first_name} is succesful added in blacklist.")
            database.close()


# command to remove a user from blacklist (/unblock @username)
@app.on_message(filters.command("unblock"))
async def unblock_command(client, message):
        database = sqlite3.connect("blacklist.db")
        c = database.cursor()
        isadmin = c.execute(f"select id from admins where id='{message.from_user.id}'").fetchone()
        if isadmin or message.from_user.id in owner:
            target = await app.get_users(message.command[1])

            exists = c.execute(f"select id from users where id='{target.id}'").fetchone()
            if exists:
                c.execute(f"DELETE FROM users WHERE id = '{target.id}'") # remove the old blacklisted person from database.
                # remove this comment if u want use SimpleBlacklist in a single group app.unban_chat_member(message.chat.id, target.id) # unban the user from group
                await message.reply(f"{target.first_name} has correctly removed from blacklist.")
                database.commit()
                database.close()
            else:
                await message.reply(f"{target.first_name} not exists on database's blacklist.")



@app.on_message(filters.command("setadmin"))
async def setadmin_command(client, message):
    db = sqlite3.connect("blacklist.db")
    c = db.cursor()
    admin = c.execute(f"select id from admins where id='{message.from_user.id}'").fetchone()
    if admin or message.from_user.id in owner:
        target = await app.get_users(message.command[1])
        isadmin = c.execute(f"select id from admins where id='{target.id}'").fetchone()
        if isadmin:
            await message.reply("This user is already a bot's admin.")
        else:
            c.execute(f"insert into admins values('{target.id}')"); db.commit()
            await message.reply(f"Succesful added {target.first_name} in bot's admins.\n\nTo remove him, type /unsetadmin @username/ID")
    db.close()


@app.on_message(filters.command("unsetadmin"))
async def unsetadmin_command(client, message):
    db = sqlite3.connect("blacklist.db")
    c = db.cursor()
    admin = c.execute(f"select id from admins where id='{message.from_user.id}'").fetchone()
    if admin or message.from_user.id in owner:
        target = await app.get_users(message.command[1])
        if target.id in owner:
            await message.reply("You can't remove from admins the owner.")
            db.close()
            return;
        isadmin = c.execute(f"select id from admins where id='{target.id}'").fetchone()
        if isadmin:
            c.execute(f"DELETE FROM admins where id='{target.id}'"); db.commit()
            await message.reply(f"Correctly removed {target.id} from admins.\n\nTo readd him, type /setadmin @username/ID")
        else:
            await message.reply(f"{target.first_name} isn't admin.")
    db.close()



# if you want that the user blacklisted is alerted on the bot for every his message as blacklisted user, remove the comment from the code below

'''@app.on_message(filters.text)
async def check_messages(client, message):
    db = sqlite3.connect("blacklist.db"); c = db.cursor()
    isblacklisted = c.execute(f"select id from users where id='{message.from_user.id}'").fetchone()
    if isblacklisted:
        await message.reply(f"⚠️ {message.from_user.mention} is a blacklisted person.")
    db.close()'''




# run bot
app.run()