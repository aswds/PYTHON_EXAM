import json
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

TOKEN = os.environ.get("TOKEN")
# Завантажуємо дані один раз
with open("all_topics.json", "r", encoding="utf-8") as f:
    topics = json.load(f)

# Пояснення символів, які можуть бути у формулах (поставити на початок відповіді, якщо є формули)
FORMULA_SYMBOLS_EXPLANATION = (
    "Пояснення символів у формулах:\n"
    "∑ — знак суми\n"
    "k, n, M — індекси та межі сумування\n"
    "h[k], x[n-k] — елементи послідовностей або сигналів\n"
    "· — множення\n"
    "log₂ — логарифм за основою 2\n"
    "Y, A, B — змінні логічних сигналів\n\n"
)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.isdigit():
        num = str(int(text))
        if num in topics:
            topic = topics[num]
            response_parts = [f"Тема {num}."]
            if "title" in topic:
                response_parts.append(topic["title"])
            if "content" in topic:
                response_parts.append(topic["content"])
            if "formulas" in topic and topic["formulas"].strip():
                # Додаємо пояснення символів, а потім формули
                response_parts.insert(1, FORMULA_SYMBOLS_EXPLANATION)
                response_parts.append("Формули:\n" + topic["formulas"])

            response_text = "\n\n".join(response_parts)
            await update.message.reply_text(response_text)
            return
        else:
            await update.message.reply_text("Номер поза межами діапазону. Спробуйте інший.")
            return

    await update.message.reply_text(
        "Привіт! Надішли номер (наприклад, 1 або 2), щоб отримати відповідь."
    )

if __name__ == "__main__":

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Bot started")
    app.run_polling
