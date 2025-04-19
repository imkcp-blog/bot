from telegram import Update
from telegram.ext import CommandHandler
from config import Config

async def start(update: Update, context):
    await update.message.reply_text("🤖 机器人已上线！")

async def help(update: Update, context):
    help_text = """基本命令：
    /start - 启动机器人
    /help - 显示帮助"""
    await update.message.reply_text(help_text)

# 暴露给主程序的处理器
start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help)