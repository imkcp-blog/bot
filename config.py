import os

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "2046001110:AAEHL2OX91xpF-Lt4FY1_LqjTySplj9dFH8")
    ADMIN_IDS = [1910124860]  # 管理员ID列表
    WELCOME_MSG = "👋 欢迎新人！请阅读群规～"
    LOG_CHANNEL = -1001951108383  # 日志频道ID