# 积分流水分析看板 API接口需求文档

## 文档说明
- **版本**: v1.0
- **创建日期**: 2026-03-31
- **用途**: 为积分流水数据分析看板提供后端数据接口
- **基础URL**: `https://ggx-web.weilaiwings.com/api`
- **说明**: 此看板专注于积分流水明细分析，提供积分变动的详细记录，支持分页查询和导出

---

## 一、接口概览

| 接口编号 | 接口名称 | 请求方式 | 用途 |
|---------|---------|---------|------|
| POINT-001 | 获取积分汇总统计 | GET | 顶部4个核心指标卡片 |
| POINT-002 | 获取积分类型分布 | GET | 积分类型分布饼图 |
| POINT-003 | 获取积分区间分布 | GET | 积分区间分布柱状图 |
| POINT-004 | 获取球馆积分排行 | GET | 球馆积分排行柱状图 |
| POINT-005 | 获取每日积分趋势 | GET | 30天积分趋势折线图 |
| POINT-006 | 获取用户积分排行 | GET | 用户积分Top排行榜 |
| POINT-007 | 获取积分流水列表 | GET | 积分明细数据表格 |
| POINT-008 | 获取球馆积分统计 | GET | 按球馆统计积分数据 |
| POINT-009 | 导出积分数据 | GET | 导出Excel功能 |

---

## 二、通用说明

### 2.1 请求头
```
Content-Type: application/json
Authorization: Bearer {token}
```

### 2.2 通用筛选参数

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| province | string | 否 | 省份名称 |
| city | string | 否 | 城市名称 |
| venueId | string | 否 | 球馆ID |
| startDate | string | 否 | 开始日期（YYYY-MM-DD） |
| endDate | string | 否 | 结束日期（YYYY-MM-DD） |

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

### POINT-001 获取积分汇总统计

**接口地址**: `/points/stats/overview`

**请求方式**: GET

**功能说明**: 获取积分流水汇总统计数据

**请求参数**: 使用通用筛选参数

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "totalRecords": 4983,
        "totalPoints": 419769,
        "activePlayers": 1210,
        "activeVenues": 60,
        "avgPointsPerRecord": 84.2,
        "avgPointsPerPlayer": 346.9
    }
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| totalRecords | int | 积分流水总记录数 |
| totalPoints | int | 积分变动总金额 |
| activePlayers | int | 活跃玩家数（有积分流水的用户） |
| activeVenues | int | 活跃球馆数 |
| avgPointsPerRecord | float | 平均每条记录积分 |
| avgPointsPerPlayer | float | 平均每个玩家积分 |

---

### POINT-002 获取积分类型分布

**接口地址**: `/points/stats/type-distribution`

**请求方式**: GET

**功能说明**: 获取积分变动类型的分布统计

**请求参数**: 使用通用筛选参数

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        { "type": "球局胜利结算", "count": 4487, "points": 380000, "percentage": 90.0 },
        { "type": "球局失败结算", "count": 280, "points": -15000, "percentage": 5.6 },
        { "type": "连胜奖励", "count": 120, "points": 24000, "percentage": 2.4 },
        { "type": "段位晋升奖励", "count": 50, "points": 15000, "percentage": 1.0 },
        { "type": "活动奖励", "count": 46, "points": 15769, "percentage": 0.9 }
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

### POINT-003 获取积分区间分布

**接口地址**: `/points/stats/range-distribution`

**请求方式**: GET

**功能说明**: 获取单条记录积分金额的区间分布

**请求参数**: 使用通用筛选参数

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        { "range": "1-10", "count": 182, "percentage": 3.7 },
        { "range": "11-20", "count": 732, "percentage": 14.7 },
        { "range": "21-50", "count": 2711, "percentage": 54.4 },
        { "range": "51-100", "count": 1009, "percentage": 20.3 },
        { "range": "100+", "count": 349, "percentage": 7.0 }
    ]
}
```

---

### POINT-004 获取球馆积分排行

**接口地址**: `/points/stats/venue-ranking`

**请求方式**: GET

**功能说明**: 获取球馆按积分总额排行

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
        {
            "venueId": "V001",
            "venueName": "乔氏台球俱乐部",
            "totalPoints": 45000,
            "recordCount": 531,
            "playerCount": 150,
            "avgPoints": 84.7
        },
        {
            "venueId": "V002",
            "venueName": "龙禧台球俱乐部",
            "totalPoints": 42000,
            "recordCount": 506,
            "playerCount": 142,
            "avgPoints": 83.0
        }
    ]
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| venueId | string | 球馆ID |
| venueName | string | 球馆名称 |
| totalPoints | int | 积分总额 |
| recordCount | int | 流水记录数 |
| playerCount | int | 活跃玩家数 |
| avgPoints | float | 平均每条记录积分 |

---

### POINT-005 获取每日积分趋势

**接口地址**: `/points/stats/daily-trend`

**请求方式**: GET

**功能说明**: 获取近30天每日积分变动趋势

**请求参数**: 使用通用筛选参数

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "date": "2026-03-01",
            "totalPoints": 12500,
            "positivePoints": 14000,
            "negativePoints": -1500,
            "recordCount": 150,
            "playerCount": 85
        },
        {
            "date": "2026-03-02",
            "totalPoints": 13200,
            "positivePoints": 15000,
            "negativePoints": -1800,
            "recordCount": 165,
            "playerCount": 92
        }
    ]
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| date | string | 日期（YYYY-MM-DD） |
| totalPoints | int | 当日积分净变动 |
| positivePoints | int | 当日积分增加总额 |
| negativePoints | int | 当日积分减少总额（负数） |
| recordCount | int | 当日流水记录数 |
| playerCount | int | 当日活跃玩家数 |

---

### POINT-006 获取用户积分排行

**接口地址**: `/points/stats/user-ranking`

**请求方式**: GET

**功能说明**: 获取用户积分排行Top N

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| province | string | 否 | 按省份筛选 |
| city | string | 否 | 按城市筛选 |
| venueId | string | 否 | 按球馆筛选 |
| limit | int | 否 | 返回数量，默认50 |
| sortBy | string | 否 | 排序字段：points/recordCount，默认points |

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "rank": 1,
            "userId": "1001",
            "nickname": "台球王子",
            "venueName": "乔氏台球俱乐部",
            "province": "湖北省",
            "city": "武汉市",
            "totalPoints": 5122,
            "recordCount": 145,
            "avgPoints": 35.3
        }
    ]
}
```

---

### POINT-007 获取积分流水列表

**接口地址**: `/points/records/list`

**请求方式**: GET

**功能说明**: 获取积分流水明细列表，支持分页和多条件筛选

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| page | int | 否 | 页码，默认1 |
| pageSize | int | 否 | 每页数量，默认20，最大100 |
| userId | string | 否 | 用户ID筛选 |
| venueId | string | 否 | 球馆筛选 |
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
        "total": 4983,
        "page": 1,
        "pageSize": 20,
        "list": [
            {
                "recordId": "R001",
                "userId": "1001",
                "nickname": "台球迷",
                "venueId": "V001",
                "venueName": "乔氏台球俱乐部",
                "type": "球局胜利结算",
                "points": 35,
                "balance": 5122,
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
| venueId | string | 球馆ID |
| venueName | string | 球馆名称 |
| type | string | 积分变动类型 |
| points | int | 积分变动金额（正数为增加，负数为减少） |
| balance | int | 变动后余额 |
| title | string | 积分变动标题/说明 |
| createTime | string | 创建时间 |

---

### POINT-008 获取球馆积分统计

**接口地址**: `/points/stats/venue-summary`

**请求方式**: GET

**功能说明**: 获取各球馆的积分统计数据汇总

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| province | string | 否 | 按省份筛选 |
| city | string | 否 | 按城市筛选 |

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "venueId": "V001",
            "venueName": "乔氏台球俱乐部",
            "city": "武汉市",
            "totalPointsIn": 50000,
            "totalPointsOut": 5000,
            "netPoints": 45000,
            "recordCount": 531,
            "playerCount": 150
        }
    ]
}
```

---

### POINT-009 导出积分数据

**接口地址**: `/points/records/export`

**请求方式**: GET

**功能说明**: 导出积分流水数据为Excel文件

**请求参数**: 与POINT-007相同的筛选参数

**响应**: Excel文件流

**响应头**:
```
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename=points_records_20260331.xlsx
```

---

## 四、积分类型字典

| 类型编码 | 类型名称 | 说明 |
|---------|---------|------|
| GAME_WIN | 球局胜利结算 | 比赛胜利获得的积分 |
| GAME_LOSE | 球局失败结算 | 比赛失败扣除的积分 |
| WIN_STREAK | 连胜奖励 | 连胜额外奖励积分 |
| RANK_UP | 段位晋升奖励 | 段位提升奖励 |
| ACTIVITY | 活动奖励 | 参与活动获得积分 |
| SIGN_IN | 签到奖励 | 每日签到获得积分 |
| ADMIN | 系统调整 | 管理员手动调整 |

---

## 五、与其他看板的区别

| 对比项 | CEO看板 | 球房老板看板 | 积分看板 |
|-------|--------|-------------|---------|
| 核心数据 | 用户/场次 | 本店数据 | 积分流水 |
| 时间维度 | 日/周趋势 | 日/周趋势 | 日趋势 |
| 地区维度 | 省/市分布 | 周边排名 | 球馆排名 |
| 用户维度 | 用户分层 | 用户明细 | 积分明细 |
| 导出功能 | 有 | 有 | 有 |

---

## 六、注意事项

1. **数据量控制**: 积分流水数据量大，建议分页查询，单页最大100条
2. **时间范围**: 建议查询时间范围不超过90天
3. **性能要求**: 列表接口响应时间应控制在500ms以内
4. **导出限制**: 单次导出数据量不超过10000条
5. **积分余额**: balance字段为该时间点的用户积分余额
