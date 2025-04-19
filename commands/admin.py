from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from config import Config
from utils.decorators import admin_required
from utils.helpers import get_user_info, send_log
from datetime import datetime, timedelta  # ⚠️ 你忘记引入这两个了

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
            f"🚫 <b>封禁操作</b>\n"
            f"👮‍♂️ 管理员: {admin_user.mention_html()} ({admin_user.id})\n"
            f"🙍‍♂️ 目标用户: {target_user.mention_html()} ({target_user.id})\n"
            f"⏰ 时长: 1天",
            parse_mode='HTML'
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
            f"✅ <b>解封操作</b>\n"
            f"👮‍♂️ 管理员: {admin_user.mention_html()} ({admin_user.id})\n"
            f"🙍‍♂️ 目标用户: {target_user.mention_html()} ({target_user.id})",
            parse_mode='HTML'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ 解封失败: {str(e)}")

async def admin_panel(update: Update, context):
    await update.message.reply_text("👮‍ 管理员控制面板功能开发中…")


admin_handler = CommandHandler("admin", admin_panel)
ban_handler = CommandHandler("ban", ban_user)
unban_handler = CommandHandler("unban", unban_user)