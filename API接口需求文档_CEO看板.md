# CEO/用户运营看板 API接口需求文档

## 文档说明
- **版本**: v1.0
- **创建日期**: 2026-03-31
- **用途**: 为CEO/用户运营数据分析看板提供后端数据接口
- **基础URL**: `https://ggx-web.weilaiwings.com/api`

---

## 一、接口概览

| 接口编号 | 接口名称 | 请求方式 | 用途 |
|---------|---------|---------|------|
| CEO-001 | 获取核心统计数据 | GET | 顶部6个核心指标卡片 |
| CEO-002 | 获取段位分布数据 | GET | 段位分布饼图 |
| CEO-003 | 获取用户分层数据 | GET | 用户分层分析（RFM模型） |
| CEO-004 | 获取省份分布数据 | GET | 省份分布柱状图 |
| CEO-005 | 获取城市分布数据 | GET | 城市分布柱状图 |
| CEO-006 | 获取球馆活跃度排行 | GET | 球馆活跃度柱状图 |
| CEO-007 | 获取每日趋势数据 | GET | 30天趋势折线图 |
| CEO-008 | 获取每周趋势数据 | GET | 12周趋势混合图 |
| CEO-009 | 获取高价值用户排行 | GET | Top50高价值用户表格 |
| CEO-010 | 获取用户分页列表 | GET | 用户详情分页列表（支持筛选/排序/导出） |

---

## 二、通用说明

### 2.1 请求头
```
Content-Type: application/json
Authorization: Bearer {token}
```

### 2.2 通用筛选参数
以下参数适用于所有需要地区/球馆筛选的接口：

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| province | string | 否 | 省份名称，如"湖北省" |
| city | string | 否 | 城市名称，如"武汉市" |
| venueId | string | 否 | 球馆ID |
| rankTier | string | 否 | 段位：最强杆王/校球钻石/加塞铂金/走位黄金/翻袋白银/清台青铜 |

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
| 403 | 无权限 |
| 500 | 服务器内部错误 |

---

## 三、接口详细说明

### CEO-001 获取核心统计数据

**接口地址**: `/ceo/stats/overview`

**请求方式**: GET

**功能说明**: 获取看板顶部6个核心指标数据

**请求参数**: 使用通用筛选参数

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "totalUsers": 10000,
        "monthlyActiveUsers": 4938,
        "totalGames": 643364,
        "avgWinRate": 53.6,
        "venueCount": 32,
        "maxWinStreak": 11
    }
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| totalUsers | int | 总用户数 |
| monthlyActiveUsers | int | 月活跃用户数（近30天有场次记录） |
| totalGames | int | 总比赛场次 |
| avgWinRate | float | 平均胜率（百分比，0-100） |
| venueCount | int | 球馆数量 |
| maxWinStreak | int | 最高连胜记录 |

---

### CEO-002 获取段位分布数据

**接口地址**: `/ceo/stats/rank-distribution`

**请求方式**: GET

**功能说明**: 获取各段位用户数量，用于段位分布饼图

**请求参数**: 使用通用筛选参数

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        { "name": "最强杆王", "value": 50, "color": "#FFD700" },
        { "name": "校球钻石", "value": 650, "color": "#00CED1" },
        { "name": "加塞铂金", "value": 2300, "color": "#E6E6FA" },
        { "name": "走位黄金", "value": 4800, "color": "#FFD700" },
        { "name": "翻袋白银", "value": 2200, "color": "#C0C0C0" },
        { "name": "清台青铜", "value": 0, "color": "#CD853F" }
    ]
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| name | string | 段位名称 |
| value | int | 该段位用户数 |
| color | string | 图表显示颜色（HEX格式） |

---

### CEO-003 获取用户分层数据

**接口地址**: `/ceo/stats/user-segmentation`

**请求方式**: GET

**功能说明**: 基于RFM模型的用户分层分析

**请求参数**: 使用通用筛选参数

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "name": "核心用户",
            "value": 679,
            "percentage": 6.8,
            "description": "近7天活跃，场次≥50，胜率≥70%",
            "color": "#FFD700"
        },
        {
            "name": "活跃用户",
            "value": 7471,
            "percentage": 74.7,
            "description": "近15天活跃，场次≥30",
            "color": "#00C853"
        },
        {
            "name": "潜力用户",
            "value": 243,
            "percentage": 2.4,
            "description": "近30天活跃，场次<30",
            "color": "#2196F3"
        },
        {
            "name": "流失风险",
            "value": 329,
            "percentage": 3.3,
            "description": "近30天无活动，历史场次≥30",
            "color": "#FF9800"
        },
        {
            "name": "普通用户",
            "value": 1278,
            "percentage": 12.8,
            "description": "其他用户",
            "color": "#9E9E9E"
        }
    ]
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| name | string | 分层名称 |
| value | int | 该层用户数 |
| percentage | float | 占比（百分比） |
| description | string | 分层规则描述 |
| color | string | 图表显示颜色 |

---

### CEO-004 获取省份分布数据

**接口地址**: `/ceo/stats/province-distribution`

**请求方式**: GET

**功能说明**: 获取各省份用户数量排行（Top 10）

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| limit | int | 否 | 返回数量，默认10 |

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        { "name": "湖北省", "value": 3223 },
        { "name": "广东省", "value": 1189 },
        { "name": "河南省", "value": 1016 },
        { "name": "河北省", "value": 872 },
        { "name": "辽宁省", "value": 806 },
        { "name": "江苏省", "value": 586 },
        { "name": "浙江省", "value": 461 },
        { "name": "山东省", "value": 429 },
        { "name": "四川省", "value": 337 },
        { "name": "陕西省", "value": 312 }
    ]
}
```

---

### CEO-005 获取城市分布数据

**接口地址**: `/ceo/stats/city-distribution`

**请求方式**: GET

**功能说明**: 获取各城市用户数量排行（Top 15）

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| province | string | 否 | 按省份筛选 |
| limit | int | 否 | 返回数量，默认15 |

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        { "name": "武汉市", "value": 2847, "province": "湖北省" },
        { "name": "广州市", "value": 656, "province": "广东省" },
        { "name": "郑州市", "value": 588, "province": "河南省" },
        { "name": "沈阳市", "value": 432, "province": "辽宁省" },
        { "name": "石家庄市", "value": 430, "province": "河北省" }
    ]
}
```

---

### CEO-006 获取球馆活跃度排行

**接口地址**: `/ceo/stats/venue-activity`

**请求方式**: GET

**功能说明**: 获取球馆按用户数排行（Top 10）

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| province | string | 否 | 按省份筛选 |
| city | string | 否 | 按城市筛选 |
| limit | int | 否 | 返回数量，默认10 |

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        { "venueId": "V001", "name": "乔氏台球俱乐部", "value": 341, "city": "广州市" },
        { "venueId": "V002", "name": "龙禧台球俱乐部", "value": 336, "city": "深圳市" }
    ]
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| venueId | string | 球馆ID |
| name | string | 球馆名称 |
| value | int | 用户数 |
| city | string | 所在城市 |

---

### CEO-007 获取每日趋势数据

**接口地址**: `/ceo/stats/daily-trend`

**请求方式**: GET

**功能说明**: 获取近30天的每日统计数据

**请求参数**: 使用通用筛选参数

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "date": "2026-03-01",
            "activeUsers": 180,
            "newUsers": 45,
            "games": 450
        },
        {
            "date": "2026-03-02",
            "activeUsers": 185,
            "newUsers": 48,
            "games": 480
        }
    ]
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| date | string | 日期（YYYY-MM-DD） |
| activeUsers | int | 当日活跃用户数 |
| newUsers | int | 当日新增用户数 |
| games | int | 当日比赛场次 |

---

### CEO-008 获取每周趋势数据

**接口地址**: `/ceo/stats/weekly-trend`

**请求方式**: GET

**功能说明**: 获取近12周的每周统计数据

**请求参数**: 使用通用筛选参数

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "week": "2026-W01",
            "weekLabel": "第1周",
            "newUsers": 350,
            "games": 4500,
            "activeUsers": 650
        },
        {
            "week": "2026-W02",
            "weekLabel": "第2周",
            "newUsers": 380,
            "games": 4800,
            "activeUsers": 720
        }
    ]
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| week | string | 周标识（YYYY-Wnn格式） |
| weekLabel | string | 周显示名称 |
| newUsers | int | 该周新增用户数 |
| games | int | 该周比赛场次 |
| activeUsers | int | 该周活跃用户数 |

---

### CEO-009 获取高价值用户排行

**接口地址**: `/ceo/stats/top-users`

**请求方式**: GET

**功能说明**: 获取高价值用户Top 50排行

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| province | string | 否 | 按省份筛选 |
| city | string | 否 | 按城市筛选 |
| venueId | string | 否 | 按球馆筛选 |
| rankTier | string | 否 | 按段位筛选 |
| limit | int | 否 | 返回数量，默认50 |

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "rank": 1,
            "userId": "1728",
            "nickname": "台球王子",
            "province": "山东省",
            "city": "青岛市",
            "venueId": "V001",
            "venueName": "台球帝国",
            "rankTier": "最强杆王",
            "points": 9760,
            "games": 298,
            "winRate": 65.0,
            "winStreak": 7
        }
    ]
}
```

---

### CEO-010 获取用户分页列表

**接口地址**: `/ceo/users/list`

**请求方式**: GET

**功能说明**: 获取用户详情分页列表，支持多条件筛选、排序和导出。注意：此接口返回的是**用户档案数据**，不是积分流水记录。如需查看积分流水明细，请使用积分分析看板相关接口。

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| page | int | 否 | 页码，默认1 |
| pageSize | int | 否 | 每页数量，默认20，最大100 |
| province | string | 否 | 省份筛选 |
| city | string | 否 | 城市筛选 |
| venueId | string | 否 | 球馆筛选 |
| rankTier | string | 否 | 段位筛选 |
| segment | string | 否 | 用户分层筛选 |
| keyword | string | 否 | 关键词搜索（昵称/用户ID） |
| sortBy | string | 否 | 排序字段：points/games/winRate/lastActiveTime |
| sortOrder | string | 否 | 排序方式：asc/desc，默认desc |
| export | boolean | 否 | 是否导出Excel，默认false |

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "total": 10000,
        "page": 1,
        "pageSize": 20,
        "totalPages": 500,
        "list": [
            {
                "userId": "1000",
                "nickname": "台球迷",
                "province": "湖北省",
                "city": "武汉市",
                "venueId": "V001",
                "venueName": "乔氏台球俱乐部",
                "rankTier": "走位黄金 I",
                "points": 215,
                "games": 19,
                "winRate": 49.0,
                "segment": "普通用户",
                "registerTime": "2025-06-15 10:30:00",
                "lastActiveTime": "2026-03-25 18:23:45"
            }
        ]
    }
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| total | int | 总记录数 |
| page | int | 当前页码 |
| pageSize | int | 每页数量 |
| totalPages | int | 总页数 |
| list | array | 用户列表数据 |
| userId | string | 用户ID |
| nickname | string | 用户昵称 |
| province | string | 省份 |
| city | string | 城市 |
| venueId | string | 球馆ID |
| venueName | string | 球馆名称 |
| rankTier | string | 当前段位 |
| points | int | 当前积分 |
| games | int | 累计场次 |
| winRate | float | 胜率（百分比） |
| segment | string | 用户分层 |
| registerTime | string | 注册时间 |
| lastActiveTime | string | 最后活跃时间 |

**导出说明**:
当`export=true`时，返回Excel文件流：
```
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename=users_export_20260331.xlsx
```

---

## 四、筛选联动接口

### 获取省份列表
```
GET /regions/provinces
响应: ["湖北省", "广东省", "河南省", ...]
```

### 获取城市列表
```
GET /regions/cities?province=湖北省
响应: ["武汉市", "宜昌市", "襄阳市", ...]
```

### 获取球馆列表
```
GET /venues/list?city=武汉市
响应: [
    { "venueId": "V001", "name": "乔氏台球俱乐部" },
    { "venueId": "V002", "name": "龙禧台球俱乐部" }
]
```

---

## 五、数据字典

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
| 值 | 显示名称 | 定义规则 |
|---|---------|---------|
| core | 核心用户 | 近7天活跃 + 场次≥50 + 胜率≥70% |
| active | 活跃用户 | 近15天活跃 + 场次≥30 |
| potential | 潜力用户 | 近30天活跃 + 胜率≥60% + 场次<30 |
| at_risk | 流失风险 | 近30天无活动 + 历史场次≥30 |
| normal | 普通用户 | 不符合以上条件 |

---

## 六、注意事项

1. **性能要求**: 所有接口响应时间应控制在500ms以内
2. **数据缓存**: 建议对统计数据接口增加缓存（如5分钟）
3. **权限控制**: 需要验证用户登录状态和权限
4. **数据一致性**: 统计数据截止时间应统一（T+1）
