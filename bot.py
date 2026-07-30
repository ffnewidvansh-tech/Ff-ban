import os
import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# ============================================================
# CONFIGURATION - ENVIRONMENT VARIABLES
# ============================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Render.com env se lega
API_URL = "https://ffidbanapi.vercel.app/ban-account"
API_KEY = "ANIXH"
OWNER_ID = os.environ.get("OWNER_ID", "8471373583")  # Apna Telegram ID

# States for conversation
TOKEN_STATE = 1

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================================
# CHECK TOKEN
# ============================================================
if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable not set!")
    print("👉 Please set BOT_TOKEN in Render.com environment variables")
    exit(1)

# ============================================================
# START COMMAND
# ============================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_msg = f"""
🔥 FREE FIRE ACCOUNT BAN BOT 🔥

👋 Welcome {user.first_name}!

📌 How to use:
1️⃣ Send me your Free Fire Access Token
2️⃣ I will try to ban the account
3️⃣ Get instant result!

⚠️ Warning:
• Use at your own risk
• Only for educational purposes
• I am not responsible for any ban

💡 Example:
Send: xyz123abc456def789ghi012

🤖 Made with ❤️ by @iflexzyan
    """
    
    await update.message.reply_text(welcome_msg)

# ============================================================
# HELP COMMAND
# ============================================================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_msg = """
📖 How to get Access Token?

1️⃣ Open Free Fire Game
2️⃣ Go to Settings ⚙️
3️⃣ Click on Account
4️⃣ Find "Data Access" or "Login"
5️⃣ Copy the Access Token

🔑 Send me the token to ban!
    """
    await update.message.reply_text(help_msg)

# ============================================================
# ABOUT COMMAND
# ============================================================
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    about_msg = """
🤖 Free Fire Ban Bot

👨‍💻 Developer: @iflexzyan
🔗 Channel: https://t.me/+4ssy7cgJ7WQxMDA5

⚡ Features:
• Ban Free Fire Accounts
• Instant Results
• Simple & Easy

⚠️ Disclaimer:
This bot is for educational purposes only.
Use at your own risk!
    """
    await update.message.reply_text(about_msg)

# ============================================================
# BAN ACCOUNT FUNCTION
# ============================================================
async def ban_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    access_token = update.message.text.strip()
    
    # Show processing
    processing_msg = await update.message.reply_text(
        "⏳ Processing your request...\n\nPlease wait, I am banning the account!"
    )
    
    try:
        # API Call
        url = f"{API_URL}?access-token={access_token}&key={API_KEY}"
        response = requests.get(url, timeout=30)
        data = response.json()
        
        # ============================================================
        # PARSE RESPONSE - SIRF ID, NAME, UID
        # ============================================================
        account_id = data.get('id', 'N/A')
        account_name = data.get('name', 'N/A')
        account_uid = data.get('uid', 'N/A')
        status = data.get('status', 'UNKNOWN')
        message = data.get('message', 'No message')
        
        # Check if banned
        is_banned = "BANNED" in str(status).upper() or "BAN" in str(message).upper()
        
        # ============================================================
        # RESPONSE MESSAGE - SIRF ID, NAME, UID
        # ============================================================
        if is_banned:
            result_msg = f"""
✅ ACCOUNT BANNED SUCCESSFULLY!

📋 Account Details:
🆔 ID: {account_id}
👤 Name: {account_name}
🔢 UID: {account_uid}

⚠️ Account has been banned!
    """
        else:
            result_msg = f"""
❌ ACCOUNT NOT BANNED!

📋 Account Details:
🆔 ID: {account_id}
👤 Name: {account_name}
🔢 UID: {account_uid}

📌 Status: {status}
💬 Message: {message}

⚠️ Possible reasons:
• Invalid Access Token
• Account already banned
• Server error
    """
        
        # Delete processing message
        await processing_msg.delete()
        
        # Send result with buttons
        keyboard = [
            [InlineKeyboardButton("🔄 Try Again", callback_data="try_again")],
            [InlineKeyboardButton("📢 Join Channel", url="https://t.me/+4ssy7cgJ7WQxMDA5")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            result_msg,
            reply_markup=reply_markup
        )
        
    except requests.exceptions.Timeout:
        await processing_msg.delete()
        await update.message.reply_text(
            "⏰ Timeout Error!\n\nAPI is not responding. Please try again later."
        )
    except requests.exceptions.RequestException as e:
        await processing_msg.delete()
        await update.message.reply_text(
            f"❌ Error!\n\n{str(e)}\n\nPlease try again later."
        )
    except Exception as e:
        await processing_msg.delete()
        await update.message.reply_text(
            f"❌ Unexpected Error!\n\n{str(e)}"
        )

# ============================================================
# HANDLE CALLBACK (BUTTONS)
# ============================================================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == "try_again":
        await query.edit_message_text(
            "📤 Send me your Free Fire Access Token!"
        )
        return

# ============================================================
# STATS COMMAND (OWNER ONLY)
# ============================================================
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    
    if user_id != OWNER_ID:
        await update.message.reply_text("❌ Unauthorized!")
        return
    
    stats_msg = """
📊 BOT STATISTICS

🤖 Bot Status: 🟢 Online
👥 Total Users: (Coming soon)
📈 Requests Today: (Coming soon)

⚡ API Status: 🟢 Active
🔑 API Key: ANIXH

📅 Uptime: 100%
    """
    await update.message.reply_text(stats_msg)

# ============================================================
# CANCEL COMMAND
# ============================================================
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "❌ Operation cancelled!\n\nSend /start to use again."
    )

# ============================================================
# HANDLE TEXT (FOR TOKEN)
# ============================================================
async def handle_token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if it's a command
    if update.message.text.startswith('/'):
        return
    
    # Check if token length is reasonable
    token = update.message.text.strip()
    if len(token) < 30:
        await update.message.reply_text(
            "❌ Invalid Token!\n\nAccess token should be at least 30 characters long.\n\nSend /help to know how to get token."
        )
        return
    
    # Process ban
    await ban_account(update, context)

# ============================================================
# MAIN FUNCTION
# ============================================================
def main() -> None:
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("cancel", cancel))
    
    # Add message handler for tokens
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_token))
    
    # Add callback handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Start bot
    print("🤖 Bot is running...")
    print(f"👤 Owner ID: {OWNER_ID}")
    print(f"🔑 API Key: {API_KEY}")
    print(f"🌐 API URL: {API_URL}")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
