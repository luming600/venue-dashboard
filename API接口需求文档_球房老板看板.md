# 球房老板看板 API接口需求文档

## 文档说明
- **版本**: v1.0
- **创建日期**: 2026-03-31
- **用途**: 为球房老板数据分析看板提供后端数据接口
- **基础URL**: `https://ggx-web.weilaiwings.com/api`
- **权限说明**: 球房老板只能查看自己名下球馆的数据

---

## 一、接口概览

| 接口编号 | 接口名称 | 请求方式 | 用途 |
|---------|---------|---------|------|
| VENUE-001 | 获取本店核心统计数据 | GET | 顶部6个核心指标卡片 |
| VENUE-002 | 获取本店段位分布数据 | GET | 段位分布饼图 |
| VENUE-003 | 获取本店用户分层数据 | GET | 用户分层分析 |
| VENUE-004 | 获取本店每日趋势数据 | GET | 30天趋势折线图 |
| VENUE-005 | 获取本店每周趋势数据 | GET | 12周趋势混合图 |
| VENUE-006 | 获取周边球馆排名 | GET | 周边球馆活跃度排名 |
| VENUE-007 | 获取本店活跃用户排行 | GET | 活跃用户Top20表格 |
| VENUE-008 | 获取本店用户列表数据 | GET | 用户详情数据表格 |
| VENUE-009 | 获取球馆信息 | GET | 获取当前登录球馆基本信息 |
| VENUE-010 | 获取本店积分汇总统计 | GET | 积分核心指标卡片 |
| VENUE-011 | 获取本店积分类型分布 | GET | 积分类型分布饼图 |
| VENUE-012 | 获取本店积分流水列表 | GET | 积分明细数据表格（分页） |
| VENUE-013 | 导出本店积分数据 | GET | 导出Excel功能 |
| VENUE-014 | 获取对局模式分布 | GET | 对局模式分布图表 |
| VENUE-015 | 获取积分兑换率统计 | GET | 积分兑换率展示 |
| VENUE-016 | 获取玩家排名数据 | GET | 玩家排名（日/周/月/季度） |
| VENUE-017 | 获取用户高级统计 | GET | 炸清/接清/大金/小金等 |

---

## 二、通用说明

### 2.1 请求头
```
Content-Type: application/json
Authorization: Bearer {token}
```

### 2.2 权限控制
- 所有接口自动根据登录用户获取其所属球馆ID
- 球馆老板只能查看自己球馆的数据
- 无需传递venueId参数，由后端从token中解析

### 2.3 通用响应格式
```json
{
    "code": 200,
    "message": "success",
    "data": { ... }
}
```

### 2.4 错误码说明
| 错误码 | 说明 |
|-------|------|
| 200 | 成功 |
| 400 | 参数错误 |
| 401 | 未授权/登录过期 |
| 403 | 无权限（非球馆老板账号） |
| 404 | 球馆不存在 |
| 500 | 服务器内部错误 |

---

## 三、接口详细说明

### VENUE-001 获取本店核心统计数据

**接口地址**: `/venue/stats/overview`

**请求方式**: GET

**功能说明**: 获取本球馆顶部6个核心指标数据

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| rankTier | string | 否 | 段位筛选 |

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "venueId": "V001",
        "venueName": "乔氏台球俱乐部",
        "totalUsers": 310,
        "monthlyActiveUsers": 255,
        "totalGames": 20000,
        "avgWinRate": 53.3,
        "maxWinStreak": 7,
        "regionRank": 4,
        "regionTotal": 32
    }
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| venueId | string | 球馆ID |
| venueName | string | 球馆名称 |
| totalUsers | int | 本店用户数 |
| monthlyActiveUsers | int | 本店月活跃用户数 |
| totalGames | int | 本店总场次 |
| avgWinRate | float | 本店平均胜率（百分比） |
| maxWinStreak | int | 本店最高连胜 |
| regionRank | int | 区域排名 |
| regionTotal | int | 区域内球馆总数 |

---

### VENUE-002 获取本店段位分布数据

**接口地址**: `/venue/stats/rank-distribution`

**请求方式**: GET

**功能说明**: 获取本球馆各段位用户数量

**请求参数**: 无

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        { "name": "最强杆王", "value": 1, "color": "#FFD700" },
        { "name": "校球钻石", "value": 23, "color": "#00CED1" },
        { "name": "加塞铂金", "value": 74, "color": "#E6E6FA" },
        { "name": "走位黄金", "value": 141, "color": "#FFD700" },
        { "name": "翻袋白银", "value": 71, "color": "#C0C0C0" },
        { "name": "清台青铜", "value": 0, "color": "#CD853F" }
    ]
}
```

---

### VENUE-003 获取本店用户分层数据

**接口地址**: `/venue/stats/user-segmentation`

**请求方式**: GET

**功能说明**: 获取本球馆用户分层分析数据

**请求参数**: 无

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "name": "核心用户",
            "value": 23,
            "percentage": 7.4,
            "description": "近7天活跃，场次≥50，胜率≥70%",
            "color": "#FFD700"
        },
        {
            "name": "活跃用户",
            "value": 232,
            "percentage": 74.8,
            "description": "近15天活跃，场次≥30",
            "color": "#00C853"
        },
        {
            "name": "潜力用户",
            "value": 4,
            "percentage": 1.3,
            "description": "近30天活跃，场次<30",
            "color": "#2196F3"
        },
        {
            "name": "流失风险",
            "value": 10,
            "percentage": 3.2,
            "description": "近30天无活动，历史场次≥30",
            "color": "#FF9800"
        },
        {
            "name": "普通用户",
            "value": 41,
            "percentage": 13.2,
            "description": "其他用户",
            "color": "#9E9E9E"
        }
    ]
}
```

---

### VENUE-004 获取本店每日趋势数据

**接口地址**: `/venue/stats/daily-trend`

**请求方式**: GET

**功能说明**: 获取本球馆近30天的每日统计数据

**请求参数**: 无

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "date": "2026-03-01",
            "activeUsers": 25,
            "games": 68
        },
        {
            "date": "2026-03-02",
            "activeUsers": 28,
            "games": 72
        }
    ]
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| date | string | 日期（YYYY-MM-DD） |
| activeUsers | int | 当日活跃用户数（本店） |
| games | int | 当日比赛场次（本店） |

---

### VENUE-005 获取本店每周趋势数据

**接口地址**: `/venue/stats/weekly-trend`

**请求方式**: GET

**功能说明**: 获取本球馆近12周的每周统计数据

**请求参数**: 无

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "week": "2026-W01",
            "weekLabel": "第1周",
            "games": 680,
            "activeUsers": 98
        },
        {
            "week": "2026-W02",
            "weekLabel": "第2周",
            "games": 720,
            "activeUsers": 105
        }
    ]
}
```

---

### VENUE-006 获取周边球馆排名

**接口地址**: `/venue/stats/region-ranking`

**请求方式**: GET

**功能说明**: 获取本球馆所在区域的球馆活跃度排名，本店高亮显示

**请求参数**: 无

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "regionName": "武汉市",
        "myVenue": {
            "venueId": "V001",
            "name": "乔氏台球俱乐部",
            "rank": 4,
            "value": 341,
            "isCurrentVenue": true
        },
        "ranking": [
            { "venueId": "V010", "name": "台球帝国", "value": 341, "rank": 1, "isCurrentVenue": false },
            { "venueId": "V011", "name": "九球台球俱乐部", "value": 330, "rank": 2, "isCurrentVenue": false },
            { "venueId": "V012", "name": "星际台球", "value": 332, "rank": 3, "isCurrentVenue": false },
            { "venueId": "V001", "name": "乔氏台球俱乐部", "value": 341, "rank": 4, "isCurrentVenue": true },
            { "venueId": "V013", "name": "风云台球会所", "value": 334, "rank": 5, "isCurrentVenue": false }
        ]
    }
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| regionName | string | 区域名称（城市） |
| myVenue | object | 本店排名信息 |
| ranking | array | 区域球馆排名列表 |
| isCurrentVenue | boolean | 是否为当前登录球馆 |

---

### VENUE-007 获取本店活跃用户排行

**接口地址**: `/venue/stats/top-users`

**请求方式**: GET

**功能说明**: 获取本球馆活跃用户Top 20排行

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| rankTier | string | 否 | 段位筛选 |
| limit | int | 否 | 返回数量，默认20 |

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "rank": 1,
            "userId": "1001",
            "nickname": "台球迷",
            "rankTier": "加塞铂金 II",
            "points": 850,
            "games": 95,
            "winRate": 58.0,
            "winStreak": 5,
            "segment": "活跃用户"
        }
    ]
}
```

---

### VENUE-008 获取本店用户列表数据

**接口地址**: `/venue/users/list`

**请求方式**: GET

**功能说明**: 获取本球馆用户详情列表，支持分页和筛选

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| page | int | 否 | 页码，默认1 |
| pageSize | int | 否 | 每页数量，默认20，最大100 |
| rankTier | string | 否 | 段位筛选 |
| segment | string | 否 | 用户分层筛选 |
| keyword | string | 否 | 关键词搜索（昵称/用户ID） |
| sortBy | string | 否 | 排序字段：points/games/winRate |
| sortOrder | string | 否 | 排序方式：asc/desc，默认desc |

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "total": 310,
        "page": 1,
        "pageSize": 20,
        "list": [
            {
                "userId": "1001",
                "nickname": "台球迷",
                "rankTier": "加塞铂金 II",
                "points": 850,
                "games": 95,
                "winRate": 58.0,
                "winStreak": 5,
                "segment": "活跃用户",
                "lastActiveTime": "2026-03-30 18:23:45"
            }
        ]
    }
}
```

---

### VENUE-009 获取球馆信息

**接口地址**: `/venue/info`

**请求方式**: GET

**功能说明**: 获取当前登录球馆的基本信息

**请求参数**: 无

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "venueId": "V001",
        "venueName": "乔氏台球俱乐部",
        "province": "湖北省",
        "city": "武汉市",
        "address": "武汉市江汉区XX路XX号",
        "contactPhone": "027-12345678",
        "openTime": "09:00",
        "closeTime": "23:00",
        "tableCount": 12
    }
}
```

---

### VENUE-010 获取本店积分汇总统计

**接口地址**: `/venue/points/overview`

**请求方式**: GET

**功能说明**: 获取本球馆积分流水汇总统计数据

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| startDate | string | 否 | 开始日期（YYYY-MM-DD） |
| endDate | string | 否 | 结束日期（YYYY-MM-DD） |

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "totalRecords": 531,
        "totalPointsIn": 45000,
        "totalPointsOut": 5000,
        "netPoints": 40000,
        "activePlayers": 150,
        "avgPointsPerRecord": 75.3
    }
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| totalRecords | int | 积分流水总记录数（本店） |
| totalPointsIn | int | 积分增加总额 |
| totalPointsOut | int | 积分减少总额 |
| netPoints | int | 积分净变动 |
| activePlayers | int | 有积分流水的玩家数 |
| avgPointsPerRecord | float | 平均每条记录积分 |

---

### VENUE-011 获取本店积分类型分布

**接口地址**: `/venue/points/type-distribution`

**请求方式**: GET

**功能说明**: 获取本球馆积分变动类型的分布统计

**请求参数**: 无

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        { "type": "球局胜利结算", "count": 480, "points": 38000, "percentage": 85.0 },
        { "type": "球局失败结算", "count": 30, "points": -3000, "percentage": 5.6 },
        { "type": "连胜奖励", "count": 15, "points": 4500, "percentage": 2.8 },
        { "type": "段位晋升奖励", "count": 6, "points": 2000, "percentage": 1.1 }
    ]
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| type | string | 积分变动类型 |
| count | int | 该类型记录数 |
| points | int | 该类型积分总额（负数表示扣减） |
| percentage | float | 占比（百分比） |

---

### VENUE-012 获取本店积分流水列表

**接口地址**: `/venue/points/records/list`

**请求方式**: GET

**功能说明**: 获取本球馆积分流水明细列表，支持分页和多条件筛选

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| page | int | 否 | 页码，默认1 |
| pageSize | int | 否 | 每页数量，默认20，最大100 |
| userId | string | 否 | 用户ID筛选 |
| type | string | 否 | 积分类型筛选 |
| minPoints | int | 否 | 最小积分金额 |
| maxPoints | int | 否 | 最大积分金额 |
| startDate | string | 否 | 开始日期 |
| endDate | string | 否 | 结束日期 |
| sortBy | string | 否 | 排序字段：createTime/points |
| sortOrder | string | 否 | 排序方式：asc/desc，默认desc |

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "total": 531,
        "page": 1,
        "pageSize": 20,
        "list": [
            {
                "recordId": "R001",
                "userId": "1001",
                "nickname": "台球迷",
                "type": "球局胜利结算",
                "points": 35,
                "balance": 850,
                "title": "对阵用户1002胜利",
                "createTime": "2026-03-30 18:23:45"
            }
        ]
    }
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| recordId | string | 流水记录ID |
| userId | string | 用户ID |
| nickname | string | 用户昵称 |
| type | string | 积分变动类型 |
| points | int | 积分变动金额（正数为增加，负数为减少） |
| balance | int | 变动后余额 |
| title | string | 积分变动标题/说明 |
| createTime | string | 创建时间 |

---

### VENUE-013 导出本店积分数据

**接口地址**: `/venue/points/records/export`

**请求方式**: GET

**功能说明**: 导出本球馆积分流水数据为Excel文件

**请求参数**: 与VENUE-012相同的筛选参数

**响应**: Excel文件流

**响应头**:
```
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename=venue_points_records_20260331.xlsx
```

---

### VENUE-014 获取对局模式分布

**接口地址**: `/venue/stats/match-modes`

**请求方式**: GET

**功能说明**: 获取本店对局模式（抢5/7/9/11/13/其它）的分布统计

**请求参数**: 无

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        { "name": "抢5", "value": 111000, "desc": "先赢5局", "percentage": 14.07 },
        { "name": "抢7", "value": 196000, "desc": "先赢7局", "percentage": 24.77 },
        { "name": "抢9", "value": 319000, "desc": "17局9胜", "percentage": 39.63 },
        { "name": "抢11", "value": 118000, "desc": "先赢11局", "percentage": 15.0 },
        { "name": "抢13", "value": 52000, "desc": "先赢13局", "percentage": 6.53 },
        { "name": "其它", "value": 30000, "desc": "其他赛制", "percentage": 3.8 }
    ]
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| name | string | 对局模式名称 |
| value | int | 对局场次 |
| desc | string | 模式描述 |
| percentage | float | 占比百分比 |

---

### VENUE-015 获取积分兑换率统计

**接口地址**: `/venue/stats/points-exchange`

**请求方式**: GET

**功能说明**: 获取本店积分兑换率统计数据

**请求参数**: 无

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "totalPoints": 5000000,
        "exchangedPoints": 1250000,
        "exchangeRate": 25.0,
        "exchangeCount": 850,
        "avgExchangeAmount": 235,
        "topExchangeItems": [
            { "name": "球杆", "count": 120, "points": 5000 },
            { "name": "台球", "count": 180, "points": 2000 },
            { "name": "手套", "count": 220, "points": 800 },
            { "name": "巧粉", "count": 280, "points": 300 },
            { "name": "会员卡", "count": 50, "points": 10000 }
        ]
    }
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| totalPoints | int | 总积分 |
| exchangedPoints | int | 已兑换积分 |
| exchangeRate | float | 兑换率(%) |
| exchangeCount | int | 兑换次数 |
| avgExchangeAmount | int | 平均兑换金额 |
| topExchangeItems | array | 热门兑换商品列表 |

---

### VENUE-016 获取玩家排名数据

**接口地址**: `/venue/rankings/players`

**请求方式**: GET

**功能说明**: 获取本店玩家排名数据，支持按日/周/月/季度/年/全部维度

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| period | string | 否 | 统计周期: daily/weekly/monthly/quarterly/yearly/all，默认daily |
| limit | int | 否 | 返回数量，默认20，最大50 |

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "period": "daily",
        "rankings": [
            {
                "rank": 1,
                "userId": "1001",
                "name": "台球王子",
                "games": 15,
                "score": 5200,
                "winRate": 78,
                "streak": 5,
                "rankChange": 2,
                "breakClears": 3,
                "runClears": 4,
                "bigGold": 2,
                "smallGold": 3,
                "doubleMatchPointWinRate": 85
            }
        ]
    }
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| rank | int | 排名 |
| userId | string | 用户ID |
| name | string | 用户昵称 |
| games | int | 场次 |
| score | int | 积分 |
| winRate | float | 胜率(%) |
| streak | int | 连胜记录 |
| rankChange | int | 段位变化(正数升段，负数降段) |
| breakClears | int | 炸清数 |
| runClears | int | 接清数 |
| bigGold | int | 大金数 |
| smallGold | int | 小金数 |
| doubleMatchPointWinRate | float | 双赛点胜率(%) |

---

### VENUE-017 获取用户高级统计

**接口地址**: `/venue/users/{userId}/advanced-stats`

**请求方式**: GET

**功能说明**: 获取指定用户的高级统计数据

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| userId | string | 是 | 用户ID（路径参数） |

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "userId": "1001",
        "name": "台球王子",
        "rank": "清台星耀 III",
        "games": 150,
        "winRate": 68.5,
        "breakClears": 18,
        "runClears": 25,
        "bigGold": 8,
        "smallGold": 12,
        "doubleMatchPointWinRate": 75.0,
        "avgGameTime": 12.5,
        "maxBreak": 85,
        "totalClears": 43
    }
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| breakClears | int | 炸清数（开球后直接清台） |
| runClears | int | 接清数（对手开球后自己清台） |
| bigGold | int | 大金数（特殊高分记录） |
| smallGold | int | 小金数（特殊记录） |
| doubleMatchPointWinRate | float | 双赛点胜率(%) |
| avgGameTime | float | 平均每局用时(分钟) |
| maxBreak | int | 最高单杆得分 |
| totalClears | int | 总清台次数 |

---

## 四、数据字典

### 段位枚举值
| 值 | 显示名称 | 颜色代码 |
|---|---------|---------|
| king | 最强杆王 | #FFD700 |
| diamond | 校球钻石 | #00CED1 |
| platinum | 加塞铂金 | #E6E6FA |
| gold | 走位黄金 | #FFD700 |
| silver | 翻袋白银 | #C0C0C0 |
| bronze | 清台青铜 | #CD853F |

### 用户分层枚举值
| 值 | 显示名称 |
|---|---------|
| core | 核心用户 |
| active | 活跃用户 |
| potential | 潜力用户 |
| at_risk | 流失风险 |
| normal | 普通用户 |

---

## 五、与CEO看板的区别

| 对比项 | CEO看板 | 球房老板看板 |
|-------|--------|-------------|
| 数据范围 | 全国/可筛选 | 仅本店 |
| 权限控制 | 管理员权限 | 球馆老板权限 |
| venueId | 可传参 | 自动从token获取 |
| 地区分布 | 有省份/城市分布 | 无 |
| 周边排名 | 无 | 有（本店高亮） |
| 新增用户趋势 | 有 | 无 |

---

## 六、注意事项

1. **权限隔离**: 球馆老板只能查看自己球馆数据，严禁跨球馆访问
2. **性能要求**: 所有接口响应时间应控制在300ms以内
3. **数据实时性**: 用户数据建议实时更新，统计数据可缓存5分钟
4. **区域排名**: 排名基于球馆所在城市计算
