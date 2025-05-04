import telebot
import subprocess
from telebot.types import Message

# Настройки бота
BOT_TOKEN = "8179325241:AAFDL8ZlMOmpSnk3_MjDDpwk0ZXqbcowzNQ"
ADMIN_IDS = [6646133212]  # ID админов, которым разрешено управление

bot = telebot.TeleBot(BOT_TOKEN)

# Проверка прав пользователя
def is_admin(user_id):
    return user_id in ADMIN_IDS

# Команда /install
@bot.message_handler(commands=["install"])
def install_docker(message: Message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ У вас нет прав на эту команду!")
        return

    bot.reply_to(message, "🔄 Запускаю установку Hikka в Docker...")

    try:
        # Собираем и запускаем Docker-контейнер
        commands = [
            "docker build -t hikka .",
            "docker run -d --name hikka_bot -p 8080:8080 hikka"
        ]

        for cmd in commands:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(result.stderr)

        bot.reply_to(message, "✅ Hikka успешно запущена в Docker!")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()