from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from PyPDF2 import PdfReader, PdfWriter
import os

Railway environment variable se token lega

BOT_TOKEN = os.getenv("BOT_TOKEN")

Apna channel link yahan set karo

CHANNEL_LINK = "https://t.me/raj_education_news"

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
document = update.message.document

# Original file name
file_name = document.file_name

# Download file
file = await document.get_file()
await file.download_to_drive(file_name)

# Read and write PDF
reader = PdfReader(file_name)
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Metadata me link add (optional but safe)
writer.add_metadata({
    "/Title": CHANNEL_LINK,
    "/Author": "Telegram Bot"
})

# Save file
with open(file_name, "wb") as f:
    writer.write(f)

# Send back with clickable caption link
await update.message.reply_document(
    document=open(file_name, "rb"),
    caption=f"अधिक जानकारी के लिए टेलीग्राम चैनल ज्वॉइन करे:\nhttps://t.me/raj_education_news"
)

# Optional cleanup
try:
    os.remove(file_name)
except:
    pass

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))

print("Bot started...")

app.run_polling()
