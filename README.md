Telegram Check-in Bot
Simple Telegram bot to record check-ins using SQLite.

Files
bot.py — main bot program (async, python-telegram-bot v20+)
requirements.txt — Python dependencies
.env.example — environment variable example
Setup
Python 3.8+ recommended.
Clone files into a folder.
Create a virtual environment (optional):
python -m venv venv
source venv/bin/activate (Linux/macOS) or venv\Scripts\activate (Windows)
Install dependencies:
pip install -r requirements.txt
Copy .env.example to .env and set TELEGRAM_TOKEN (from BotFather). Optionally set ADMIN_IDS.
Run:
python bot.py
Commands
/checkin [note] — Record a check-in. Optionally include a note.
/status — Show today's check-ins for the user.
/export [from_date] [to_date] — Admin only. Export CSV. Dates are YYYY-MM-DD. If only one date is given, exports that date. If no dates, exports all records.
/help — Show help message.
Notes & Improvements
This is a simple starter implementation. For production you might want:
Add rate-limiting and anti-fraud (geo/photo/face) checks.
Use a connection pool or a dedicated DB instance for heavy load.
Add scheduled reminders (cron / APScheduler).
Add web dashboard for admins.
