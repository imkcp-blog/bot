from telegram import Bot
from datetime import datetime
from config import Config
import os
import json

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

# 设置文件路径
USER_POINTS_FILE = "user_points.json"

# 确保用户积分文件存在，如果不存在则创建一个空的文件
if not os.path.exists(USER_POINTS_FILE):
    with open(USER_POINTS_FILE, "w") as f:
        json.dump({}, f)

def _load_data():
    """加载积分数据"""
    with open(USER_POINTS_FILE, "r") as f:
        return json.load(f)

def _save_data(data):
    """保存积分数据"""
    with open(USER_POINTS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def sign_in(user_id):
    """签到功能，用户签到并获得20积分"""
    data = _load_data()
    
    # 获取今天的日期
    today = datetime.today().date().strftime("%Y-%m-%d")
    
    # 如果用户今天已经签到，则返回 False
    if str(user_id) in data and "last_sign_in" in data[str(user_id)] and data[str(user_id)]["last_sign_in"] == today:
        return False
    
    # 否则，更新积分并记录签到日期
    if str(user_id) not in data:
        data[str(user_id)] = {"points": 0, "last_sign_in": today}
    
    data[str(user_id)]["points"] += 20  # 签到获得 20 积分
    data[str(user_id)]["last_sign_in"] = today
    
    _save_data(data)
    return True

def get_leaderboard():
    """获取积分排行榜，按积分降序排列"""
    data = _load_data()
    
    # 按积分排序，返回用户的 ID 和积分
    leaderboard = sorted(data.items(), key=lambda x: x[1]["points"], reverse=True)
    
    return leaderboard

def get_user_points(user_id):
    """获取用户当前积分"""
    data = _load_data()
    
    # 如果用户没有积分记录，则返回 0 积分
    if str(user_id) not in data:
        return 0
    
    return data[str(user_id)]["points"]

def add_message_points(user_id):
    """每次用户发言增加 1 积分"""
    data = _load_data()
    
    if str(user_id) not in data:
        data[str(user_id)] = {"points": 0, "last_sign_in": ""}
    
    data[str(user_id)]["points"] += 1  # 每条消息加 1 积分
    
    _save_data(data)