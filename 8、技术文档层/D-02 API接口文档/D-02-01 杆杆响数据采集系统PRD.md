# 杆杆响天梯赛数据采集系统 PRD

> **文档版本**：V1.0
> **更新日期**：2026年3月
> **文档状态**：待评审
> **目标读者**：研发团队、产品经理、测试工程师

---

## 一、产品概述

### 1.1 产品背景

杆杆响天梯赛系统已在球房部署并正常运行，系统记录了用户的使用、参赛、互动等完整行为数据。为支撑天梯赛案例数据收集工作，需要将分散在各模块的数据进行整合封装，形成标准化的数据输出能力。

### 1.2 产品目标

1. **数据自主化**：实现案例所需核心数据的自主采集，减少对收银系统的依赖
2. **数据标准化**：统一数据口径，形成可复用的数据接口
3. **流程自动化**：支持定时同步飞书多维表格，实现数据自动更新

### 1.3 核心价值

| 场景 | 原方案 | 新方案 |
|------|--------|--------|
| 上座率统计 | 依赖收银系统导出 | 杆杆响使用记录直接计算 |
| 到店频次 | 依赖收银系统 | 杆杆响使用打卡记录 |
| 停留时长 | 依赖收银系统 | 杆杆响使用时长记录 |
| 用户活跃 | 需对接第三方 | 杆杆响直接统计 |
| 活动数据 | 需手工整理 | 杆杆响自动汇总 |

---

## 二、数据能力矩阵

### 2.1 杆杆响可自主采集的数据

#### 2.1.0 多维度时间粒度支持

**说明**：系统支持按日(DAY)、周(WEEK)、月(MONTH)三种时间粒度进行数据统计，便于不同场景的分析需求。

**时间粒度定义**：

| 粒度 | 说明 | 适用场景 |
|------|------|----------|
| **日 (DAY)** | 精确到每一天 | 活动效果分析、异常排查 |
| **周 (WEEK)** | 按自然周统计（周一~周日） | 短期趋势分析、周对比 |
| **月 (MONTH)** | 按自然月统计 | 月度汇报、周期对比 |

**时间粒度参数说明**：

| API | group_by参数 | 支持粒度 | 默认值 |
|-----|--------------|----------|--------|
| F-002 用户数据统计 | group_by | day/week/month | month |
| F-005 到店频次统计 | group_by | day/week/month | month |
| F-006 停留时长统计 | group_by | day/week/month | month |
| F-007 积分转化分析 | group_by | day/week/month | month |
| F-010 RFM分析 | stat_days | 支持任意天数 | 90天 |

**日期格式化规则**：

```sql
-- 按日统计
DATE_FORMAT(date_column, '%Y-%m-%d') as stat_date

-- 按周统计（自然周，周一为起始）
DATE_FORMAT(DATE_SUB(date_column, INTERVAL WEEKDAY(date_column) DAY), '%Y-%m-%d') as stat_week_start

-- 按月统计
DATE_FORMAT(date_column, '%Y-%m') as stat_month
```

**多维度SQL示例**：

```sql
-- 通用多粒度统计查询模板
-- 传入参数 @group_by: 'day' | 'week' | 'month'

SELECT
    merchant_id,
    CASE @group_by
        WHEN 'day' THEN DATE_FORMAT(created_at, '%Y-%m-%d')
        WHEN 'week' THEN DATE_FORMAT(DATE_SUB(created_at, INTERVAL WEEKDAY(created_at) DAY), '%Y-%m-%d')
        WHEN 'month' THEN DATE_FORMAT(created_at, '%Y-%m')
    END as stat_period,
    COUNT(DISTINCT user_id) as users,
    COUNT(*) as events,
    AVG(value) as avg_value
FROM source_table
WHERE created_at BETWEEN @start_date AND @end_date
GROUP BY merchant_id,
    CASE @group_by
        WHEN 'day' THEN DATE_FORMAT(created_at, '%Y-%m-%d')
        WHEN 'week' THEN DATE_FORMAT(DATE_SUB(created_at, INTERVAL WEEKDAY(created_at) DAY), '%Y-%m-%d')
        WHEN 'month' THEN DATE_FORMAT(created_at, '%Y-%m')
    END;
```

**周统计特殊处理**：

```sql
-- 周报数据计算（周一~周日为一周）
SELECT
    merchant_id,
    YEARWEEK(created_at, 1) as year_week,  -- 1表示周一为起始
    MIN(DATE(created_at)) as week_start,
    MAX(DATE(created_at)) as week_end,
    COUNT(DISTINCT user_id) as weekly_active_users,
    COUNT(*) as weekly_events
FROM usage_records
GROUP BY merchant_id, YEARWEEK(created_at, 1)
ORDER BY year_week DESC;
```

**返回格式示例（按日）**：

```json
{
    "code": 0,
    "data": {
        "period": {
            "start": "2025-09-01",
            "end": "2025-09-30"
        },
        "group_by": "day",
        "daily_stats": [{
            "date": "2025-09-01",
            "day_of_week": "周一",
            "active_users": 120,
            "total_visits": 350,
            "avg_stay_minutes": 185
        }, {
            "date": "2025-09-02",
            "day_of_week": "周二",
            "active_users": 95,
            "total_visits": 280,
            "avg_stay_minutes": 175
        }]
    }
}
```

**返回格式示例（按周）**：

```json
{
    "code": 0,
    "data": {
        "period": {
            "start": "2025-09-01",
            "end": "2025-09-30"
        },
        "group_by": "week",
        "weekly_stats": [{
            "week_start": "2025-09-01",
            "week_end": "2025-09-07",
            "week_num": 36,
            "active_users": 580,
            "total_visits": 2100,
            "avg_stay_minutes": 188,
            "growth_rate_vs_last_week": 5.2
        }]
    }
}
```

---

#### 2.1.1 用户行为数据

| 数据项 | 计算方式 | 数据来源 | 实时性 |
|--------|----------|----------|--------|
| 注册用户数 | COUNT(DISTINCT user_id) | 用户注册表 | 实时 |
| 月活用户数 | COUNT(DISTINCT user_id) WHERE login_time >= 本月 | 登录日志表 | 每日更新 |
| 活跃率 | 月活用户数 / 注册用户数 × 100% | 公式计算 | 每日更新 |
| 累计参赛人次 | SUM(参赛次数) | 赛事参与表 | 实时 |
| 30日留存率 | Cohort分析：第N日留存用户/当日新增用户 | 留存分析表 | 每日更新 |
| 新增用户数 | COUNT(*) WHERE created_at >= 统计周期起始 | 用户表 | 每日更新 |

#### 2.1.2 天梯赛系统使用行为数据

| 数据项 | 计算方式 | 数据来源 | 实时性 |
|--------|----------|----------|--------|
| 使用次数 | COUNT(*) WHERE type='open' | 使用记录表 | 实时 |
| 关闭次数 | COUNT(*) WHERE type='close' | 使用记录表 | 实时 |
| 营业时长 | SUM(use_end_time - use_start_time) | 使用记录表 | 每日汇总 |
| 累计使用时长 | SUM(stay_duration) | 用户行为表 | 实时 |
| 平均单次使用时长 | AVG(stay_duration) | 用户行为表 | 每日更新 |
| 日均使用数 | COUNT(*)/ 统计天数 | 公式计算 | 每日更新 |
| 登录次数 | COUNT(*) | 登录日志表 | 实时 |
| 活跃天数 | COUNT(DISTINCT DATE(login_time)) | 登录日志表 | 每日更新 |

#### 2.1.3 上座率计算

**计算逻辑**：

```
上座率 = 实际使用时长 ÷ (球桌数量 × 营业时长) × 100%
```

**数据来源**：
- `billiard_tables`：球桌数量（table_count字段）
- `usage_records`：使用记录（use_start_time, use_end_time, table_id）
- `merchant_config`：营业时长配置（start_time, end_time）

**SQL示例**：

```sql
-- 工作日上座率计算（示例：周一至周四）
SELECT
    merchant_id,
    COUNT(DISTINCT DATE(use_start_time)) as days,
    SUM(
        CASE
            WHEN DAYOFWEEK(use_start_time) BETWEEN 2 AND 5  -- 周一到周四
            THEN TIMESTAMPDIFF(MINUTE, use_start_time, use_end_time)
            ELSE 0
        END
    ) as total_minutes,
    (SELECT table_count FROM billiard_tables WHERE merchant_id = t.merchant_id LIMIT 1) as table_count,
    (SELECT
        SUM(TIMESTAMPDIFF(MINUTE, start_time, end_time))
        FROM merchant_config
        WHERE merchant_id = t.merchant_id
        AND DAYOFWEEK(start_time) BETWEEN 2 AND 5
    ) as available_minutes
FROM usage_records t
WHERE use_start_time >= '2025-09-01' AND use_start_time < '2025-12-01'
GROUP BY merchant_id;
```

**公式**：

```
工作日上座率 = (实际使用总时长 / 可用总时长) × 100%
可用使用时长 = 球桌数量 × 单日营业时长(分钟) × 工作日天数
```

#### 2.1.4 到店频次计算

**计算逻辑**：

```
月均到店频次 = 月度使用总次数 / 月度活跃用户数
```

**SQL示例**：

```sql
-- 用户月均到店频次
SELECT
    merchant_id,
    COUNT(*) as total_visits,
    COUNT(DISTINCT user_id) as active_users,
    COUNT(*) / COUNT(DISTINCT user_id) as avg_frequency
FROM usage_records
WHERE use_start_time >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
GROUP BY merchant_id;
```

#### 2.1.5 停留时长计算

**计算逻辑**：

```
停留时长 = use_end_time - use_start_time
平均停留时长 = AVG(use_end_time - use_start_time)
```

**SQL示例**：

```sql
-- 平均停留时长统计
SELECT
    merchant_id,
    AVG(TIMESTAMPDIFF(MINUTE, use_start_time, use_end_time)) as avg_stay_minutes,
    MAX(TIMESTAMPDIFF(MINUTE, use_start_time, use_end_time)) as max_stay_minutes,
    MIN(TIMESTAMPDIFF(MINUTE, use_start_time, use_end_time)) as min_stay_minutes
FROM usage_records
WHERE use_end_time IS NOT NULL
GROUP BY merchant_id;
```

#### 2.1.6 积分转化数据

**说明**：积分系统记录用户在天梯赛中的积分获取和消耗行为，用于分析用户的参与深度和留存情况。

**积分获取来源**：
| 来源类型 | 说明 |
|----------|------|
| login | 每日登录奖励 |
| competition | 参与比赛奖励 |
| rank | 比赛排名奖励 |
| task | 完成任务奖励 |
| invite | 邀请好友奖励 |

**积分消耗去向**：
| 去向类型 | 说明 |
|----------|------|
| redeem | 兑换礼品/优惠券 |
| offset | 抵扣消费 |
| lottery | 参与抽奖 |
| upgrade | 升级称号/头像框 |

**计算逻辑**：

```
积分获取率 = 获得积分用户数 / 月活用户数 × 100%
积分消耗率 = 消耗积分用户数 / 月活用户数 × 100%
积分余额均值 = SUM(用户积分余额) / 用户数
积分转化率 = 有积分消耗的用户数 / 获得积分用户数 × 100%
```

**SQL示例 - 积分获取统计**：

```sql
-- 月度积分获取统计
SELECT
    merchant_id,
    DATE_FORMAT(created_at, '%Y-%m') as stat_month,
    COUNT(DISTINCT user_id) as users_earned,
    SUM(points) as total_points_earned,
    AVG(points) as avg_points_per_transaction
FROM point_transactions
WHERE type = 'earn'
GROUP BY merchant_id, stat_month;
```

**SQL示例 - 积分消耗统计**：

```sql
-- 月度积分消耗统计
SELECT
    merchant_id,
    DATE_FORMAT(created_at, '%Y-%m') as stat_month,
    COUNT(DISTINCT user_id) as users_consumed,
    SUM(points) as total_points_consumed,
    COUNT(*) as consume_times
FROM point_transactions
WHERE type = 'consume'
GROUP BY merchant_id, stat_month;
```

**SQL示例 - 积分转化率**：

```sql
-- 积分转化率 = 消耗用户 / 获取用户
SELECT
    p.merchant_id,
    p.stat_month,
    e.users_earned,
    c.users_consumed,
    ROUND(c.users_consumed / e.users_earned * 100, 2) as conversion_rate
FROM (
    SELECT merchant_id, DATE_FORMAT(created_at, '%Y-%m') as stat_month,
           COUNT(DISTINCT user_id) as users_earned
    FROM point_transactions WHERE type = 'earn'
    GROUP BY merchant_id, stat_month
) e
LEFT JOIN (
    SELECT merchant_id, DATE_FORMAT(created_at, '%Y-%m') as stat_month,
           COUNT(DISTINCT user_id) as users_consumed
    FROM point_transactions WHERE type = 'consume'
    GROUP BY merchant_id, stat_month
) c ON e.merchant_id = c.merchant_id AND e.stat_month = c.stat_month;
```

**数据表设计参考**：

```sql
-- 积分账户表
CREATE TABLE user_points (
    id VARCHAR(32) PRIMARY KEY,
    user_id VARCHAR(32) NOT NULL,
    merchant_id VARCHAR(32) NOT NULL,
    balance INT DEFAULT 0 COMMENT '当前积分余额',
    total_earned INT DEFAULT 0 COMMENT '累计获取积分',
    total_consumed INT DEFAULT 0 COMMENT '累计消耗积分',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_merchant (user_id, merchant_id)
) COMMENT '用户积分账户表';

-- 积分变动记录表
CREATE TABLE point_transactions (
    id VARCHAR(32) PRIMARY KEY,
    user_id VARCHAR(32) NOT NULL,
    merchant_id VARCHAR(32) NOT NULL,
    type VARCHAR(20) NOT NULL COMMENT 'earn:获取 consume:消耗',
    points INT NOT NULL COMMENT '积分数量（正数）',
    source VARCHAR(50) COMMENT '来源类型：login/competition/rank/task/invite/redeem/offset/lottery/upgrade',
    order_id VARCHAR(32) COMMENT '关联订单ID（如有）',
    description VARCHAR(200) COMMENT '变动描述',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_date (user_id, created_at),
    INDEX idx_merchant_date (merchant_id, created_at)
) COMMENT '积分变动记录表';
```

#### 2.1.7 RFM用户价值分析

**说明**：RFM模型是经典的用户价值分析工具，用于评估用户的忠诚度和贡献价值。在天梯赛场景中，RFM被重新定义为：

| 维度 | 天梯赛定义 | 计算方式 |
|------|------------|----------|
| **R - Recency（近度）** | 用户最近一次使用天梯赛的距今天数 | 距离分析基准日的天数 |
| **F - Frequency（频度）** | 用户使用天梯赛的频率 | 统计周期内的使用/参赛次数 |
| **M - Monetary（忠诚度）** | 用户对天梯赛的参与深度 | 累计积分获取量 |

**RFM分群定义**：

| 用户类型 | R值 | F值 | M值 | 特征描述 |
|----------|-----|-----|-----|----------|
| **重要价值用户** | 高 | 高 | 高 | 核心用户，持续活跃，高积分贡献 |
| **重要保持用户** | 低 | 高 | 高 | 活跃度下降，需重点召回 |
| **重要发展用户** | 高 | 低 | 高 | 潜力用户，需提升使用频率 |
| **重要挽留用户** | 低 | 低 | 高 | 流失风险，需激活 |
| **一般价值用户** | 高 | 高 | 低 | 活跃但贡献低，可推送积分消耗 |
| **一般用户** | 其他组合 | - | - | 普通用户 |

**计算逻辑**：

```
R值 = 分析基准日 - 用户最后使用日期
F值 = 统计周期内使用总次数
M值 = 统计周期内积分获取总量

R评分 = 根据R值分布计算1-5分
F评分 = 根据F值分布计算1-5分
M评分 = 根据M值分布计算1-5分

RFM组合 = R评分 + F评分 + M评分
用户分层 = 根据RFM组合判定用户类型
```

**SQL示例 - RFM计算**：

```sql
-- 计算用户RFM值
SELECT
    u.id as user_id,
    u.merchant_id,
    DATEDIFF(CURDATE(), COALESCE(MAX(r.use_start_time), u.created_at)) as R_value,
    COUNT(r.id) as F_value,
    COALESCE(SUM(p.points), 0) as M_value
FROM users u
LEFT JOIN usage_records r ON u.id = r.user_id
    AND r.use_start_time >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
LEFT JOIN point_transactions p ON u.id = p.user_id
    AND p.type = 'earn'
    AND p.created_at >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
WHERE u.merchant_id = 'M001'
GROUP BY u.id, u.merchant_id;
```

**SQL示例 - RFM评分（使用百分位数）**：

```sql
-- 计算RFM评分（1-5分）
WITH rfm_raw AS (
    SELECT
        user_id,
        merchant_id,
        DATEDIFF(CURDATE(), last_action_date) as R,
        total_frequency as F,
        total_monetary as M
    FROM (
        SELECT
            u.id as user_id,
            u.merchant_id,
            MAX(COALESCE(r.use_start_time, p.created_at)) as last_action_date,
            COUNT(DISTINCT r.id) as total_frequency,
            COALESCE(SUM(CASE WHEN p.type = 'earn' THEN p.points ELSE 0 END), 0) as total_monetary
        FROM users u
        LEFT JOIN usage_records r ON u.id = r.user_id
        LEFT JOIN point_transactions p ON u.id = p.user_id
        WHERE u.merchant_id = 'M001'
        GROUP BY u.id, u.merchant_id
    ) t
)
SELECT
    user_id,
    merchant_id,
    R, F, M,
    NTILE(5) OVER (ORDER BY R DESC) as R_score,    -- R越小分数越高
    NTILE(5) OVER (ORDER BY F ASC) as F_score,     -- F越大分数越高
    NTILE(5) OVER (ORDER BY M ASC) as M_score,     -- M越大分数越高
    CONCAT(
        NTILE(5) OVER (ORDER BY R DESC),
        NTILE(5) OVER (ORDER BY F ASC),
        NTILE(5) OVER (ORDER BY M ASC)
    ) as RFM_code
FROM rfm_raw;
```

**SQL示例 - 用户分群统计**：

```sql
-- RFM用户分群
WITH rfm_scores AS (
    SELECT
        user_id,
        merchant_id,
        R, F, M,
        CASE
            WHEN R_score >= 4 AND F_score >= 4 AND M_score >= 4 THEN '重要价值用户'
            WHEN R_score <= 2 AND F_score >= 4 AND M_score >= 4 THEN '重要保持用户'
            WHEN R_score >= 4 AND F_score <= 2 AND M_score >= 4 THEN '重要发展用户'
            WHEN R_score <= 2 AND F_score <= 2 AND M_score >= 4 THEN '重要挽留用户'
            WHEN R_score >= 4 AND F_score >= 4 AND M_score <= 2 THEN '一般价值用户'
            ELSE '一般用户'
        END as user_segment
    FROM rfm_scores_calc
)
SELECT
    merchant_id,
    user_segment,
    COUNT(*) as user_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY merchant_id), 2) as percentage,
    AVG(F) as avg_frequency,
    AVG(M) as avg_monetary
FROM rfm_scores
GROUP BY merchant_id, user_segment
ORDER BY merchant_id, user_count DESC;
```

**数据表设计参考**：

```sql
-- RFM分析结果表
CREATE TABLE user_rfm_analysis (
    id VARCHAR(32) PRIMARY KEY,
    merchant_id VARCHAR(32) NOT NULL,
    user_id VARCHAR(32) NOT NULL,
    analysis_date DATE NOT NULL COMMENT '分析基准日期',
    stat_days INT DEFAULT 90 COMMENT '统计周期天数',
    R_value INT COMMENT 'R值（距今天数）',
    F_value INT COMMENT 'F值（使用频次）',
    M_value INT COMMENT 'M值（积分贡献）',
    R_score TINYINT COMMENT 'R评分 1-5',
    F_score TINYINT COMMENT 'F评分 1-5',
    M_score TINYINT COMMENT 'M评分 1-5',
    RFM_code VARCHAR(10) COMMENT 'RFM组合码',
    user_segment VARCHAR(50) COMMENT '用户分群',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_date (user_id, analysis_date),
    INDEX idx_merchant_segment (merchant_id, user_segment)
) COMMENT '用户RFM分析表';

-- 定时任务建议：每日凌晨计算一次
```

---

## 三、功能需求

### 3.1 核心功能列表

| 功能编号 | 功能名称 | 功能描述 | 优先级 |
|----------|----------|----------|--------|
| F-001 | 商户数据导出API | 提供商户基础信息接口 | P0 |
| F-002 | 用户数据统计API | 提供用户相关统计数据接口 | P0 |
| F-003 | 使用记录查询API | 提供使用/关闭记录查询接口 | P0 |
| F-004 | 上座率计算服务 | 自动计算各周期上座率 | P0 |
| F-005 | 到店频次统计API | 提供用户到店频次数据 | P0 |
| F-006 | 停留时长统计API | 提供用户停留时长数据 | P0 |
| F-007 | 积分转化分析API | 提供用户积分获取/消耗/转化数据 | P0 |
| F-010 | RFM用户价值分析API | 提供用户RFM分层和价值分析 | P1 |
| F-008 | 月度数据报告生成 | 自动生成月度数据报告 | P1 |
| F-009 | 数据同步飞书 | 支持定时同步飞书多维表格 | P1 |

### 3.2 功能详细说明

#### F-001：商户数据导出API

**接口路径**：`GET /api/v1/merchants/export`

**请求参数**：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| merchant_id | string | 否 | 商户ID，不传则返回全部 |
| fields | string | 否 | 导出字段，逗号分隔 |

**返回字段**：
```json
{
    "code": 0,
    "data": [{
        "merchant_id": "M001",
        "merchant_name": "武昌万象城XX球房",
        "city": "武汉市",
        "address": "武昌区XX路XX号",
        "table_count": 20,
        "area_sqm": 800,
        "contact_name": "张老板",
        "contact_phone": "138xxxx",
        "join_date": "2025-09-01",
        "join_days": 180
    }]
}
```

---

#### F-002：用户数据统计API

**接口路径**：`GET /api/v1/merchants/{merchant_id}/users/stats`

**请求参数**：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| start_date | string | 是 | 统计开始日期 YYYY-MM-DD |
| end_date | string | 是 | 统计结束日期 YYYY-MM-DD |
| group_by | string | 否 | 统计粒度：day(按日)/week(按周)/month(按月)，默认month |

**返回字段（默认按月）**：
```json
{
    "code": 0,
    "data": {
        "merchant_id": "M001",
        "period": {
            "start": "2025-09-01",
            "end": "2025-12-01",
            "days": 92
        },
        "group_by": "month",
        "user_stats": {
            "total_registered": 1200,
            "monthly_active": 684,
            "active_rate": 57.0,
            "total_visits": 2400,
            "daily_avg_visits": 26.1,
            "new_users": 700,
            "retention_30d": 45.0
        }
    }
}
```

**返回字段（按日/按周）**：
```json
{
    "code": 0,
    "data": {
        "merchant_id": "M001",
        "period": {
            "start": "2025-09-01",
            "end": "2025-09-30"
        },
        "group_by": "day",
        "daily_stats": [{
            "date": "2025-09-01",
            "day_of_week": "周一",
            "new_users": 25,
            "active_users": 120,
            "total_visits": 350,
            "new_user_rate": 20.8
        }],
        "weekly_stats": [{
            "week_start": "2025-09-01",
            "week_end": "2025-09-07",
            "week_num": 36,
            "new_users": 156,
            "active_users": 580,
            "total_visits": 2100,
            "growth_rate": 5.2
        }]
    }
}
```

---

#### F-003：使用记录查询API

**接口路径**：`GET /api/v1/merchants/{merchant_id}/usage-records`

**请求参数**：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| start_date | string | 是 | 开始日期 |
| end_date | string | 是 | 结束日期 |
| user_id | string | 否 | 用户ID筛选 |
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页条数，默认50 |

**返回字段**：
```json
{
    "code": 0,
    "data": {
        "records": [{
            "record_id": "R001",
            "user_id": "U001",
            "table_id": "T001",
            "use_start_time": "2025-10-15 14:30:00",
            "use_end_time": "2025-10-15 17:45:00",
            "duration_minutes": 195
        }],
        "pagination": {
            "page": 1,
            "page_size": 50,
            "total": 1200
        }
    }
}
```

---

#### F-004：上座率计算服务

**接口路径**：`GET /api/v1/merchants/{merchant_id}/occupancy-rate`

**请求参数**：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| start_date | string | 是 | 开始日期 |
| end_date | string | 是 | 结束日期 |
| day_type | string | 否 | weekday(工作日)/weekend(周末)/all(全部)，默认all |

**返回字段**：
```json
{
    "code": 0,
    "data": {
        "merchant_id": "M001",
        "period": {
            "start": "2025-09-01",
            "end": "2025-12-01",
            "days": 92
        },
        "config": {
            "table_count": 20,
            "daily_business_hours": {
                "start": "10:00",
                "end": "02:00",
                "minutes_per_day": 960
            }
        },
        "occupancy": {
            "workday": {
                "days": 66,
                "actual_minutes": 897600,
                "available_minutes": 1267200,
                "rate": 70.8
            },
            "weekend": {
                "days": 26,
                "actual_minutes": 421200,
                "available_minutes": 499200,
                "rate": 84.4
            },
            "overall": {
                "actual_minutes": 1318800,
                "available_minutes": 1766400,
                "rate": 74.7
            }
        }
    }
}
```

---

#### F-005：到店频次统计API

**接口路径**：`GET /api/v1/merchants/{merchant_id}/visit-frequency`

**请求参数**：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| start_date | string | 是 | 开始日期 |
| end_date | string | 是 | 结束日期 |
| group_by | string | 否 | 统计粒度：day/week/month，默认month |

**返回字段（按月）**：
```json
{
    "code": 0,
    "data": {
        "merchant_id": "M001",
        "period": "2025-09-01 to 2025-12-01",
        "group_by": "month",
        "summary": {
            "total_visits": 2400,
            "active_users": 684,
            "avg_frequency_per_user": 3.5,
            "avg_frequency_per_month": 1.17
        },
        "user_distribution": [{
            "frequency_range": "1-2次",
            "user_count": 200,
            "percentage": 29.2
        }]
    }
}
```

**返回字段（按日/按周）**：
```json
{
    "code": 0,
    "data": {
        "merchant_id": "M001",
        "period": "2025-09-01 to 2025-09-30",
        "group_by": "day",
        "daily_stats": [{
            "date": "2025-09-01",
            "day_of_week": "周一",
            "total_visits": 120,
            "active_users": 85,
            "avg_frequency": 1.41
        }],
        "weekly_stats": [{
            "week_start": "2025-09-01",
            "week_end": "2025-09-07",
            "total_visits": 850,
            "active_users": 420,
            "avg_frequency": 2.02,
            "growth_rate": 8.5
        }]
    }
}
```

---

#### F-006：停留时长统计API

**接口路径**：`GET /api/v1/merchants/{merchant_id}/stay-duration`

**请求参数**：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| start_date | string | 是 | 开始日期 |
| end_date | string | 是 | 结束日期 |
| group_by | string | 否 | 统计粒度：day/week/month，默认month |

**返回字段（按月）**：
```json
{
    "code": 0,
    "data": {
        "merchant_id": "M001",
        "period": "2025-09-01 to 2025-12-01",
        "group_by": "month",
        "summary": {
            "total_duration_minutes": 468000,
            "total_visits": 2400,
            "avg_stay_minutes": 195,
            "median_stay_minutes": 180
        },
        "distribution": [{
            "range": "0-1小时",
            "count": 240,
            "percentage": 10.0
        }]
    }
}
```

**返回字段（按日/按周）**：
```json
{
    "code": 0,
    "data": {
        "merchant_id": "M001",
        "period": "2025-09-01 to 2025-09-30",
        "group_by": "day",
        "daily_stats": [{
            "date": "2025-09-01",
            "day_of_week": "周一",
            "total_visits": 120,
            "avg_stay_minutes": 188,
            "total_stay_minutes": 22560
        }],
        "weekly_stats": [{
            "week_start": "2025-09-01",
            "week_end": "2025-09-07",
            "total_visits": 850,
            "avg_stay_minutes": 192,
            "total_stay_minutes": 163200,
            "growth_rate": 3.2
        }]
    }
}
```

---

#### F-007：积分转化分析API

**接口路径**：`GET /api/v1/merchants/{merchant_id}/points`

**请求参数**：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| start_date | string | 是 | 开始日期 |
| end_date | string | 是 | 结束日期 |
| group_by | string | 否 | 统计粒度：day/week/month，默认month |

**返回字段（按月）**：
```json
{
    "code": 0,
    "data": {
        "merchant_id": "M001",
        "period": {
            "start": "2025-09-01",
            "end": "2025-12-01"
        },
        "group_by": "month",
        "earn_stats": {
            "total_users": 684,
            "total_points_earned": 136800,
            "avg_points_per_user": 200,
            "distribution": {
                "login": 34200,
                "competition": 68400,
                "rank": 20520,
                "task": 10200,
                "invite": 3480
            }
        },
        "consume_stats": {
            "total_users": 342,
            "total_points_consumed": 68400,
            "avg_points_per_user": 200,
            "conversion_rate": 50.0,
            "distribution": {
                "redeem": 41040,
                "offset": 20520,
                "lottery": 6840,
                "upgrade": 0
            }
        },
        "balance_summary": {
            "total_balance": 68400,
            "avg_balance_per_user": 100,
            "users_with_balance": 500,
            "users_zero_balance": 184
        }
    }
}
```

**返回字段（按日/按周）**：
```json
{
    "code": 0,
    "data": {
        "merchant_id": "M001",
        "period": {
            "start": "2025-09-01",
            "end": "2025-09-30"
        },
        "group_by": "day",
        "daily_stats": [{
            "date": "2025-09-01",
            "day_of_week": "周一",
            "users_earned": 85,
            "points_earned": 4250,
            "users_consumed": 42,
            "points_consumed": 2100,
            "conversion_rate": 49.4
        }],
        "weekly_stats": [{
            "week_start": "2025-09-01",
            "week_end": "2025-09-07",
            "users_earned": 520,
            "points_earned": 31200,
            "users_consumed": 280,
            "points_consumed": 16800,
            "conversion_rate": 53.8,
            "growth_rate": 5.2
        }]
    }
}
```

---

#### F-010：RFM用户价值分析API

**接口路径**：`GET /api/v1/merchants/{merchant_id}/rfm`

**请求参数**：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| analysis_date | string | 否 | 分析基准日期，默认当天 |
| stat_days | int | 否 | 统计周期天数，默认90天 |

**返回字段**：
```json
{
    "code": 0,
    "data": {
        "merchant_id": "M001",
        "analysis_date": "2026-03-20",
        "stat_days": 90,
        "overview": {
            "total_users": 1200,
            "avg_R": 15.5,
            "avg_F": 4.2,
            "avg_M": 856.3
        },
        "segments": {
            "重要价值用户": {
                "count": 120,
                "percentage": 10.0,
                "avg_R": 5.2,
                "avg_F": 8.5,
                "avg_M": 2560.0
            },
            "重要保持用户": {
                "count": 84,
                "percentage": 7.0,
                "avg_R": 45.3,
                "avg_F": 6.2,
                "avg_M": 1820.0
            },
            "重要发展用户": {
                "count": 168,
                "percentage": 14.0,
                "avg_R": 3.8,
                "avg_F": 2.1,
                "avg_M": 1540.0
            },
            "重要挽留用户": {
                "count": 96,
                "percentage": 8.0,
                "avg_R": 62.5,
                "avg_F": 1.8,
                "avg_M": 1280.0
            },
            "一般价值用户": {
                "count": 192,
                "percentage": 16.0,
                "avg_R": 8.2,
                "avg_F": 5.5,
                "avg_M": 420.0
            },
            "一般用户": {
                "count": 540,
                "percentage": 45.0,
                "avg_R": 22.6,
                "avg_F": 2.8,
                "avg_M": 180.0
            }
        },
        "action_suggestions": {
            "重要价值用户": "保持服务，提供专属权益",
            "重要保持用户": "推送召回活动，送积分奖励",
            "重要发展用户": "引导更多参与，送比赛优惠券",
            "重要挽留用户": "定向触达，送大额新人积分",
            "一般价值用户": "推送积分消耗活动",
            "一般用户": "引导参与基础活动"
        }
    }
}
```

**接口路径（用户明细）**：`GET /api/v1/merchants/{merchant_id}/rfm/users`

**返回字段（用户明细）**：
```json
{
    "code": 0,
    "data": {
        "users": [{
            "user_id": "U001",
            "R_value": 5,
            "F_value": 12,
            "M_value": 2560,
            "R_score": 5,
            "F_score": 5,
            "M_score": 5,
            "RFM_code": "555",
            "user_segment": "重要价值用户",
            "last_action_time": "2026-03-15 14:30:00"
        }],
        "pagination": {
            "page": 1,
            "page_size": 50,
            "total": 1200
        }
    }
}
```

---

#### F-008：月度数据报告生成

**接口路径**：`POST /api/v1/merchants/{merchant_id}/reports/monthly`

**请求参数**：
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| year_month | string | 是 | 报表月份 YYYY-MM |

**返回字段**：
```json
{
    "code": 0,
    "data": {
        "report_id": "RPT-202603",
        "merchant_id": "M001",
        "report_month": "2026-03",
        "generated_at": "2026-04-01 00:05:00",
        "sections": {
            "user_stats": { /* 同F-002 */ },
            "occupancy": { /* 同F-004 */ },
            "visit_frequency": { /* 同F-005 */ },
            "stay_duration": { /* 同F-006 */ },
            "conversion": { /* 同F-007 */ }
        },
        "comparisons": {
            "vs_last_month": { /* 环比数据 */ },
            "vs_same_period_last_year": { /* 同比数据 */ }
        }
    }
}
```

---

#### F-009：数据同步飞书

**接口路径**：`POST /api/v1/integrations/feishu/sync`

**功能说明**：
- 支持定时任务触发（建议每日凌晨2:00）
- 将指定商户的关键数据同步至飞书多维表格
- 支持增量同步和全量同步

**请求参数**：
```json
{
    "merchant_ids": ["M001", "M002"],
    "sync_type": "incremental",
    "tables": ["user_stats", "occupancy", "monthly_report"]
}
```

---

## 四、数据模型设计

### 4.1 核心数据表

#### 4.1.1 商户基础信息表 (merchants)

```sql
CREATE TABLE merchants (
    id VARCHAR(32) PRIMARY KEY COMMENT '商户ID',
    name VARCHAR(100) NOT NULL COMMENT '商户名称',
    short_name VARCHAR(50) COMMENT '对外简称',
    city VARCHAR(50) COMMENT '城市',
    district VARCHAR(50) COMMENT '区县',
    address VARCHAR(200) COMMENT '详细地址',
    longitude DECIMAL(10, 6) COMMENT '经度',
    latitude DECIMAL(10, 6) COMMENT '纬度',
    table_count INT DEFAULT 0 COMMENT '球桌数量',
    area_sqm INT COMMENT '经营面积平方米',
    contact_name VARCHAR(50) COMMENT '联系人',
    contact_phone VARCHAR(20) COMMENT '联系电话',
    join_date DATE COMMENT '接入日期',
    status TINYINT DEFAULT 1 COMMENT '状态：0停用1正常',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '商户基础信息表';
```

#### 4.1.2 用户表 (users)

```sql
CREATE TABLE users (
    id VARCHAR(32) PRIMARY KEY COMMENT '用户ID',
    merchant_id VARCHAR(32) NOT NULL COMMENT '商户ID',
    nickname VARCHAR(50) COMMENT '昵称',
    phone VARCHAR(20) COMMENT '手机号',
    first_visit_time DATETIME COMMENT '首次到店时间',
    total_visits INT DEFAULT 0 COMMENT '累计到店次数',
    total_duration INT DEFAULT 0 COMMENT '累计停留时长(分钟)',
    last_visit_time DATETIME COMMENT '最后到店时间',
    status TINYINT DEFAULT 1 COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_merchant_id (merchant_id),
    INDEX idx_first_visit (first_visit_time),
    INDEX idx_last_visit (last_visit_time)
) COMMENT '用户表';
```

#### 4.1.3 使用记录表 (usage_records)

```sql
CREATE TABLE usage_records (
    id VARCHAR(32) PRIMARY KEY COMMENT '记录ID',
    merchant_id VARCHAR(32) NOT NULL COMMENT '商户ID',
    user_id VARCHAR(32) COMMENT '用户ID',
    table_id VARCHAR(32) NOT NULL COMMENT '球桌ID',
    use_start_time DATETIME NOT NULL COMMENT '使用开始时间',
    use_end_time DATETIME COMMENT '使用结束时间',
    duration_minutes INT COMMENT '使用时长(分钟)',
    source VARCHAR(20) DEFAULT 'offline' COMMENT '来源：offline/online',
    status TINYINT DEFAULT 1 COMMENT '状态：1使用中2已结束3已取消',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_merchant_date (merchant_id, use_start_time),
    INDEX idx_user_date (user_id, use_start_time),
    INDEX idx_table_date (table_id, use_start_time)
) COMMENT '使用记录表';
```

#### 4.1.4 登录日志表 (login_logs)

```sql
CREATE TABLE login_logs (
    id VARCHAR(32) PRIMARY KEY,
    merchant_id VARCHAR(32) NOT NULL,
    user_id VARCHAR(32) NOT NULL,
    login_time DATETIME NOT NULL,
    login_type VARCHAR(20) COMMENT 'login/scan/active',
    device_info VARCHAR(200) COMMENT '设备信息',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_date (user_id, login_time),
    INDEX idx_merchant_date (merchant_id, login_time)
) COMMENT '登录日志表';
```

#### 4.1.5 赛事参与表 (competition_participants)

```sql
CREATE TABLE competition_participants (
    id VARCHAR(32) PRIMARY KEY,
    merchant_id VARCHAR(32) NOT NULL,
    user_id VARCHAR(32) NOT NULL,
    competition_id VARCHAR(32) NOT NULL,
    competition_name VARCHAR(100) COMMENT '赛事名称',
    competition_type VARCHAR(20) COMMENT 'daily/weekly/monthly/season',
    participation_time DATETIME NOT NULL,
    rank INT COMMENT '排名',
    score INT COMMENT '得分',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_merchant_date (merchant_id, participation_time),
    INDEX idx_user_date (user_id, participation_time)
) COMMENT '赛事参与表';
```

### 4.2 数据统计表（月度汇总）

```sql
CREATE TABLE merchant_monthly_stats (
    id VARCHAR(32) PRIMARY KEY,
    merchant_id VARCHAR(32) NOT NULL,
    stat_month VARCHAR(7) NOT NULL COMMENT '统计月份 YYYY-MM',
    total_registered INT DEFAULT 0 COMMENT '累计注册用户',
    monthly_active INT DEFAULT 0 COMMENT '月活用户',
    active_rate DECIMAL(5, 2) COMMENT '活跃率',
    total_visits INT DEFAULT 0 COMMENT '月度到店次数',
    avg_frequency DECIMAL(5, 2) COMMENT '人均到店频次',
    avg_stay_minutes INT COMMENT '平均停留时长',
    workday_occupancy DECIMAL(5, 2) COMMENT '工作日上座率',
    weekend_occupancy DECIMAL(5, 2) COMMENT '周末上座率',
    overall_occupancy DECIMAL(5, 2) COMMENT '整体上座率',
    conversion_rate DECIMAL(5, 2) COMMENT '二次转化率',
    total_revenue DECIMAL(12, 2) COMMENT '营收(如有)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_merchant_month (merchant_id, stat_month)
) COMMENT '商户月度统计表';
```

---

## 五、技术实现要求

### 5.1 性能要求

| 指标 | 要求 |
|------|------|
| API响应时间 | P99 < 500ms |
| 数据导出(单商户1年数据) | < 5秒 |
| 月度报告生成 | < 30秒 |
| 定时同步任务 | 支持100+商户并发 |

### 5.2 数据更新频率

| 数据类型 | 更新频率 | 说明 |
|----------|----------|------|
| 实时数据 | 实时 | 使用记录、登录日志 |
| 日统计 | 每日凌晨 | 用户活跃、使用统计 |
| 月统计 | 每月1日 | 月度汇总报表 |
| 留存分析 | 每日凌晨 | 30日留存率 |

### 5.3 数据导出格式

支持导出格式：
- JSON（API默认）
- CSV（数据导出）
- Excel（报告导出）

---

## 六、飞书集成方案

### 6.1 飞书多维表格同步策略

| 数据表 | 同步方式 | 同步频率 | 同步字段 |
|--------|----------|----------|----------|
| 商户基础信息 | 全量同步 | 按需 | 全部字段 |
| 用户数据 | 增量同步 | 每日 | 用户统计、活跃数据 |
| 效果对比 | 增量同步 | 每日 | 上座率、频次、停留时长 |
| 活动数据 | 实时同步 | 活动后 | 活动统计 |

### 6.2 飞书字段映射

| 杆杆响字段 | 飞书字段 | 数据类型 | 映射关系 |
|------------|----------|----------|----------|
| merchant.name | 球房名称 | 文本 | 1:1 |
| total_registered | 注册用户总数 | 数字 | 1:1 |
| monthly_active | 月活用户数 | 数字 | 1:1 |
| active_rate | 活跃率 | 数字 | 公式=月活/注册 |
| workday_occupancy | 工作日上座率 | 数字 | 1:1 |
| avg_frequency | 月均到店频次 | 数字 | 1:1 |
| avg_stay_minutes | 平均停留时长 | 数字 | 1:1 |
| conversion_rate | 二次转化率 | 数字 | 1:1 |

---

## 七、验收标准

### 7.1 功能验收

| 功能编号 | 验收标准 | 测试方法 |
|----------|----------|----------|
| F-001 | 返回商户基础信息正确 | 调用接口验证字段 |
| F-002 | 用户统计数据准确 | 与后台数据交叉验证 |
| F-003 | 使用记录完整 | 对比数据库记录数 |
| F-004 | 上座率计算正确 | 人工核算验证 |
| F-005 | 到店频次统计准确 | 抽样用户核对 |
| F-006 | 停留时长数据正确 | 抽样记录验证 |
| F-007 | 积分获取/消耗数据准确 | 与积分流水交叉验证 |
| F-008 | 月报数据完整 | 检查所有字段 |
| F-009 | 飞书同步成功 | 飞书表格数据验证 |
| F-010 | RFM分群计算正确 | 抽样验证用户分群结果 |

### 7.2 性能验收

| 指标 | 验收标准 | 测试方法 |
|------|----------|----------|
| API响应 | P99 < 500ms | JMeter压测 |
| 数据导出 | < 5秒 | 计时验证 |
| 定时任务 | 执行成功 | 查看执行日志 |

### 7.3 数据准确性验收

- 上座率数据与收银系统数据误差 < 5%
- 用户数与实际注册数100%一致
- 停留时长与原始记录误差 < 1分钟

---

## 八、里程碑计划

| 阶段 | 内容 | 交付物 | 预计工时 |
|------|------|--------|----------|
| Phase 1 | 核心API开发 | F-001 ~ F-007 | 5人日 |
| Phase 2 | 月报生成功能 | F-008 | 2人日 |
| Phase 3 | 飞书集成 | F-009 | 3人日 |
| Phase 4 | 测试与优化 | 全部 | 3人日 |
| **合计** | | | **13人日** |

---

## 九、附录

### 9.1 术语表

| 术语 | 定义 |
|------|------|
| 上座率 | 球桌被使用时长占总可用时长的比例 |
| 月活用户 | 当月有登录或使用行为的去重用户数 |
| 30日留存率 | 当日新增用户在第30天仍有活跃的比例 |
| 积分转化率 | 有积分消耗的用户数 / 获得积分用户数 × 100% |
| Cohort分析 | 按用户首次到访时间分组进行的留存分析 |
| R值 | 用户最近一次使用天梯赛的距今天数 |
| F值 | 用户使用天梯赛的频率（使用次数） |
| M值 | 用户对天梯赛的参与深度（积分获取量） |
| RFM评分 | 根据R/F/M值分布计算的1-5分评分 |
| RFM分群 | 根据RFM评分组合判定的用户类型 |

### 9.2 参考文档

- 飞书多维表格API文档
- 杆杆响数据库设计文档
- 天梯赛案例模板V1.0

---

**文档编制**：杆杆响产品团队
**联系方式**：如有疑问请联系产品经理
**每一杆，都有回响**