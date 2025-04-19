from telegram import Update
from telegram.ext import CommandHandler
from config import Config
from utils.decorators import admin_required

@admin_required
async def admin_panel(update: Update, context):
    await update.message.reply_text("管理面板已打开")

@admin_required
async def ban_user(update: Update, context):
    # 封禁逻辑
    pass

# 暴露处理器
admin_handler = CommandHandler("admin", admin_panel)
ban_handler = CommandHandler("ban", ban_user)
unban_handler = CommandHandler("unban", unban_user)