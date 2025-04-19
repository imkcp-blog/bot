from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters
from config import Config
from utils.decorators import admin_required
from utils.helpers import sign_in, get_user_points, get_leaderboard, add_message_points  # 导入 sign_in
from datetime import datetime, timedelta
from utils.helpers import send_log

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
    """检测用户是否发送签到文本，并获得20积分"""
    user_id = update.effective_user.id
    
    # 检测用户消息是否包含“签到”关键词
    if "签到" in update.message.text or "sign in" in update.message.text:
        if sign_in(user_id):  # 调用 sign_in 函数
            await update.message.reply_text(f"🎉 你今天成功签到并获得了20积分！")
        else:
            await update.message.reply_text(f"⚠️ 你今天已经签到过了！")
    else:
        add_message_points(user_id)
        #await update.message.reply_text(f"你当前积分为：{get_user_points(user_id)}")
        
@admin_required
async def list_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """显示积分排行榜"""
    leaderboard = get_leaderboard()
    
    leaderboard_message = "🏆 积分排行榜：\n\n"
    for idx, (user_id, data) in enumerate(leaderboard, 1):
        # 使用 context.bot 获取机器人实例
        user = await context.bot.get_chat(user_id)
        leaderboard_message += f"{idx}. {user.first_name} ({user.username}) - {data['points']}积分\n"

    await update.message.reply_text(leaderboard_message)
@admin_required
# 监听消息，给用户增加积分
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理用户发来的消息"""
    user_id = update.effective_user.id
    message = update.message.text.lower()

    if "签到" in message or "sign in" in message:
        await sign_in_user(update, context)
    elif "积分" in message:
        # 可以根据需要在此返回积分，但如果不想让机器人回复积分，可以注释掉以下行
        points = get_user_points(user_id)
        await update.message.reply_text(f"你当前有 {points} 积分。")
    else:
        # 其他消息增加积分，后台记录
        add_message_points(user_id)
        # 不回复积分
        # await update.message.reply_text(f"当前积分：{get_user_points(user_id)}")

# 定义命令处理器
list_handler = CommandHandler("list", list_points)
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)

# 注册所有处理器
handlers = [
    list_handler,
    message_handler
]

ban_handler = CommandHandler("ban", ban_user)
unban_handler = CommandHandler("unban", unban_user)
