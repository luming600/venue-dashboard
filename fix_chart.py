# -*- coding: utf-8 -*-
import re

with open('球房老板看板_v2.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找并替换段位分布饼图配置
old_start = "echarts.init(document.getElementById('rankChart')).setOption({"
old_end = "color: ['#CD7F32', '#C0C0C0', '#FFD700', '#00CED1', '#E6E6FA', '#FFD700']\n            });"

new_config = """echarts.init(document.getElementById('rankChart')).setOption({
                tooltip: {
                    trigger: 'item',
                    formatter: '{b}: {c}人 ({d}%)',
                    textStyle: { fontSize: 14 }
                },
                legend: {
                    bottom: '0%',
                    textStyle: { color: '#fff', fontSize: 13 },
                    itemWidth: 12,
                    itemHeight: 12,
                    itemGap: 8
                },
                series: [{
                    type: 'pie',
                    radius: ['35%', '55%'],
                    center: ['50%', '42%'],
                    data: rankDist,
                    label: { show: false },
                    emphasis: {
                        label: { show: true, fontSize: 14, fontWeight: 'bold' }
                    },
                    labelLine: { show: false },
                    itemStyle: { borderRadius: 6 }
                }],
                color: ['#CD7F32', '#C0C0C0', '#FFD700', '#00CED1', '#E6E6FA', '#9932CC', '#FF4500', '#8B0000', '#FFD700', '#FFD700']
            });"""

# 找到开始和结束位置
start_idx = content.find(old_start)
end_idx = content.find(old_end, start_idx)

if start_idx != -1 and end_idx != -1:
    end_idx += len(old_end)
    content = content[:start_idx] + new_config + content[end_idx:]
    print('段位分布饼图配置已更新')
else:
    print('未找到目标内容')
    print('start_idx:', start_idx)
    print('end_idx:', end_idx)

with open('球房老板看板_v2.html', 'w', encoding='utf-8') as f:
    f.write(content)
