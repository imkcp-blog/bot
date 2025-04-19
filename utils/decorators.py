from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from config import Config
from telegram.error import BadRequest

def admin_required(func):
    """
    管理员权限校验装饰器
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        chat = update.effective_chat
        
        # 验证用户是否在管理员列表
        if user.id in Config.ADMIN_IDS:
            return await func(update, context, *args, **kwargs)
        
        # 验证群组管理员权限
        try:
            member = await chat.get_member(user.id)
            if member.status in ["administrator", "creator"]:
                return await func(update, context, *args, **kwargs)
        except BadRequest:
            pass
        
        await update.message.reply_text("🚫 需要管理员权限")
    return wrapper

def log_errors(func):
    """
    错误日志记录装饰器
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        try:
            return await func(update, context, *args, **kwargs)
        except Exception as e:
            error_msg = f"❌ 错误发生在 {func.__name__}: {str(e)}"
            print(error_msg)
            await send_log(context, error_msg)
    return wrapper