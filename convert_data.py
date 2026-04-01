# -*- coding: utf-8 -*-
import pandas as pd
import json
import os
import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def convert_to_serializable(obj):
    """转换数据为可JSON序列化的格式"""
    if isinstance(obj, (pd.Timestamp, np.datetime64)):
        return str(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif pd.isna(obj):
        return None
    return obj

base_dir = r"C:\Users\陆鸣\Desktop\杆杆响天梯赛"

# 转换积分流水数据
points_file = os.path.join(base_dir, "用户积分流水 (1).xls")
if os.path.exists(points_file):
    print(f"读取: {points_file}")
    df = pd.read_excel(points_file)
    print(f"共 {len(df)} 条记录")
    print(f"列名: {list(df.columns)}")
    
    # 转换为列表，处理特殊类型
    data = []
    for _, row in df.iterrows():
        record = {k: convert_to_serializable(v) for k, v in row.items()}
        data.append(record)
    
    # 保存为JSON
    json_file = os.path.join(base_dir, "points_data.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"已保存: {json_file}")
else:
    print(f"文件不存在: {points_file}")

print("转换完成!")
