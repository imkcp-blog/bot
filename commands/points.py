import os
from datetime import datetime

# 在内存中保存用户积分信息
user_points = {}

# 签到获取积分
def get_points(user_id):
    # 初始化用户积分
    if user_id not in user_points:
        user_points[user_id] = {"points": 0, "last_sign_in": None}
    
    return user_points[user_id]

# 添加积分
def add_points(user_id, points):
    if user_id not in user_points:
        user_points[user_id] = {"points": 0, "last_sign_in": None}
    
    user_points[user_id]["points"] += points

# 签到功能：每天一次，获得20积分
def sign_in(user_id):
    user_data = get_points(user_id)
    last_sign_in = user_data["last_sign_in"]
    
    # 如果当天已经签到，不能重复签到
    if last_sign_in and last_sign_in.date() == datetime.now().date():
        return False  # 今日已签到
    
    # 更新签到时间并添加积分
    user_data["last_sign_in"] = datetime.now()
    add_points(user_id, 20)  # 每天签到获得20积分
    return True

# 获取积分排行
def get_leaderboard():
    # 排序并返回积分榜
    leaderboard = sorted(user_points.items(), key=lambda x: x[1]["points"], reverse=True)
    return leaderboard

# 获取某个用户的积分
def get_user_points(user_id):
    if user_id in user_points:
        return user_points[user_id]["points"]
    return 0
