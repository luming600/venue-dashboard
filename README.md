# 天梯赛数据看板系统

## 项目简介

本项目为天梯赛平台提供三个核心数据看板:
1. **CEO/用户运营看板** - 整体运营数据概览
2. **球房老板看板** - 球房运营数据详情
3. **积分流水分析看板** - 用户积分变动明细

## 功能特性

### 用户分层模型(RFM)
- 核心用户: 近7天有活动 + 对局≥50场 + 胜率≥70%
- 活跃用户: 近15天有活动 + 对局≥30场
- 潜力用户: 近30天有活动 + 胜率≥60% + 对局<30场
- 流失风险: 超过30天无活动 + 历史对局≥30场
- 普通用户: 其他用户

### 对局模式分布
- 抢5对局
- 抢7对局
- 抢9对局(17局9胜)
- 抢11对局
- 抢13对局

## 本地运行

直接用浏览器打开以下文件:
- `球房老板看板_v3_登录版_独立版.html` - 球房老板看板(带登录)
- `天梯赛看板_独立版.html` - CEO看板
- `数据分析看板.html` - 数据分析看板
- `积分分析看板.html` - 积分流水分析

## 测试账号

球房老板看板提供20个测试账号:
- qiaoshi / qiaoshi123 (乔氏台球)
- taiqiu / taiqiu123 (台球俱乐部)
- jueren / jueren123 (巨人台球)
- xingpai / xingpai123 (星牌台球)
- liaoyuan / liaoyuan123 (燎原台球)
- qianjiang / qianjiang123 (千江台球)
- yinhe / yinhe123 (银河台球)
- tiyu / tiyu123 (体育中心)
- dongfang / dongfang123 (东方台球)
- jinsha / jinsha123 (金沙台球)
- mingzhu / mingzhu123 (明珠台球)
- huayang / huayang123 (花样年华)
- jinxiu / jinxiu123 (锦绣台球)
- longcheng / longcheng123 (龙城台球)
- haiyun / haiyun123 (海韵台球)
- yangguang / yangguang123 (阳光台球)
- jinye / jinye123 (金叶台球)
- xinyue / xinyue123 (新月台球)
- hupo / hupo123 (琥珀台球)
- tiancheng / tiancheng123 (天成台球)

## 在线部署

### Gitee Pages部署步骤

1. 登录 Gitee (账号: luming60)
2. 进入仓库: https://gitee.com/luming60/venue-dashboard
3. 点击"服务" → "Gitee Pages"
4. 选择分支: master, 目录: / (根目录)
5. 点击"启动"

### 手动上传文件

如果Git推送失败,可以通过Web界面上传:

1. 访问 https://gitee.com/luming60/venue-dashboard
2. 点击"+"号或"上传文件"
3. 上传以下文件:
   - index.html (首页)
   - 球房老板看板_v3_登录版_独立版.html
   - 天梯赛看板_独立版.html
   - 数据分析看板.html
   - 积分分析看板.html
   - demo_data.js (数据文件)

## 技术栈

- HTML5 + CSS3 + JavaScript
- ECharts 5.4.3 (数据可视化)
- 响应式设计 (支持移动端)
- 深色主题

## 项目结构

```
├── index.html                              # 首页导航
├── 球房老板看板_v3_登录版_独立版.html       # 球房老板看板(带登录)
├── 天梯赛看板_独立版.html                   # CEO看板
├── 数据分析看板.html                        # 数据分析看板
├── 积分分析看板.html                        # 积分流水分析
├── demo_data.js                            # 模拟数据
├── venue_accounts.js                       # 账号配置
└── README.md                               # 本文档
```

## API接口文档

详见以下文档:
- API接口需求文档_CEO看板.md
- API接口需求文档_球房老板看板.md
- API接口需求文档_积分看板.md

## 联系方式

如有问题,请联系开发团队。
