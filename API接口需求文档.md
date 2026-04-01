# 天梯赛数据看板 API接口需求文档

## 文档说明
- **版本**: v1.0
- **创建日期**: 2026-03-31
- **用途**: 为天梯赛数据分析看板提供后端数据接口
- **基础URL**: `https://ggx-web.weilaiwings.com/api`

---

## 一、接口概览

| 接口编号 | 接口名称 | 请求方式 | 用途 |
|---------|---------|---------|------|
| API-001 | 获取核心统计数据 | GET | 看板顶部6个核心指标卡片 |
| API-002 | 获取段位分布数据 | GET | 段位分布饼图 |
| API-003 | 获取用户分层数据 | GET | 用户分层分析（RFM模型） |
| API-004 | 获取省份分布数据 | GET | 省份分布柱状图 |
| API-005 | 获取城市分布数据 | GET | 城市分布柱状图 |
| API-006 | 获取球馆活跃度排行 | GET | 球馆活跃度柱状图 |
| API-007 | 获取球馆胜率排行 | GET | 球馆胜率柱状图 |
| API-008 | 获取每日趋势数据 | GET | 30天趋势折线图 |
| API-009 | 获取每周趋势数据 | GET | 12周趋势混合图 |
| API-010 | 获取高价值用户排行 | GET | Top50高价值用户表格 |
| API-011 | 获取用户列表数据 | GET | 用户详情数据表格（分页、筛选） |

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
| province | string | 否 | 省份名称，如"广东省" |
| city | string | 否 | 城市名称，如"广州市" |
| venueId | string | 否 | 球馆ID |
| rankTier | string | 否 | 段位：杆王/钻石/铂金/黄金/白银/青铜 |

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

### API-001 获取核心统计数据

**接口地址**: `/stats/overview`

**请求方式**: GET

**功能说明**: 获取看板顶部6个核心指标数据

**请求参数**: 使用通用筛选参数

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "totalUsers": 7992,
        "monthlyActiveUsers": 2341,
        "totalGames": 145680,
        "avgWinRate": 62.5,
        "venueCount": 60,
        "maxWinStreak": 36
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

### API-002 获取段位分布数据

**接口地址**: `/stats/rank-distribution`

**请求方式**: GET

**功能说明**: 获取各段位用户数量，用于段位分布饼图

**请求参数**: 使用通用筛选参数

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        { "name": "杆王", "value": 156, "color": "#FF6B6B" },
        { "name": "钻石", "value": 892, "color": "#4ECDC4" },
        { "name": "铂金", "value": 1456, "color": "#45B7D1" },
        { "name": "黄金", "value": 2134, "color": "#F7DC6F" },
        { "name": "白银", "value": 2456, "color": "#BDC3C7" },
        { "name": "青铜", "value": 898, "color": "#CD853F" }
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

### API-003 获取用户分层数据

**接口地址**: `/stats/user-segmentation`

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
            "value": 523,
            "percentage": 6.5,
            "description": "近7天活跃，场次≥20，胜率≥60%",
            "color": "#FFD700"
        },
        {
            "name": "活跃用户",
            "value": 1856,
            "percentage": 23.2,
            "description": "近15天活跃，场次≥10",
            "color": "#2ECC71"
        },
        {
            "name": "潜力用户",
            "value": 2134,
            "percentage": 26.7,
            "description": "近30天活跃，场次≥5",
            "color": "#3498DB"
        },
        {
            "name": "流失风险",
            "value": 1567,
            "percentage": 19.6,
            "description": "近30天无活动，但历史场次≥10",
            "color": "#E67E22"
        },
        {
            "name": "普通用户",
            "value": 1912,
            "percentage": 24.0,
            "description": "其他用户",
            "color": "#95A5A6"
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

### API-004 获取省份分布数据

**接口地址**: `/stats/province-distribution`

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
        { "name": "广东省", "value": 1856 },
        { "name": "江苏省", "value": 1234 },
        { "name": "浙江省", "value": 987 },
        { "name": "山东省", "value": 876 },
        { "name": "河南省", "value": 765 },
        { "name": "四川省", "value": 654 },
        { "name": "湖北省", "value": 543 },
        { "name": "湖南省", "value": 432 },
        { "name": "福建省", "value": 321 },
        { "name": "安徽省", "value": 234 }
    ]
}
```

---

### API-005 获取城市分布数据

**接口地址**: `/stats/city-distribution`

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
        { "name": "广州市", "value": 654, "province": "广东省" },
        { "name": "深圳市", "value": 543, "province": "广东省" },
        { "name": "南京市", "value": 432, "province": "江苏省" },
        { "name": "杭州市", "value": 321, "province": "浙江省" }
        // ... 共15条
    ]
}
```

---

### API-006 获取球馆活跃度排行

**接口地址**: `/stats/venue-activity`

**请求方式**: GET

**功能说明**: 获取球馆按场次数量排行（Top 10）

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
        { "venueId": "V001", "name": "乔氏台球俱乐部", "value": 5234, "city": "广州市" },
        { "venueId": "V002", "name": "龙禧台球俱乐部", "value": 4876, "city": "深圳市" },
        { "venueId": "V003", "name": "星牌台球会所", "value": 4123, "city": "南京市" }
        // ... 共10条
    ]
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| venueId | string | 球馆ID |
| name | string | 球馆名称 |
| value | int | 场次数 |
| city | string | 所在城市 |

---

### API-007 获取球馆胜率排行

**接口地址**: `/stats/venue-winrate`

**请求方式**: GET

**功能说明**: 获取球馆按平均胜率排行（Top 10）

**请求参数**: 同 API-006

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        { "venueId": "V001", "name": "乔氏台球俱乐部", "winRate": 68.5, "city": "广州市" },
        { "venueId": "V002", "name": "龙禧台球俱乐部", "winRate": 65.2, "city": "深圳市" }
        // ... 共10条
    ]
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| winRate | float | 平均胜率（百分比，0-100） |

---

### API-008 获取每日趋势数据

**接口地址**: `/stats/daily-trend`

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
            "activeUsers": 234,
            "newUsers": 45,
            "games": 567
        },
        {
            "date": "2026-03-02",
            "activeUsers": 256,
            "newUsers": 52,
            "games": 612
        }
        // ... 共30条
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

### API-009 获取每周趋势数据

**接口地址**: `/stats/weekly-trend`

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
            "newUsers": 312,
            "games": 4521,
            "activeUsers": 876
        },
        {
            "week": "2026-W02",
            "weekLabel": "第2周",
            "newUsers": 298,
            "games": 4234,
            "activeUsers": 823
        }
        // ... 共12条
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

### API-010 获取高价值用户排行

**接口地址**: `/stats/top-users`

**请求方式**: GET

**功能说明**: 获取高价值用户Top 50排行

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| province | string | 否 | 按省份筛选 |
| city | string | 否 | 按城市筛选 |
| venueId | string | 否 | 按球馆筛选 |
| limit | int | 否 | 返回数量，默认50 |

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "rank": 1,
            "userId": "U001",
            "nickname": "台球王子",
            "province": "广东省",
            "city": "广州市",
            "venueName": "乔氏台球俱乐部",
            "rankTier": "杆王",
            "points": 15890,
            "games": 456,
            "winRate": 78.5,
            "winStreak": 15
        },
        {
            "rank": 2,
            "userId": "U002",
            "nickname": "黑八高手",
            "province": "广东省",
            "city": "深圳市",
            "venueName": "龙禧台球俱乐部",
            "rankTier": "钻石",
            "points": 12345,
            "games": 321,
            "winRate": 72.3,
            "winStreak": 12
        }
        // ... 共50条
    ]
}
```

---

### API-011 获取用户列表数据

**接口地址**: `/users/list`

**请求方式**: GET

**功能说明**: 获取用户详情列表，支持分页和多条件筛选，用于数据表格展示和Excel导出

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| page | int | 否 | 页码，默认1 |
| pageSize | int | 否 | 每页数量，默认20，最大100 |
| province | string | 否 | 省份筛选 |
| city | string | 否 | 城市筛选 |
| venueId | string | 否 | 球馆筛选 |
| rankTier | string | 否 | 段位筛选 |
| segment | string | 否 | 用户分层筛选：核心用户/活跃用户/潜力用户/流失风险/普通用户 |
| keyword | string | 否 | 关键词搜索（昵称/用户ID） |
| sortBy | string | 否 | 排序字段：points/games/winRate/lastActiveTime |
| sortOrder | string | 否 | 排序方式：asc/desc，默认desc |

**响应示例**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "total": 7992,
        "page": 1,
        "pageSize": 20,
        "list": [
            {
                "userId": "U001",
                "nickname": "台球王子",
                "province": "广东省",
                "city": "广州市",
                "venueId": "V001",
                "venueName": "乔氏台球俱乐部",
                "rankTier": "杆王",
                "points": 15890,
                "games": 456,
                "winRate": 78.5,
                "segment": "核心用户",
                "lastActiveTime": "2026-03-30 18:23:45",
                "registerTime": "2025-06-15 10:30:00"
            }
            // ... 共20条
        ]
    }
}
```

**字段说明**:
| 字段名 | 类型 | 说明 |
|-------|------|------|
| userId | string | 用户ID |
| nickname | string | 用户昵称 |
| province | string | 省份 |
| city | string | 城市 |
| venueId | string | 球馆ID |
| venueName | string | 球馆名称 |
| rankTier | string | 段位 |
| points | int | 积分 |
| games | int | 总场次 |
| winRate | float | 胜率（百分比） |
| segment | string | 用户分层 |
| lastActiveTime | string | 最后活跃时间 |
| registerTime | string | 注册时间 |

---

## 四、筛选联动说明

前端实现筛选时，需要支持级联筛选：

1. **省份 → 城市**: 选择省份后，城市下拉框只显示该省份下的城市
2. **城市 → 球馆**: 选择城市后，球馆下拉框只显示该城市下的球馆

### 需要额外提供的辅助接口

#### 获取省份列表
```
GET /regions/provinces
响应: ["广东省", "江苏省", "浙江省", ...]
```

#### 获取城市列表
```
GET /regions/cities?province=广东省
响应: ["广州市", "深圳市", "东莞市", ...]
```

#### 获取球馆列表
```
GET /venues/list?city=广州市
响应: [
    { "venueId": "V001", "name": "乔氏台球俱乐部" },
    { "venueId": "V002", "name": "龙禧台球俱乐部" }
]
```

---

## 五、数据字典

### 5.1 段位枚举值
| 值 | 显示名称 | 颜色代码 |
|---|---------|---------|
| king | 杆王 | #FF6B6B |
| diamond | 钻石 | #4ECDC4 |
| platinum | 铂金 | #45B7D1 |
| gold | 黄金 | #F7DC6F |
| silver | 白银 | #BDC3C7 |
| bronze | 青铜 | #CD853F |

### 5.2 用户分层枚举值
| 值 | 显示名称 | 定义规则 |
|---|---------|---------|
| core | 核心用户 | 近7天活跃 + 场次≥20 + 胜率≥60% |
| active | 活跃用户 | 近15天活跃 + 场次≥10 |
| potential | 潜力用户 | 近30天活跃 + 场次≥5 |
| at_risk | 流失风险 | 近30天无活动 + 历史场次≥10 |
| normal | 普通用户 | 不符合以上条件的用户 |

---

## 六、前端对接示例

### JavaScript 调用示例

```javascript
// 获取核心统计数据
async function fetchOverviewStats(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`/api/stats/overview?${params}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.json();
}

// 获取用户列表
async function fetchUserList(params = {}) {
    const queryParams = new URLSearchParams({
        page: params.page || 1,
        pageSize: params.pageSize || 20,
        ...params.filters
    });
    const response = await fetch(`/api/users/list?${queryParams}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.json();
}

// 刷新所有图表数据
async function refreshDashboard(filters = {}) {
    const [
        stats,
        rankDist,
        segments,
        provinces,
        cities,
        venueActivity,
        venueWinRate,
        dailyTrend,
        weeklyTrend,
        topUsers
    ] = await Promise.all([
        fetchOverviewStats(filters),
        fetch(`/api/stats/rank-distribution?${new URLSearchParams(filters)}`).then(r => r.json()),
        fetch(`/api/stats/user-segmentation?${new URLSearchParams(filters)}`).then(r => r.json()),
        fetch(`/api/stats/province-distribution`).then(r => r.json()),
        fetch(`/api/stats/city-distribution?province=${filters.province || ''}`).then(r => r.json()),
        fetch(`/api/stats/venue-activity?${new URLSearchParams(filters)}`).then(r => r.json()),
        fetch(`/api/stats/venue-winrate?${new URLSearchParams(filters)}`).then(r => r.json()),
        fetch(`/api/stats/daily-trend?${new URLSearchParams(filters)}`).then(r => r.json()),
        fetch(`/api/stats/weekly-trend?${new URLSearchParams(filters)}`).then(r => r.json()),
        fetch(`/api/stats/top-users?${new URLSearchParams(filters)}`).then(r => r.json())
    ]);

    // 更新各图表...
    updateCharts({ stats, rankDist, segments, ... });
}
```

---

## 七、注意事项

1. **性能要求**: 所有接口响应时间应控制在500ms以内
2. **数据缓存**: 建议对统计数据接口增加缓存（如5分钟），提高响应速度
3. **分页限制**: 用户列表接口单次最多返回100条
4. **权限控制**: 接口需要验证用户登录状态，并根据权限返回对应数据范围
5. **数据一致性**: 所有统计数据的截止时间应统一（建议使用T+1，即统计到前一天）

---

## 八、版本记录

| 版本 | 日期 | 修改内容 | 修改人 |
|-----|------|---------|-------|
| v1.0 | 2026-03-31 | 初始版本，定义11个核心接口 | - |
