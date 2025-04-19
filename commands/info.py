from telegram import Update
from telegram.ext import CommandHandler

async def group_info(update: Update, context):
    chat = update.effective_chat
    info = f"""
📊 群组信息
ID: {chat.id}
类型: {chat.type}
成员数: {await context.bot.get_chat_member_count(chat.id)}
    """
    await update.message.reply_text(info)

info_handler = CommandHandler("info", group_info)