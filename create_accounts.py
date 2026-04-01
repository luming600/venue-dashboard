# -*- coding: utf-8 -*-
import json

# 球馆账号映射
venue_accounts = {
    "qiaoshi": {"password": "qiaoshi123", "venue": "乔氏台球俱乐部"},
    "taiqiu": {"password": "taiqiu123", "venue": "台球帝国"},
    "xingji": {"password": "xingji123", "venue": "星际台球"},
    "jiuqiu": {"password": "jiuqiu123", "venue": "九球台球俱乐部"},
    "mingshi": {"password": "mingshi123", "venue": "名仕台球"},
    "jinzue": {"password": "jinzue123", "venue": "金爵台球俱乐部"},
    "haoting": {"password": "haoting123", "venue": "豪庭台球俱乐部"},
    "dianfeng": {"password": "dianfeng123", "venue": "巅峰台球"},
    "fengyun": {"password": "fengyun123", "venue": "风云台球会所"},
    "yipin": {"password": "yipin123", "venue": "壹品台球"},
    "manishikong": {"password": "manishikong123", "venue": "乌达区慢时空台球厅"},
    "wuchang": {"password": "wuchang123", "venue": "武昌万象城八楼名仕台球"},
    "bojue": {"password": "bojue123", "venue": "伯爵台球会所"},
    "tiangong": {"password": "tiangong123", "venue": "天工台球城"},
    "wangzhe": {"password": "wangzhe123", "venue": "王者台球俱乐部"},
    "shenshi": {"password": "shenshi123", "venue": "绅士台球俱乐部"},
    "guanjun": {"password": "guanjun123", "venue": "冠军台球馆"},
    "xingyun": {"password": "xingyun123", "venue": "星云台球"},
    "heiba": {"password": "heiba123", "venue": "黑八台球城"},
    "xingpai": {"password": "xingpai123", "venue": "星牌台球会所"}
}

# 生成账号数据的JS
accounts_js = "const venueAccounts = " + json.dumps(venue_accounts, ensure_ascii=False, indent=2) + ";\n"

print("球馆账号列表：")
for username, info in venue_accounts.items():
    print(f"  账号: {username:15} 密码: {info['password']:15} 球馆: {info['venue']}")

print(f"\n共 {len(venue_accounts)} 个球馆账号")

# 保存账号数据
with open("venue_accounts.js", "w", encoding="utf-8") as f:
    f.write(accounts_js)
