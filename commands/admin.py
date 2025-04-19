from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters
from config import Config
from utils.decorators import admin_required
from utils.helpers import get_user_info, send_log, sign_in, get_leaderboard, get_user_points
from datetime import datetime, timedelta

# 假设你有一个用户积分的数据结构
user_points = {}

@admin_required
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """封禁用户"""
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ 请回复要封禁的用户消息")
        return

    target_user = update.message.reply_to_message.from_user
    admin_user = update.effective_user

    try:
        await update.effective_chat.ban_member(
            user_id=target_user.id,
            until_date=datetime.now() + timedelta(days=1)
        )
        await update.message.reply_text(
            f"🚫 已封禁用户 {target_user.mention_html()}",
            parse_mode='HTML'
        )
        # ✅ 日志记录
        await send_log(
            f"🚫 封禁操作\n"
            f"👮‍♂️ 管理员: {admin_user.mention_html()} ({admin_user.id})\n"
            f"🙍‍♂️ 目标用户: {target_user.mention_html()} ({target_user.id})\n"
            f"⏰ 时长: 1天",
            parse_mode='HTML'  # 传递 HTML 格式
        )
    except Exception as e:
        await update.message.reply_text(f"❌ 封禁失败: {str(e)}")

@admin_required
async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """解封用户"""
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ 请回复要解封的用户消息")
        return

    target_user = update.message.reply_to_message.from_user
    admin_user = update.effective_user

    try:
        await update.effective_chat.unban_member(user_id=target_user.id)
        await update.message.reply_text(
            f"✅ 已解封用户 {target_user.mention_html()}",
            parse_mode='HTML'
        )
        # ✅ 日志记录
        await send_log(
            f"✅ 解封操作\n"
            f"👮‍♂️ 管理员: {admin_user.mention_html()} ({admin_user.id})\n"
            f"🙍‍♂️ 目标用户: {target_user.mention_html()} ({target_user.id})",
            parse_mode='HTML'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ 解封失败: {str(e)}")


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """管理员控制面板"""
    await update.message.reply_text("👮‍ 管理员控制面板功能开发中…")


@admin_required
async def sign_in_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """用户签到，获得20积分"""
    user_id = update.effective_user.id
    
    if sign_in(user_id):
        await update.message.reply_text(f"🎉 你今天成功签到并获得了20积分！")
    else:
        await update.message.reply_text(f"⚠️ 你今天已经签到过了！")

@admin_required
async def list_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """显示积分排行榜"""
    leaderboard = get_leaderboard()
    
    # 生成排行榜的消息
    leaderboard_message = "🏆 积分排行榜：\n\n"
    for idx, (user_id, data) in enumerate(leaderboard, 1):
        user = await update.bot.get_chat(user_id)
        leaderboard_message += f"{idx}. {user.first_name} ({user.username}) - {data['points']}积分\n"

    await update.message.reply_text(leaderboard_message)

@admin_required
async def check_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """查看用户个人积分"""
    user_id = update.effective_user.id
    points = get_user_points(user_id)
    await update.message.reply_text(f"你当前有 {points} 积分。")

# 监听消息，给用户增加积分
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理用户发来的消息"""
    user_id = update.effective_user.id
    message = update.message.text.lower()

    # 如果消息中包含 "签到"，执行签到
    if "签到" in message:
        await sign_in_user(update, context)
    else:
        # 其他消息增加积分
        add_message_points(user_id)
        await update.message.reply_text(f"当前积分：{get_user_points(user_id)}")

# 定义命令处理器
sign_in_handler = CommandHandler("签到", sign_in_user)
list_handler = CommandHandler("list", list_points)
check_points_handler = CommandHandler("积分", check_points)

# 监听所有非命令的文本消息
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)

# 注册所有处理器
handlers = [
    sign_in_handler,
    list_handler,
    check_points_handler,
    message_handler
]