from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os
from dotenv import load_dotenv
import sqlite3
from datetime import datetime

# Load environment variables
load_dotenv()
TOKEN = os.getenv("8685632329:AAGJiC8s9IvfnblQz2wMV5WK-TS67tAN9_Q")

# SQLite database setup
conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS records (
    user_id INTEGER,
    username TEXT,
    action TEXT,
    time TEXT
)
""")
conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    keyboard = [["上班", "下班", "回座"], ["上厕所", "吃饭", "抽烟", "离开"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "欢迎使用打卡机器人！请使用下方按钮进行操作。",
        reply_markup=reply_markup,
    )

async def handle_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses (actions)."""
    action = update.message.text
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "匿名用户"
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Log action to database
    cursor.execute("INSERT INTO records (user_id, username, action, time) VALUES (?, ?, ?, ?)",
                   (user_id, username, action, time))
    conn.commit()
    
    # Craft response
    if action == "上班":
        text = f"上班 打卡成功！\n时间：{time}\n用户：{username or '匿名'}"
    elif action == "下班":
        text = f"下班 打卡成功！\n时间：{time}\n用户：{username or '匿名'}"
    else:
        text = f"{action} 操作记录成功！\n时间：{time}\n用户：{username or '匿名'}"
    
    await update.message.reply_text(text)

async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    await update.message.reply_text("使用 /start 开始打卡，使用下方按钮记录行为！")

def main():
    """Main function to start the bot."""
    app = Application.builder().token(TOKEN).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", show_help))
    
    # Handle actions
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_action))
    
    # Start polling
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
