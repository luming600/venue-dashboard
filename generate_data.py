# -*- coding: utf-8 -*-
import json
import random

# 正确的段位体系（从低到高）
ranks = [
    "沉稳青铜",
    "推杆白银", 
    "走位黄金",
    "加塞铂金",
    "校球钻石",
    "清台星耀",
    "最强杆王",
    "无双杆王",
    "荣耀杆王",
    "传奇杆王"
]

# 段位子等级
rank_levels = ["I", "II", "III", "IV"]

# 用户分层
segments = ["核心用户", "活跃用户", "潜力用户", "流失风险", "普通用户"]

# 省份城市
provinces_cities = {
    "湖北省": ["武汉市", "宜昌市", "襄阳市", "荆州市"],
    "广东省": ["广州市", "深圳市", "东莞市", "佛山市"],
    "河南省": ["郑州市", "洛阳市", "开封市", "南阳市"],
    "河北省": ["石家庄市", "唐山市", "保定市"],
    "辽宁省": ["沈阳市", "大连市", "鞍山市"],
    "江苏省": ["南京市", "苏州市", "无锡市", "常州市"],
    "浙江省": ["杭州市", "宁波市", "温州市"],
    "山东省": ["济南市", "青岛市", "烟台市"],
    "四川省": ["成都市", "绵阳市", "德阳市"],
    "陕西省": ["西安市", "咸阳市", "宝鸡市"]
}

venues = [
    "乔氏台球俱乐部", "台球帝国", "星际台球", "九球台球俱乐部",
    "名仕台球", "金爵台球俱乐部", "豪庭台球俱乐部", "巅峰台球",
    "风云台球会所", "壹品台球", "乌达区慢时空台球厅", "武昌万象城八楼名仕台球",
    "伯爵台球会所", "天工台球城", "王者台球俱乐部", "绅士台球俱乐部",
    "冠军台球馆", "星云台球", "黑八台球城", "星牌台球会所"
]

surnames = ["张", "王", "李", "赵", "刘", "陈", "杨", "黄", "周", "吴", "徐", "孙", "马", "朱", "胡", "郭", "何", "高", "林", "罗", "郑", "梁", "谢", "宋", "唐", "许", "韩", "冯", "邓", "曹", "彭", "曾", "萧", "田", "董", "袁", "潘", "于", "蒋", "蔡", "余", "杜", "叶", "程", "苏", "魏", "吕", "丁", "任", "沈", "姚", "卢", "姜", "崔", "钟", "谭", "陆", "汪", "范", "金", "石", "廖", "贾", "夏", "韦", "付", "方", "白", "邹", "孟", "熊", "秦", "邱", "江", "尹", "薛", "闫", "段", "雷", "侯", "龙", "史", "陶", "黎", "贺", "顾", "毛", "郝", "龚", "邵", "万", "钱", "严", "覃", "武", "戴", "莫", "孔", "向", "汤"]

def generate_name():
    return random.choice(surnames) + random.choice(["伟", "芳", "娜", "秀英", "敏", "静", "丽", "强", "磊", "军", "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀兰", "霞", "平", "刚", "桂英", "玉兰", "英", "梅", "婷", "华", "玲", "飞", "宇", "浩", "凯", "峰", "龙", "博", "阳", "斌", "辉", "鹏", "旭", "建", "志", "永", "林", "云", "帆", "航", "一", "二", "三"])

def generate_users(count=10000):
    users = []
    rank_dist = {}
    
    for i in range(count):
        user_id = str(1000 + i)
        
        # 段位分布：低段位多，高段位少
        rank_weights = [25, 20, 20, 15, 10, 5, 3, 1.5, 0.4, 0.1]  # 权重
        rank_idx = random.choices(range(10), weights=rank_weights)[0]
        base_rank = ranks[rank_idx]
        
        # 只有黄金及以上才有子等级，青铜白银没有
        if rank_idx >= 2:
            level = random.choice(rank_levels)
            rank = f"{base_rank} {level}"
        else:
            rank = base_rank
            
        rank_dist[base_rank] = rank_dist.get(base_rank, 0) + 1
        
        # 积分根据段位计算
        base_score = (rank_idx + 1) * 800 + random.randint(0, 500)
        
        # 场次
        games = random.randint(10, 300)
        
        # 胜率（高段位胜率略高）
        win_rate = random.randint(35, 75) + rank_idx * 2
        win_rate = min(win_rate, 95)
        
        # 连胜
        streak = random.randint(0, 12) if random.random() > 0.7 else 0
        
        # 高级统计（台球专业数据）
        # 炸清数：开球后直接清台（高手更多）
        break_clears = random.randint(0, max(1, games // 10)) if rank_idx >= 5 else random.randint(0, max(1, games // 20))
        # 接清数：对手开球后自己清台
        run_clears = random.randint(0, max(1, games // 8)) if rank_idx >= 5 else random.randint(0, max(1, games // 15))
        # 大金数：特殊高分记录
        big_gold = random.randint(0, max(1, games // 15)) if rank_idx >= 6 else random.randint(0, max(1, games // 25))
        # 小金数：特殊记录
        small_gold = random.randint(0, max(1, games // 12)) if rank_idx >= 5 else random.randint(0, max(1, games // 20))
        # 双赛点胜率：赛点局的胜率
        double_match_point_win_rate = min(95, max(30, win_rate + random.randint(-10, 15)))
        
        # 段位变化（正数为升段，负数为降段）
        rank_change = random.randint(-3, 5) if random.random() > 0.3 else 0
        
        # 最近活跃天数（用于RFM分层）
        last_active_days = random.choices(
            [0, 1, 2, 3, 5, 7, 10, 15, 20, 30, 45, 60],
            weights=[5, 10, 10, 10, 10, 15, 10, 10, 8, 5, 4, 3]
        )[0]
        
        # 省份城市
        province = random.choice(list(provinces_cities.keys()))
        city = random.choice(provinces_cities[province])
        
        # 球馆
        venue = random.choice(venues)
        
        # 分层 - 基于RFM模型
        # 核心用户: 近7天活跃 + 场次≥50 + 胜率≥70%
        # 活跃用户: 近15天活跃 + 场次≥30
        # 潜力用户: 近30天活跃 + 胜率≥60% + 场次<30
        # 流失风险: 近30天无活动 + 历史场次≥30
        # 普通用户: 默认
        
        if last_active_days <= 7 and games >= 50 and win_rate >= 70:
            segment = "核心用户"
        elif last_active_days <= 15 and games >= 30:
            segment = "活跃用户"
        elif last_active_days <= 30 and win_rate >= 60 and games < 30:
            segment = "潜力用户"
        elif last_active_days > 30 and games >= 30:
            segment = "流失风险"
        else:
            segment = "普通用户"
        
        # 姓名
        if random.random() > 0.85:
            name = f"用户{user_id}"
        elif random.random() > 0.95:
            name = f"King{random.randint(100, 999)}"
        else:
            name = generate_name()
        
        users.append({
            "id": user_id,
            "name": name,
            "province": province,
            "city": city,
            "venue": venue,
            "rank": rank,
            "score": base_score,
            "games": games,
            "winRate": win_rate,
            "streak": streak,
            "segment": segment,
            "breakClears": break_clears,
            "runClears": run_clears,
            "bigGold": big_gold,
            "smallGold": small_gold,
            "doubleMatchPointWinRate": double_match_point_win_rate,
            "rankChange": rank_change
        })
    
    return users, rank_dist

# 生成数据
users, rank_dist = generate_users(10000)

# 统计
total_games = sum(u["games"] for u in users)
active_users = len([u for u in users if u["segment"] in ["核心用户", "活跃用户"]])
avg_win_rate = sum(u["winRate"] for u in users) / len(users)

# 省份分布
province_dist = {}
for u in users:
    province_dist[u["province"]] = province_dist.get(u["province"], 0) + 1
provinces_sorted = sorted(province_dist.items(), key=lambda x: -x[1])[:10]

# 城市分布
city_dist = {}
for u in users:
    city_dist[u["city"]] = city_dist.get(u["city"], 0) + 1
cities_sorted = sorted(city_dist.items(), key=lambda x: -x[1])[:15]

# 球馆分布
venue_dist = {}
for u in users:
    venue_dist[u["venue"]] = venue_dist.get(u["venue"], 0) + 1
venues_sorted = sorted(venue_dist.items(), key=lambda x: -x[1])[:10]

# 分层统计
segment_dist = {}
for u in users:
    segment_dist[u["segment"]] = segment_dist.get(u["segment"], 0) + 1

# 对局模式分布（抢5、抢7、抢9、抢11、抢13）
# 抢5: 新手/休闲玩家多
# 抢7: 常规比赛
# 抢9: 正式比赛（17局9胜）
# 抢11: 高级别比赛
# 抢13: 冠军赛/决赛
match_modes = [
    {"name": "抢5", "value": random.randint(80000, 120000), "desc": "先赢5局"},
    {"name": "抢7", "value": random.randint(150000, 200000), "desc": "先赢7局"},
    {"name": "抢9", "value": random.randint(300000, 400000), "desc": "17局9胜"},
    {"name": "抢11", "value": random.randint(100000, 150000), "desc": "先赢11局"},
    {"name": "抢13", "value": random.randint(30000, 60000), "desc": "先赢13局"},
    {"name": "其它", "value": random.randint(20000, 40000), "desc": "其他赛制"}
]

# 积分兑换率数据
points_exchange = {
    "totalPoints": sum(u["score"] for u in users),  # 总积分
    "exchangedPoints": random.randint(200000, 400000),  # 已兑换积分
    "exchangeRate": round(random.uniform(15, 35), 1),  # 兑换率%
    "exchangeCount": random.randint(500, 1500),  # 兑换次数
    "avgExchangeAmount": random.randint(150, 300),  # 平均兑换金额
    "topExchangeItems": [  # 热门兑换商品
        {"name": "球杆", "count": random.randint(50, 150), "points": 5000},
        {"name": "台球", "count": random.randint(80, 200), "points": 2000},
        {"name": "手套", "count": random.randint(100, 250), "points": 800},
        {"name": "巧粉", "count": random.randint(150, 300), "points": 300},
        {"name": "会员卡", "count": random.randint(30, 100), "points": 10000}
    ]
}

# 生成玩家排名数据（按日/周/月/季度）
def generate_rankings(users, period_name, limit=20):
    """生成指定周期的排名数据"""
    # 随机调整一些数据模拟不同周期的变化
    ranking_users = sorted(users, key=lambda x: -x["score"])[:limit*2]
    
    rankings = []
    for i, u in enumerate(ranking_users[:limit]):
        rankings.append({
            "rank": i + 1,
            "userId": u["id"],
            "name": u["name"],
            "games": u["games"] + random.randint(-5, 10),
            "score": u["score"] + random.randint(-100, 200),
            "winRate": u["winRate"] + random.randint(-3, 5),
            "streak": u["streak"],
            "rankChange": u["rankChange"],
            "breakClears": u["breakClears"] + random.randint(-1, 3),
            "runClears": u["runClears"] + random.randint(-1, 3),
            "bigGold": u["bigGold"] + random.randint(0, 2),
            "smallGold": u["smallGold"] + random.randint(0, 2),
            "doubleMatchPointWinRate": u["doubleMatchPointWinRate"] + random.randint(-5, 5)
        })
    
    return rankings

player_rankings = {
    "daily": generate_rankings(users, "daily", 20),
    "weekly": generate_rankings(users, "weekly", 20),
    "monthly": generate_rankings(users, "monthly", 20),
    "quarterly": generate_rankings(users, "quarterly", 20),
    "yearly": generate_rankings(users, "yearly", 20),
    "all": generate_rankings(users, "all", 20)
}

# 构建数据对象
data = {
    "stats": {
        "totalUsers": len(users),
        "activeUsers": active_users,
        "totalGames": total_games,
        "avgWinRate": round(avg_win_rate, 1),
        "totalVenues": len(venues),
        "maxStreak": max(u["streak"] for u in users)
    },
    "rankDist": [{"name": r, "value": rank_dist.get(r, 0), "color": c} for r, c in zip(ranks, ["#CD7F32", "#C0C0C0", "#FFD700", "#E6E6FA", "#00CED1", "#9932CC", "#FF4500", "#8B0000", "#FFD700", "#FFD700"])],
    "segments": [{"name": s, "value": segment_dist.get(s, 0), "color": c} for s, c in zip(segments, ["#FFD700", "#00C853", "#2196F3", "#FF9800", "#9E9E9E"])],
    "matchModes": match_modes,
    "pointsExchange": points_exchange,
    "playerRankings": player_rankings,
    "provinces": provinces_sorted,
    "cities": cities_sorted,
    "venues": venues_sorted,
    "venueWinRates": [[v[0], round(50 + random.random() * 10, 1)] for v in venues_sorted],
    "dailyTrend": [[f"03-{str(i+1).zfill(2)}", random.randint(150, 280), random.randint(30, 80), random.randint(400, 700)] for i in range(31)],
    "weeklyTrend": [[f"第{i+1}周", random.randint(300, 600), random.randint(3000, 6500), random.randint(500, 1100)] for i in range(12)],
    "topUsers": sorted(users, key=lambda x: -x["score"])[:10],
    "allUsers": users
}

# 写入文件
js_content = f"""// 自动生成的测试数据 - {len(users)}个用户
const demoData = {json.dumps(data, ensure_ascii=False, indent=2)};
"""

with open("demo_data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"生成完成: {len(users)}个用户")
print(f"段位分布: {rank_dist}")
