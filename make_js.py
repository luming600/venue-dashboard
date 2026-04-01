# -*- coding: utf-8 -*-
import json

base_dir = r"C:\Users\陆鸣\Desktop\杆杆响天梯赛"

# 读取JSON数据
with open(f"{base_dir}\\points_data.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# 写入JS文件
with open(f"{base_dir}\\points_data.js", 'w', encoding='utf-8') as f:
    f.write("const pointsData = ")
    json.dump(data, f, ensure_ascii=False)
    f.write(";")

print(f"已生成 points_data.js，共 {len(data)} 条记录")
