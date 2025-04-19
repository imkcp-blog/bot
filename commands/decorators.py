from functools import wraps
from telegram import Update
from config import Config

def admin_required(func):
    @wraps(func)
    async def wrapper(update: Update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in Config.ADMIN_IDS:
            await update.message.reply_text("❌ 需要管理员权限")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper