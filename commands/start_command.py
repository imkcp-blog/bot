from telegram import Update
from telegram.ext import ContextTypes

# /start 命令处理函数
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /start 命令，欢迎用户"""
    await update.message.reply_text("欢迎使用机器人！输入 /help 获取帮助信息。")
