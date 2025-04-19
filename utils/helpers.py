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

# 在 send_log 中确保它能处理 parse_mode 参数
async def send_log(message: str, parse_mode: str = None) -> bool:
    try:
        bot = Bot(token=Config.BOT_TOKEN)  # 创建 bot 实例

        # 发送到日志频道
        if Config.LOG_CHANNEL:
            await bot.send_message(
                chat_id=Config.LOG_CHANNEL,
                text=f"📝 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n{message}",
                parse_mode=parse_mode  # 确保将 parse_mode 传递进去
            )

        # 写入本地日志文件
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
