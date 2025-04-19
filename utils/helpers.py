from telegram import Bot
from datetime import datetime
from config import Config
import os

async def get_user_info(user) -> str:
    """
    获取用户信息格式化字符串
    """
    username = f"@{user.username}" if user.username else "无"
    return (
        f"👤 用户ID: {user.id}\n"
        f"📛 姓名: {user.full_name}\n"
        f"🔗 用户名: {username}\n"
        f"🤖 是否机器人: {'是' if user.is_bot else '否'}"
    )

def format_time(timestamp: float) -> str:
    """
    格式化UNIX时间戳为可读时间
    """
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

async def send_log(context_or_bot, message: str) -> bool:
    """
    发送日志到日志频道和本地文件。
    参数可以是 ContextTypes.DEFAULT_TYPE 或 Bot。
    """
    # 自动识别 bot 实例
    bot = getattr(context_or_bot, "bot", context_or_bot)
    
    try:
        # ✅ 发送到日志频道
        if Config.LOG_CHANNEL:
            await bot.send_message(
                chat_id=Config.LOG_CHANNEL,
                text=f"📝 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n{message}"
            )
        
        # ✅ 写入本地日志文件
        if Config.LOG_FILE:
            log_dir = os.path.dirname(Config.LOG_FILE)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            with open(Config.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] {message}\n")
        
        return True

    except Exception as e:
        print(f"⚠️ 日志记录失败: {str(e)}")
        return False