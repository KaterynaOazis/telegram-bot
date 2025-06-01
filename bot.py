import os
from datetime import datetime, time
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from langdetect import detect

# Отримуємо токен з середовища
TOKEN = os.getenv("BOT_TOKEN")

# Робочий час
WORK_START = time(9, 0)
WORK_END = time(18, 0)

# Відповіді на повідомлення поза робочим часом
RESPONSES = {
    'pl': "Nasi menedżerowie odpowiedzą na Twoje pytanie w godzinach pracy.\n"
          "09:00 - 18:00 – w tych godzinach nasz zespół jest zawsze dostępny.",
    'ru': "Наши менеджеры ответят вам в рабочие часы.\n"
          "09:00 – 18:00 – в это время команда всегда на связи.",
    'uk': "Наші менеджери дадуть відповідь у робочий час.\n"
          "09:00 – 18:00 – саме тоді команда на зв'язку.",
    'en': "Our managers will get back to you during business hours.\n"
          "09:00 – 18:00 – during this time, our team is always available.",
    'default': "We will respond during our business hours: 09:00 – 18:00."
}

# Відповіді на аварійні ситуації
ACCIDENT_RESPONSES = {
    'uk': "Зібрали для вас список цілодобових сервісів для допомоги в нічний час, а саме:\n\n"
          "1. Цілодобовий автомагазин: 📍https://maps.app.goo.gl/kAJTVjhWVwqp8R9S8\n"
          "2. Цілодобові шиномонтажі: 📍https://maps.app.goo.gl/ihAP8Mq6JrbfcPNY9\n"
          "📍https://maps.app.goo.gl/jHscEECMq7oaYX4X6\n"
          "3. Мобільний шиномонтаж: 📍https://maps.app.goo.gl/iaG17MJkGnd4RzQB9\n"
          "4. Евакуатор: +48 791 323 496 — Канат\n\n"
          "‼️ Всі послуги оплачуються по фактурі: NIP: 5213954140",
    'ru': "Собрали для вас список круглосуточных сервисов для помощи:\n\n"
          "1. Автомагазин: 📍https://maps.app.goo.gl/kAJTVjhWVwqp8R9S8\n"
          "2. Шиномонтаж: 📍https://maps.app.goo.gl/ihAP8Mq6JrbfcPNY9\n"
          "📍https://maps.app.goo.gl/jHscEECMq7oaYX4X6\n"
          "3. Мобильный шиномонтаж: 📍https://maps.app.goo.gl/iaG17MJkGnd4RzQB9\n"
          "4. Эвакуатор: +48 791 323 496 Канат\n\n"
          "‼️ Оплата по фактуре: NIP: 5213954140",
    'pl': "Przygotowaliśmy listę całodobowych usług pomocy:\n\n"
          "1. Sklep: 📍https://maps.app.goo.gl/kAJTVjhWVwqp8R9S8\n"
          "2. Montaż opon: 📍https://maps.app.goo.gl/ihAP8Mq6JrbfcPNY9\n"
          "📍https://maps.app.goo.gl/jHscEECMq7oaYX4X6\n"
          "3. Mobilny serwis: 📍https://maps.app.goo.gl/iaG17MJkGnd4RzQB9\n"
          "4. Laweta: +48 791 323 496 Kanat\n\n"
          "‼️ Faktura: NIP: 5213954140",
    'en': "24-hour emergency resources:\n\n"
          "1. Auto store: 📍https://maps.app.goo.gl/kAJTVjhWVwqp8R9S8\n"
          "2. Tire service: 📍https://maps.app.goo.gl/ihAP8Mq6JrbfcPNY9\n"
          "📍https://maps.app.goo.gl/jHscEECMq7oaYX4X6\n"
          "3. Mobile repair: 📍https://maps.app.goo.gl/iaG17MJkGnd4RzQB9\n"
          "4. Tow truck: +48 791 323 496 Kanat\n\n"
          "‼️ Invoice required: NIP: 5213954140"
}

# Обробник повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now().time()
    user_text = update.message.text.lower()

    try:
        lang = detect(user_text)
    except:
        lang = 'default'

    # 🔍 Триґери для аварій
    accident_keywords = [
        "пробив шину", "колесо", "не їде авто", "аварія", "дтп", "аварійна ситуація", "помилка", "чек гібрид", "лампа",
        "пробил шину", "машина не едет", "авария", "ошибка", "загорелся чек", "лампочка",
        "przebiłem", "koło", "gumę", "nie jedzie", "wypadek", "awaryjna", "błąd", "żarówka",
        "flat tire", "punctured", "won’t move", "accident", "emergency", "error", "check hybrid", "bulb", "lamp"
    ]

    if any(keyword in user_text for keyword in accident_keywords):
        await update.message.reply_text(ACCIDENT_RESPONSES.get(lang, ACCIDENT_RESPONSES['pl']))
        return

    # Відповідь поза робочим часом
    if now < WORK_START or now > WORK_END:
        await update.message.reply_text(RESPONSES.get(lang, RESPONSES['default']))

# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.TEXT, handle_message))
print("✅ Бот працює. Очікує повідомлень у групах...")
app.run_polling()
