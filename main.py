from telegram.ext import Application, MessageHandler, filters
from config import Config
from commands import basic, admin, info  # 添加正确的导入
from admin import sign_in_handler, list_handler, check_points_handler
from utils.points import add_points  # 引入增加积分的功能

# 消息处理函数，监听所有非命令的文本消息并增加积分
async def message_handler(update, context):
    user_id = update.effective_user.id
    add_points(user_id, 1)  # 每发一条消息，增加1积分
    if update.effective_user.is_bot:
        return  # 如果是机器人发送的消息，忽略


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
    
    # 注册积分相关命令
    application.add_handler(sign_in_handler)
    application.add_handler(list_handler)
    application.add_handler(check_points_handler)

    # 注册消息处理器，监听所有文本消息（非命令），并增加积分
    message_handler_instance = MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
    application.add_handler(message_handler_instance)


if __name__ == "__main__":
    # 初始化应用
    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    # 注册处理器
    register_handlers(application)
    
    # 启动机器人
    print("🤖 Bot is running...")
    application.run_polling()
