import logging
import os
from dotenv import load_dotenv

from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загружаем переменные окружения из файла .env
load_dotenv()

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получаем токен бота из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ Токен бота не найден! Убедитесь, что он указан в файле .env")

# Определим кнопки меню
MAIN_MENU_BUTTONS = [
    [KeyboardButton("🏢 О компании")],
    [KeyboardButton("🛠 Услуги")],
    [KeyboardButton("📞 Контакты")]
]

BACK_BUTTON = [[KeyboardButton("⬅️ Назад")]]

# Функция для отправки главного меню
async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(MAIN_MENU_BUTTONS, resize_keyboard=True)
    await update.message.reply_text("Выберите раздел:", reply_markup=reply_markup)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать в справочник компании!")
    await send_main_menu(update, context)

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "⬅️ Назад":
        await send_main_menu(update, context)
        return

    # Раздел "О компании"
    if text == "🏢 О компании":
        reply_markup = ReplyKeyboardMarkup(BACK_BUTTON, resize_keyboard=True)
        await update.message.reply_text(
            "🏢 *О компании*\n\n"
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
            "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    # Раздел "Услуги"
    elif text == "🛠 Услуги":
        services_menu = [
            [KeyboardButton("🔧 Техническая поддержка")],
            [KeyboardButton("🌐 Веб-разработка")],
            [KeyboardButton("📱 Мобильные приложения")],
            [KeyboardButton("⬅️ Назад")]
        ]
        reply_markup = ReplyKeyboardMarkup(services_menu, resize_keyboard=True)
        await update.message.reply_text("Выберите услугу:", reply_markup=reply_markup)

    # Подразделы услуг
    elif text == "🔧 Техническая поддержка":
        reply_markup = ReplyKeyboardMarkup(BACK_BUTTON, resize_keyboard=True)
        await update.message.reply_text(
            "🔧 *Техническая поддержка*\n\n"
            "Наши специалисты готовы помочь вам 24/7. "
            "Lorem ipsum dolor sit amet, consectetur adipisicing elit.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    elif text == "🌐 Веб-разработка":
        reply_markup = ReplyKeyboardMarkup(BACK_BUTTON, resize_keyboard=True)
        await update.message.reply_text(
            "🌐 *Веб-разработка*\n\n"
            "Создаем современные и адаптивные сайты под ваши задачи. "
            "Duis aute irure dolor in reprehenderit in voluptate velit esse.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    elif text == "📱 Мобильные приложения":
        reply_markup = ReplyKeyboardMarkup(BACK_BUTTON, resize_keyboard=True)
        await update.message.reply_text(
            "📱 *Мобильные приложения*\n\n"
            "Разрабатываем iOS и Android приложения с интуитивным интерфейсом. "
            "Excepteur sint occaecat cupidatat non proident.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    # Раздел "Контакты"
    elif text == "📞 Контакты":
        reply_markup = ReplyKeyboardMarkup(BACK_BUTTON, resize_keyboard=True)
        await update.message.reply_text(
            "📞 *Контакты*\n\n"
            "📧 Email: info@example.com\n"
            "📱 Телефон: +7 (999) 123-45-67\n"
            "📍 Адрес: г. Москва, ул. Примерная, д. 10\n\n"
            "Режим работы: Пн–Пт с 9:00 до 18:00",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    # Неизвестная команда
    else:
        await update.message.reply_text("Пожалуйста, используйте кнопки меню.")
        await send_main_menu(update, context)

# Основная функция запуска
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()