from telegram.ext import ApplicationBuilder
from config import Config
from commands import *

def register_handlers(application):
    # 注册基础命令
    application.add_handler(basic.start_handler)
    application.add_handler(basic.help_handler)
    
    # 注册管理命令
    application.add_handler(admin.admin_handler)
    application.add_handler(admin.ban_handler)
    application.add_handler(admin.unban_handler)
    
    # 注册信息命令
    application.add_handler(info.info_handler)

if __name__ == "__main__":
    # 初始化应用
    app = ApplicationBuilder().token(Config.BOT_TOKEN).build()
    
    # 注册处理器
    register_handlers(app)
    
    # 启动机器人
    print("🤖 Bot is running...")
    app.run_polling()