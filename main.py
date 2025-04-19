import asyncio
import logging

from telegram import BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from config import Config
from commands import start_command, basic, admin, info
from commands.admin import handlers as admin_handlers

# 日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def set_bot_commands(application: Application):
    """同步地设置机器人命令列表"""
    commands = [
        BotCommand("start", "启动机器人"),
        BotCommand("help", "显示帮助信息"),
        BotCommand("list", "显示积分排行榜"),
        BotCommand("ban", "封禁用户"),
        BotCommand("unban", "解封用户"),
        BotCommand("info", "显示机器人信息"),
    ]
    # set_my_commands 是 async，需要 run_until_complete 调用
    asyncio.get_event_loop().run_until_complete(
        application.bot.set_my_commands(commands)
    )
    logger.info("Bot commands have been set.")

async def help_command(update, context: ContextTypes.DEFAULT_TYPE):
    """/help 命令处理，动态读取当前命令并展示"""
    current = await context.bot.get_my_commands()
    help_text = "以下是我支持的命令：\n" + "\n".join(
        f"/{cmd.command} - {cmd.description}" for cmd in current
    )
    await update.message.reply_text(help_text)

async def error_handler(update, context: ContextTypes.DEFAULT_TYPE):
    """全局异常处理"""
    logger.error(f"Update {update} caused error: {context.error}")

def register_handlers(app: Application):
    # 基础命令
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(basic.start_handler)
    app.add_handler(basic.help_handler)

    # 管理命令
    app.add_handler(admin.ban_handler)
    app.add_handler(admin.unban_handler)

    # info 命令
    app.add_handler(info.info_handler)

    # admin 模块里其他的处理器列表
    for handler in admin_handlers:
        app.add_handler(handler)

def main():
    # 1. 构建应用
    application = Application.builder().token(Config.BOT_TOKEN).build()

    # 2. 添加全局错误处理
    application.add_error_handler(error_handler)

    # 3. 同步设置机器人命令
    set_bot_commands(application)

    # 4. 注册所有命令和消息处理器
    register_handlers(application)

    # 5. 启动轮询（blocking）
    logger.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
