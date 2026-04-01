import random
import json
from datetime import datetime, timedelta

# 设置随机种子保证可重复
random.seed(42)

# 基础数据配置
PROVINCES = [
    ("湖北省", 3200), ("广东省", 1200), ("河南省", 980), ("河北省", 850),
    ("辽宁省", 720), ("江苏省", 580), ("浙江省", 450), ("山东省", 380),
    ("四川省", 320), ("陕西省", 280), ("湖南省", 220), ("安徽省", 180),
    ("福建省", 150), ("江西省", 120), ("云南省", 80)
]

CITIES = {
    "湖北省": [("武汉市", 2800), ("宜昌市", 200), ("襄阳市", 150), ("荆州市", 50)],
    "广东省": [("广州市", 650), ("深圳市", 320), ("东莞市", 150), ("佛山市", 80)],
    "河南省": [("郑州市", 580), ("洛阳市", 200), ("开封市", 120), ("新乡市", 80)],
    "河北省": [("石家庄市", 420), ("唐山市", 200), ("保定市", 150), ("沧州市", 80)],
    "辽宁省": [("沈阳市", 380), ("大连市", 220), ("鞍山市", 80), ("抚顺市", 40)],
    "江苏省": [("南京市", 280), ("苏州市", 180), ("无锡市", 80), ("常州市", 40)],
    "浙江省": [("杭州市", 220), ("宁波市", 120), ("温州市", 80), ("嘉兴市", 30)],
    "山东省": [("济南市", 150), ("青岛市", 120), ("烟台市", 60), ("潍坊市", 50)],
    "四川省": [("成都市", 220), ("绵阳市", 60), ("德阳市", 30), ("宜宾市", 10)],
    "陕西省": [("西安市", 200), ("咸阳市", 50), ("宝鸡市", 20), ("渭南市", 10)],
    "湖南省": [("长沙市", 120), ("株洲市", 50), ("湘潭市", 30), ("岳阳市", 20)],
    "安徽省": [("合肥市", 100), ("芜湖市", 40), ("蚌埠市", 25), ("淮南市", 15)],
    "福建省": [("福州市", 60), ("厦门市", 50), ("泉州市", 25), ("漳州市", 15)],
    "江西省": [("南昌市", 60), ("九江市", 30), ("景德镇市", 18), ("萍乡市", 12)],
    "云南省": [("昆明市", 50), ("大理市", 15), ("丽江市", 10), ("曲靖市", 5)]
}

VENUES = [
    "乔氏台球俱乐部", "龙禧台球俱乐部", "星云台球", "燃·竞技台球CLUB",
    "V8禁区台球棋牌俱乐部", "名仕台球", "壹品台球", "石河子康溪盛世台球俱乐部",
    "乌达区慢时空台球厅", "武昌万象城八楼名仕台球", "星牌台球会所", "精英台球俱乐部",
    "天工台球城", "金爵台球俱乐部", "传奇台球会所", "王者台球俱乐部",
    "巅峰台球", "荣耀台球俱乐部", "冠军台球馆", "高手台球俱乐部",
    "名爵台球", "伯爵台球会所", "绅士台球俱乐部", "黑八台球城",
    "九球台球俱乐部", "斯诺克台球馆", "台球世界", "台球帝国",
    "星际台球", "银河台球俱乐部", "风云台球会所", "豪庭台球俱乐部"
]

# 段位配置
RANKS = [
    ("最强杆王", 50, 2000, 10000),      # 段位名, 人数, 最低积分, 最高积分
    ("校球钻石 I", 80, 1500, 2500),
    ("校球钻石 II", 120, 1200, 1800),
    ("校球钻石 III", 200, 1000, 1500),
    ("校球钻石 IV", 250, 800, 1200),
    ("加塞铂金 I", 350, 600, 900),
    ("加塞铂金 II", 500, 500, 750),
    ("加塞铂金 III", 650, 400, 600),
    ("加塞铂金 IV", 800, 300, 500),
    ("走位黄金 I", 900, 200, 400),
    ("走位黄金 II", 1100, 150, 300),
    ("走位黄金 III", 1300, 100, 250),
    ("走位黄金 IV", 1500, 80, 200),
    ("翻袋白银 I", 1000, 50, 120),
    ("翻袋白银 II", 800, 30, 80),
    ("翻袋白银 III", 600, 20, 60),
    ("翻袋白银 IV", 500, 10, 50),
    ("清台青铜 I", 300, 0, 30),
    ("清台青铜 II", 200, 0, 20),
    ("清台青铜 III", 150, 0, 15),
    ("清台青铜 IV", 100, 0, 10)
]

# 姓氏和名字
SURNAMES = ["王", "李", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴", "徐", "孙", "胡", "朱", "高",
            "林", "何", "郭", "马", "罗", "梁", "宋", "郑", "谢", "韩", "唐", "冯", "于", "董", "萧",
            "程", "曹", "袁", "邓", "许", "傅", "沈", "曾", "彭", "吕", "苏", "卢", "蒋", "蔡", "贾"]

GIVEN_NAMES = ["伟", "芳", "娜", "秀英", "敏", "静", "丽", "强", "磊", "军", "洋", "勇", "艳", "杰", "娟",
               "涛", "明", "超", "秀兰", "霞", "平", "刚", "桂英", "华", "飞", "玲", "英", "梅", "鹏", "斌",
               "俊", "辉", "丹", "萍", "建军", "浩", "宇", "婷", "凯", "健", "琳", "鑫", "雪", "志强", "旭",
               "雷", "亮", "波", "红", "云", "峰", "莉", "颖", "欣", "昊", "文", "杰", "豪", "轩", "博"]

NICKNAME_PREFIX = ["台球", "黑八", "斯诺克", "球王", "高手", "传奇", "王者", "冠军", "精英", "大神",
                   "杆法", "走位", "加塞", "翻袋", "清台", "进球", "高手", "达人", "专家", "大师"]

NICKNAME_SUFFIX = ["王子", "达人", "高手", "王者", "传奇", "大神", "专家", "大师", "之星", "新秀",
                   "小王子", "小霸王", "战神", "王者", "精英", "天王", "冠军", "第一", "霸主", "王者"]

def generate_nickname(user_id):
    """生成用户昵称"""
    style = random.choice([1, 2, 3, 4, 5])

    if style == 1:
        # 真实姓名风格
        surname = random.choice(SURNAMES)
        given = random.choice(GIVEN_NAMES)
        return f"{surname}{given}"
    elif style == 2:
        # 台球相关昵称
        prefix = random.choice(NICKNAME_PREFIX)
        suffix = random.choice(NICKNAME_SUFFIX)
        return f"{prefix}{suffix}"
    elif style == 3:
        # 字母+数字
        letters = random.choice(["GGX", "King", "Pro", "Master", "Player", "Billiard", "Cue", "Pool"])
        num = random.randint(1, 999)
        return f"{letters}{num}"
    elif style == 4:
        # 中文+符号
        words = random.choice(["台球迷", "热爱台球", "黑八控", "清台王", "杆杆响", "一杆清",
                               "台球爱好者", "球房常客", "台球达人", "精准走位"])
        return words
    else:
        # 随机混合
        return f"用户{user_id}"

def generate_users(count=10000):
    """生成用户数据"""
    users = []

    # 按段位分配用户
    rank_users = []
    for rank_name, rank_count, min_score, max_score in RANKS:
        rank_users.extend([(rank_name, min_score, max_score)] * rank_count)

    # 补齐或截断到指定数量
    if len(rank_users) < count:
        for _ in range(count - len(rank_users)):
            rank_users.append(("清台青铜 IV", 0, 10))
    rank_users = rank_users[:count]
    random.shuffle(rank_users)

    # 按省份分配城市和球馆
    province_city_map = {}
    for province, _ in PROVINCES:
        cities = CITIES.get(province, [(province.replace("省", "市"), 100)])
        province_city_map[province] = cities

    # 生成每个用户
    for i in range(count):
        user_id = str(1000 + i)
        rank_name, min_score, max_score = rank_users[i]

        # 选择省份（按权重）
        total_weight = sum(w for _, w in PROVINCES)
        r = random.randint(1, total_weight)
        cumulative = 0
        selected_province = PROVINCES[0][0]
        for province, weight in PROVINCES:
            cumulative += weight
            if r <= cumulative:
                selected_province = province
                break

        # 选择城市
        cities = province_city_map[selected_province]
        city_total = sum(w for _, w in cities)
        r = random.randint(1, city_total)
        cumulative = 0
        selected_city = cities[0][0]
        for city, weight in cities:
            cumulative += weight
            if r <= cumulative:
                selected_city = city
                break

        # 选择球馆
        venue = random.choice(VENUES)

        # 生成积分
        score = random.randint(min_score, max_score)

        # 生成场次（段位越高场次越多）
        if "杆王" in rank_name:
            games = random.randint(80, 300)
        elif "钻石" in rank_name:
            games = random.randint(50, 200)
        elif "铂金" in rank_name:
            games = random.randint(30, 150)
        elif "黄金" in rank_name:
            games = random.randint(15, 100)
        elif "白银" in rank_name:
            games = random.randint(5, 60)
        else:
            games = random.randint(1, 40)

        # 生成胜率（段位越高胜率越高，但有波动）
        base_win_rate = {
            "杆王": 75, "钻石": 68, "铂金": 60, "黄金": 52, "白银": 45, "青铜": 38
        }
        for key, val in base_win_rate.items():
            if key in rank_name:
                win_rate = min(95, max(20, val + random.randint(-15, 15)))
                break

        # 生成连胜
        streak = random.randint(0, max(1, int((win_rate - 30) / 5)))

        # 计算用户分层
        if win_rate >= 70 and games >= 50:
            segment = "核心用户"
        elif games >= 30:
            segment = "活跃用户"
        elif win_rate >= 60 and games >= 10:
            segment = "潜力用户"
        elif games >= 20 and win_rate < 45:
            segment = "流失风险"
        else:
            segment = "普通用户"

        # 最后活跃时间
        days_ago = random.randint(0, 60) if segment != "流失风险" else random.randint(30, 90)
        last_active = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")

        user = {
            "id": user_id,
            "name": generate_nickname(user_id),
            "province": selected_province,
            "city": selected_city,
            "venue": venue,
            "rank": rank_name,
            "score": score,
            "games": games,
            "winRate": round(win_rate, 1),
            "streak": streak,
            "segment": segment,
            "lastActive": last_active
        }
        users.append(user)

    return users

def calculate_stats(users):
    """计算统计数据"""
    total_users = len(users)

    # 月活跃用户（近30天）
    active_threshold = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    active_users = len([u for u in users if u["lastActive"] >= active_threshold])

    # 总场次
    total_games = sum(u["games"] for u in users)

    # 平均胜率
    avg_win_rate = round(sum(u["winRate"] for u in users) / total_users, 1)

    # 球馆数
    venues = len(set(u["venue"] for u in users))

    # 最高连胜
    max_streak = max(u["streak"] for u in users)

    return {
        "totalUsers": total_users,
        "activeUsers": active_users,
        "totalGames": total_games,
        "avgWinRate": avg_win_rate,
        "totalVenues": venues,
        "maxStreak": max_streak
    }

def calculate_rank_distribution(users):
    """计算段位分布"""
    rank_counts = {}
    for u in users:
        # 简化段位名
        if "杆王" in u["rank"]:
            key = "最强杆王"
        elif "钻石" in u["rank"]:
            key = "校球钻石"
        elif "铂金" in u["rank"]:
            key = "加塞铂金"
        elif "黄金" in u["rank"]:
            key = "走位黄金"
        elif "白银" in u["rank"]:
            key = "翻袋白银"
        else:
            key = "清台青铜"
        rank_counts[key] = rank_counts.get(key, 0) + 1

    colors = {
        "最强杆王": "#FFD700",
        "校球钻石": "#00CED1",
        "加塞铂金": "#E6E6FA",
        "走位黄金": "#FFD700",
        "翻袋白银": "#C0C0C0",
        "清台青铜": "#CD853F"
    }

    return [{"name": k, "value": v, "color": colors[k]} for k, v in sorted(rank_counts.items(), key=lambda x: x[1], reverse=True)]

def calculate_segments(users):
    """计算用户分层"""
    segment_counts = {}
    for u in users:
        segment_counts[u["segment"]] = segment_counts.get(u["segment"], 0) + 1

    colors = {
        "核心用户": "#FFD700",
        "活跃用户": "#00C853",
        "潜力用户": "#2196F3",
        "流失风险": "#FF9800",
        "普通用户": "#9E9E9E"
    }

    order = ["核心用户", "活跃用户", "潜力用户", "流失风险", "普通用户"]
    return [{"name": seg, "value": segment_counts.get(seg, 0), "color": colors[seg]} for seg in order]

def calculate_province_distribution(users):
    """计算省份分布"""
    province_counts = {}
    for u in users:
        province_counts[u["province"]] = province_counts.get(u["province"], 0) + 1

    sorted_provinces = sorted(province_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    return [[p, c] for p, c in sorted_provinces]

def calculate_city_distribution(users):
    """计算城市分布"""
    city_counts = {}
    for u in users:
        city_counts[u["city"]] = city_counts.get(u["city"], 0) + 1

    sorted_cities = sorted(city_counts.items(), key=lambda x: x[1], reverse=True)[:15]
    return [[c, cnt] for c, cnt in sorted_cities]

def calculate_venue_activity(users):
    """计算球馆活跃度"""
    venue_counts = {}
    for u in users:
        venue_counts[u["venue"]] = venue_counts.get(u["venue"], 0) + 1

    sorted_venues = sorted(venue_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    return [[v, c] for v, c in sorted_venues]

def calculate_venue_winrate(users):
    """计算球馆平均胜率"""
    venue_winrates = {}
    venue_counts = {}
    for u in users:
        venue_winrates[u["venue"]] = venue_winrates.get(u["venue"], 0) + u["winRate"]
        venue_counts[u["venue"]] = venue_counts.get(u["venue"], 0) + 1

    avg_winrates = {v: round(venue_winrates[v] / venue_counts[v], 1) for v in venue_winrates}
    sorted_venues = sorted(avg_winrates.items(), key=lambda x: x[1], reverse=True)[:10]
    return [[v, wr] for v, wr in sorted_venues]

def generate_daily_trend():
    """生成每日趋势数据"""
    trend = []
    base_active = 180
    base_new = 45
    base_games = 450

    for i in range(30):
        date = (datetime.now() - timedelta(days=29-i)).strftime("%m-%d")
        # 添加增长趋势和随机波动
        growth = 1 + i * 0.015
        active = int(base_active * growth * random.uniform(0.85, 1.15))
        new = int(base_new * growth * random.uniform(0.7, 1.3))
        games = int(base_games * growth * random.uniform(0.8, 1.2))

        trend.append([date, active, new, games])

    return trend

def generate_weekly_trend():
    """生成每周趋势数据"""
    trend = []
    base_new = 350
    base_games = 3200
    base_active = 550

    for i in range(12):
        week = f"第{i+1}周"
        growth = 1 + i * 0.08
        new_users = int(base_new * growth * random.uniform(0.85, 1.15))
        games = int(base_games * growth * random.uniform(0.9, 1.1))
        active = int(base_active * growth * random.uniform(0.85, 1.15))

        trend.append([week, new_users, games, active])

    return trend

def get_top_users(users, n=50):
    """获取高价值用户Top N"""
    # 按积分和胜率综合排序
    sorted_users = sorted(users, key=lambda u: (u["score"] * 0.5 + u["winRate"] * 10 + u["games"] * 2), reverse=True)
    return sorted_users[:n]

def generate_javascript_data(users):
    """生成JavaScript数据格式"""
    stats = calculate_stats(users)
    rank_dist = calculate_rank_distribution(users)
    segments = calculate_segments(users)
    provinces = calculate_province_distribution(users)
    cities = calculate_city_distribution(users)
    venues = calculate_venue_activity(users)
    venue_winrates = calculate_venue_winrate(users)
    daily_trend = generate_daily_trend()
    weekly_trend = generate_weekly_trend()
    top_users = get_top_users(users, 50)

    js_data = f"""// 自动生成的测试数据 - {len(users)}个用户
const demoData = {{
    stats: {{
        totalUsers: {stats['totalUsers']},
        activeUsers: {stats['activeUsers']},
        totalGames: {stats['totalGames']},
        avgWinRate: {stats['avgWinRate']},
        totalVenues: {stats['totalVenues']},
        maxStreak: {stats['maxStreak']}
    }},
    rankDist: {json.dumps(rank_dist, ensure_ascii=False)},
    segments: {json.dumps(segments, ensure_ascii=False)},
    provinces: {json.dumps(provinces, ensure_ascii=False)},
    cities: {json.dumps(cities, ensure_ascii=False)},
    venues: {json.dumps(venues, ensure_ascii=False)},
    venueWinRates: {json.dumps(venue_winrates, ensure_ascii=False)},
    dailyTrend: {json.dumps(daily_trend, ensure_ascii=False)},
    weeklyTrend: {json.dumps(weekly_trend, ensure_ascii=False)},
    topUsers: {json.dumps([{
        'id': u['id'],
        'name': u['name'],
        'province': u['province'],
        'city': u['city'],
        'venue': u['venue'],
        'rank': u['rank'],
        'score': u['score'],
        'games': u['games'],
        'winRate': u['winRate'],
        'streak': u['streak']
    } for u in top_users], ensure_ascii=False)},
    allUsers: {json.dumps([{
        'id': u['id'],
        'name': u['name'],
        'province': u['province'],
        'city': u['city'],
        'venue': u['venue'],
        'rank': u['rank'],
        'score': u['score'],
        'games': u['games'],
        'winRate': u['winRate'],
        'segment': u['segment']
    } for u in users], ensure_ascii=False)}
}};
"""
    return js_data

if __name__ == "__main__":
    print("正在生成10000个用户的测试数据...")
    users = generate_users(10000)

    print("生成JavaScript数据...")
    js_data = generate_javascript_data(users)

    # 保存到文件
    with open("demo_data.js", "w", encoding="utf-8") as f:
        f.write(js_data)

    print(f"完成！已生成 {len(users)} 个用户的测试数据")
    print(f"统计数据：")
    stats = calculate_stats(users)
    for key, value in stats.items():
        print(f"  - {key}: {value}")
