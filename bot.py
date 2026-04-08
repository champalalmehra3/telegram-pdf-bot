from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from pypdf import PdfReader, PdfWriter

BOT_TOKEN = "8651677584:AAG0nEioCT6RHP68zvGTgQUUJ5VH7I_rY1s"

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

    # Metadata me link add (safe method)
    writer.add_metadata({
        "/Title": CHANNEL_LINK,
        "/Author": "Telegram Bot"
    })

    # Save same name
    with open(file_name, "wb") as f:
        writer.write(f)

    # Send back
    await update.message.reply_document(document=open(file_name, "rb"))

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))

print("Bot started...")
app.run_polling()
