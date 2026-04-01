# -*- coding: utf-8 -*-
import json

# 球馆账号
accounts = {
    'qiaoshi': {'password': 'qiaoshi123', 'venue': '乔氏台球俱乐部'},
    'taiqiu': {'password': 'taiqiu123', 'venue': '台球帝国'},
    'xingji': {'password': 'xingji123', 'venue': '星际台球'},
    'jiuqiu': {'password': 'jiuqiu123', 'venue': '九球台球俱乐部'},
    'mingshi': {'password': 'mingshi123', 'venue': '名仕台球'},
    'jinzue': {'password': 'jinzue123', 'venue': '金爵台球俱乐部'},
    'haoting': {'password': 'haoting123', 'venue': '豪庭台球俱乐部'},
    'dianfeng': {'password': 'dianfeng123', 'venue': '巅峰台球'},
    'fengyun': {'password': 'fengyun123', 'venue': '风云台球会所'},
    'yipin': {'password': 'yipin123', 'venue': '壹品台球'},
    'manishikong': {'password': 'manishikong123', 'venue': '乌达区慢时空台球厅'},
    'wuchang': {'password': 'wuchang123', 'venue': '武昌万象城八楼名仕台球'},
    'bojue': {'password': 'bojue123', 'venue': '伯爵台球会所'},
    'tiangong': {'password': 'tiangong123', 'venue': '天工台球城'},
    'wangzhe': {'password': 'wangzhe123', 'venue': '王者台球俱乐部'},
    'shenshi': {'password': 'shenshi123', 'venue': '绅士台球俱乐部'},
    'guanjun': {'password': 'guanjun123', 'venue': '冠军台球馆'},
    'xingyun': {'password': 'xingyun123', 'venue': '星云台球'},
    'heiba': {'password': 'heiba123', 'venue': '黑八台球城'},
    'xingpai': {'password': 'xingpai123', 'venue': '星牌台球会所'}
}

# 读取数据
with open('demo_data.js', 'r', encoding='utf-8') as f:
    data_js = f.read()

# 读取看板HTML
with open('球房老板看板_v2.html', 'r', encoding='utf-8') as f:
    dashboard = f.read()

# 创建单文件版本
html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>球房数据看板</title>
    <script src="https://unpkg.com/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
            color: #fff;
            min-height: 100vh;
            font-size: 16px;
        }

        /* 登录页面 */
        .login-page {
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .login-page.hidden { display: none; }
        .login-box {
            background: rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 40px 50px;
            width: 400px;
            border: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }
        .login-logo { text-align: center; margin-bottom: 30px; }
        .login-logo h1 { color: #2ECC71; font-size: 28px; margin-bottom: 8px; }
        .login-logo p { color: #888; font-size: 14px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; color: #ccc; font-size: 14px; margin-bottom: 8px; }
        .form-group input {
            width: 100%; padding: 14px 18px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            color: #fff; font-size: 16px;
        }
        .form-group input:focus { outline: none; border-color: #2ECC71; }
        .form-group input::placeholder { color: #666; }
        .login-btn {
            width: 100%; padding: 16px;
            background: linear-gradient(90deg, #2ECC71 0%, #27AE60 100%);
            border: none; border-radius: 10px;
            color: #fff; font-size: 18px; font-weight: bold;
            cursor: pointer;
        }
        .login-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(46,204,113,0.4); }
        .login-error { color: #E74C3C; font-size: 14px; text-align: center; margin-top: 15px; display: none; }
        .login-error.show { display: block; }

        /* 看板页面 */
        .dashboard-page { padding: 25px; display: none; }
        .dashboard-page.active { display: block; }

        .header {
            background: linear-gradient(90deg, #2ECC71 0%, #27AE60 100%);
            border-radius: 16px;
            padding: 25px 30px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 20px rgba(46, 204, 113, 0.3);
        }
        .header h1 { font-size: 32px; font-weight: bold; text-shadow: 0 2px 4px rgba(0,0,0,0.2); }
        .venue-name { font-size: 22px; color: #FFD700; margin-top: 8px; font-weight: bold; }
        .header-info { text-align: right; }
        .header-info p { opacity: 0.95; font-size: 16px; line-height: 1.8; }
        .logout-btn {
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.3);
            color: #fff;
            padding: 8px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 10px;
        }
        .logout-btn:hover { background: rgba(231, 76, 60, 0.3); border-color: #E74C3C; }

        .filter-bar {
            background: rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 18px 25px;
            margin-bottom: 25px;
            display: flex;
            gap: 25px;
            align-items: center;
            flex-wrap: wrap;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .filter-bar label { color: #ccc; font-size: 16px; font-weight: 500; }
        .filter-bar select {
            background: rgba(255,255,255,0.15);
            border: 1px solid rgba(255,255,255,0.25);
            color: #fff;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 15px;
            min-width: 150px;
        }
        .filter-bar select option { background: #1a1a2e; }

        .stats-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 20px; margin-bottom: 25px; }
        .stat-card {
            background: rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 25px 20px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .stat-card .value { font-size: 42px; font-weight: bold; color: #2ECC71; line-height: 1.2; }
        .stat-card .label { color: #bbb; margin-top: 10px; font-size: 15px; font-weight: 500; }
        .stat-card.highlight {
            background: linear-gradient(135deg, rgba(46,204,113,0.25), rgba(39,174,96,0.25));
            border: 2px solid #2ECC71;
        }
        .stat-card.highlight .value { color: #FFD700; }

        .charts-row { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 25px; }
        .chart-card {
            background: rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .chart-title {
            font-size: 20px;
            margin-bottom: 20px;
            padding-left: 15px;
            border-left: 4px solid #2ECC71;
            font-weight: 600;
            color: #fff;
        }
        .chart-container { height: 320px; }

        .table-section {
            background: rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .table-scroll { max-height: 400px; overflow-y: auto; }
        table { width: 100%; border-collapse: collapse; }
        th {
            background: rgba(46,204,113,0.25);
            padding: 15px 12px;
            text-align: left;
            font-size: 15px;
            font-weight: 600;
            color: #fff;
            position: sticky;
            top: 0;
        }
        td {
            padding: 14px 12px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            font-size: 15px;
            color: #e0e0e0;
        }
        tr:hover { background: rgba(255,255,255,0.05); }

        .rank-tag {
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: bold;
            display: inline-block;
        }
        .rank-king { background: linear-gradient(135deg, #FFD700, #FFA500); color: #000; }
        .rank-diamond { background: linear-gradient(135deg, #00CED1, #20B2AA); color: #000; }
        .rank-platinum { background: linear-gradient(135deg, #E6E6FA, #B0C4DE); color: #000; }
        .rank-gold { background: linear-gradient(135deg, #FFD700, #DAA520); color: #000; }
        .rank-silver { background: linear-gradient(135deg, #C0C0C0, #A9A9A9); color: #000; }
        .rank-bronze { background: linear-gradient(135deg, #CD7F32, #8B4513); color: #fff; }
        .rank-star { background: linear-gradient(135deg, #9932CC, #8B008B); color: #fff; }

        .segment-tag {
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 13px;
            display: inline-block;
        }
        .seg-vip { background: #FFD700; color: #000; font-weight: bold; }
        .seg-active { background: #00C853; color: #fff; }
        .seg-potential { background: #2196F3; color: #fff; }
        .seg-risk { background: #FF9800; color: #fff; }
        .seg-normal { background: #9E9E9E; color: #fff; }

        .segment-cards { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; margin-bottom: 20px; }
        .seg-card {
            background: rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 20px 15px;
            text-align: center;
            border-left: 5px solid;
            cursor: pointer;
        }
        .seg-card.vip { border-color: #FFD700; }
        .seg-card.active { border-color: #00C853; }
        .seg-card.potential { border-color: #2196F3; }
        .seg-card.risk { border-color: #FF9800; }
        .seg-card.normal { border-color: #9E9E9E; }
        .seg-card .count { font-size: 32px; font-weight: bold; color: #2ECC71; }
        .seg-card .name { font-size: 15px; color: #ccc; margin-top: 8px; }
        .seg-card .percent { font-size: 14px; color: #888; margin-top: 4px; }

        .table-scroll::-webkit-scrollbar { width: 8px; }
        .table-scroll::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); border-radius: 4px; }
        .table-scroll::-webkit-scrollbar-thumb { background: rgba(46,204,113,0.5); border-radius: 4px; }

        @media (max-width: 1400px) {
            .stats-grid { grid-template-columns: repeat(3, 1fr); }
            .segment-cards { grid-template-columns: repeat(3, 1fr); }
        }
        @media (max-width: 1000px) {
            .charts-row { grid-template-columns: 1fr; }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .segment-cards { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <!-- 登录页面 -->
    <div class="login-page" id="loginPage">
        <div class="login-box">
            <div class="login-logo">
                <h1>球房数据看板</h1>
                <p>请登录查看您的球房数据</p>
            </div>
            <form id="loginForm">
                <div class="form-group">
                    <label>账号</label>
                    <input type="text" id="username" placeholder="请输入账号" required>
                </div>
                <div class="form-group">
                    <label>密码</label>
                    <input type="password" id="password" placeholder="请输入密码" required>
                </div>
                <button type="submit" class="login-btn">登 录</button>
                <p class="login-error" id="loginError">账号或密码错误</p>
            </form>
        </div>
    </div>

    <!-- 看板页面 -->
    <div class="dashboard-page" id="dashboardPage">
        <div class="header">
            <div>
                <h1>球房数据看板</h1>
                <div class="venue-name" id="venueNameDisplay">--</div>
            </div>
            <div class="header-info">
                <p>数据时间：2026年3月</p>
                <p id="updateTime">更新时间：--</p>
                <button class="logout-btn" onclick="logout()">退出登录</button>
            </div>
        </div>

        <div class="filter-bar">
            <div>
                <label>段位：</label>
                <select id="rankFilter" onchange="filterData()">
                    <option value="">全部段位</option>
                    <option value="传奇杆王">传奇杆王</option>
                    <option value="荣耀杆王">荣耀杆王</option>
                    <option value="无双杆王">无双杆王</option>
                    <option value="最强杆王">最强杆王</option>
                    <option value="清台星耀">清台星耀</option>
                    <option value="校球钻石">校球钻石</option>
                    <option value="加塞铂金">加塞铂金</option>
                    <option value="走位黄金">走位黄金</option>
                    <option value="推杆白银">推杆白银</option>
                    <option value="沉稳青铜">沉稳青铜</option>
                </select>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="value" id="totalUsers">--</div>
                <div class="label">本店用户数</div>
            </div>
            <div class="stat-card">
                <div class="value" id="activeUsers">--</div>
                <div class="label">本店月活跃</div>
            </div>
            <div class="stat-card">
                <div class="value" id="totalGames">--</div>
                <div class="label">本店总场次</div>
            </div>
            <div class="stat-card">
                <div class="value" id="avgWinRate">--</div>
                <div class="label">本店平均胜率</div>
            </div>
            <div class="stat-card">
                <div class="value" id="maxStreak">--</div>
                <div class="label">本店最高连胜</div>
            </div>
            <div class="stat-card highlight">
                <div class="value" id="regionRank">--</div>
                <div class="label">区域排名</div>
            </div>
        </div>

        <div class="charts-row">
            <div class="chart-card">
                <div class="chart-title">本店段位分布</div>
                <div class="chart-container" id="rankChart"></div>
            </div>
            <div class="chart-card">
                <div class="chart-title">用户分层</div>
                <div>
                    <div class="segment-cards">
                        <div class="seg-card vip" onclick="showSegment('核心用户')">
                            <div class="count" id="segVipCount">--</div>
                            <div class="name">核心用户</div>
                            <div class="percent" id="segVipPercent">--</div>
                        </div>
                        <div class="seg-card active" onclick="showSegment('活跃用户')">
                            <div class="count" id="segActiveCount">--</div>
                            <div class="name">活跃用户</div>
                            <div class="percent" id="segActivePercent">--</div>
                        </div>
                        <div class="seg-card potential" onclick="showSegment('潜力用户')">
                            <div class="count" id="segPotentialCount">--</div>
                            <div class="name">潜力用户</div>
                            <div class="percent" id="segPotentialPercent">--</div>
                        </div>
                        <div class="seg-card risk" onclick="showSegment('流失风险')">
                            <div class="count" id="segRiskCount">--</div>
                            <div class="name">流失风险</div>
                            <div class="percent" id="segRiskPercent">--</div>
                        </div>
                        <div class="seg-card normal" onclick="showSegment('普通用户')">
                            <div class="count" id="segNormalCount">--</div>
                            <div class="name">普通用户</div>
                            <div class="percent" id="segNormalPercent">--</div>
                        </div>
                    </div>
                    <div class="chart-container" id="segmentChart" style="height: 200px;"></div>
                </div>
            </div>
        </div>

        <div class="charts-row">
            <div class="chart-card">
                <div class="chart-title">每日趋势（近30天）</div>
                <div class="chart-container" id="dailyTrendChart"></div>
            </div>
            <div class="chart-card">
                <div class="chart-title">每周趋势（近12周）</div>
                <div class="chart-container" id="weeklyTrendChart"></div>
            </div>
        </div>

        <div class="charts-row">
            <div class="chart-card" style="grid-column: span 2;">
                <div class="chart-title">周边球馆活跃度排名</div>
                <div class="chart-container" id="venueRankChart"></div>
            </div>
        </div>

        <div class="charts-row">
            <div class="chart-card">
                <div class="chart-title">对局模式分布</div>
                <div class="chart-container" id="matchModeChart"></div>
            </div>
            <div class="chart-card">
                <div class="chart-title">对局模式占比</div>
                <div class="chart-container" id="matchModePieChart"></div>
            </div>
        </div>

        <div class="table-section">
            <div class="chart-title">活跃用户 Top20</div>
            <div class="table-scroll">
                <table>
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>用户ID</th>
                            <th>昵称</th>
                            <th>段位</th>
                            <th>积分</th>
                            <th>场次</th>
                            <th>胜率</th>
                            <th>连胜</th>
                            <th>分层</th>
                        </tr>
                    </thead>
                    <tbody id="topUsersTable"></tbody>
                </table>
            </div>
        </div>

        <div class="table-section">
            <div class="chart-title">用户明细</div>
            <div class="table-scroll">
                <table>
                    <thead>
                        <tr>
                            <th>用户ID</th>
                            <th>昵称</th>
                            <th>段位</th>
                            <th>积分</th>
                            <th>场次</th>
                            <th>胜率</th>
                            <th>连胜</th>
                            <th>分层</th>
                        </tr>
                    </thead>
                    <tbody id="userDetailTable"></tbody>
                </table>
            </div>
        </div>

        <div class="table-section">
            <div class="chart-title">积分流水明细</div>
            <div class="table-scroll" style="max-height: 300px;">
                <table>
                    <thead>
                        <tr>
                            <th>流水ID</th>
                            <th>用户ID</th>
                            <th>昵称</th>
                            <th>类型</th>
                            <th>积分变动</th>
                            <th>余额</th>
                            <th>说明</th>
                            <th>时间</th>
                        </tr>
                    </thead>
                    <tbody id="pointsFlowTable"></tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
''' + data_js + '''

        const venueAccounts = ''' + json.dumps(accounts, ensure_ascii=False) + ''';

        let currentVenue = "";
        let allVenueUsers = [];

        // 登录处理
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const user = document.getElementById('username').value.trim();
            const pass = document.getElementById('password').value;

            if (venueAccounts[user] && venueAccounts[user].password === pass) {
                currentVenue = venueAccounts[user].venue;
                sessionStorage.setItem('venueName', currentVenue);
                document.getElementById('loginPage').classList.add('hidden');
                document.getElementById('dashboardPage').classList.add('active');
                document.getElementById('loginError').classList.remove('show');
                initDashboard();
            } else {
                document.getElementById('loginError').classList.add('show');
            }
        });

        // 退出登录
        function logout() {
            sessionStorage.removeItem('venueName');
            currentVenue = "";
            document.getElementById('dashboardPage').classList.remove('active');
            document.getElementById('loginPage').classList.remove('hidden');
            document.getElementById('username').value = "";
            document.getElementById('password').value = "";
        }

        // 检查登录状态
        function checkLogin() {
            const venue = sessionStorage.getItem('venueName');
            if (venue) {
                currentVenue = venue;
                document.getElementById('loginPage').classList.add('hidden');
                document.getElementById('dashboardPage').classList.add('active');
                initDashboard();
            }
        }

        // 初始化看板
        function initDashboard() {
            document.getElementById('venueNameDisplay').textContent = currentVenue;
            document.getElementById('updateTime').textContent = '更新时间: ' + new Date().toLocaleString();

            allVenueUsers = demoData.allUsers.filter(u => u.venue === currentVenue);
            initCharts(allVenueUsers);
            updateDashboard(allVenueUsers);
        }

        // 初始化图表
        function initCharts(venueUsers) {
            // 段位分布
            const rankCounts = {};
            venueUsers.forEach(u => {
                let key;
                if (u.rank.includes('传奇杆王')) key = '传奇杆王';
                else if (u.rank.includes('荣耀杆王')) key = '荣耀杆王';
                else if (u.rank.includes('无双杆王')) key = '无双杆王';
                else if (u.rank.includes('最强杆王')) key = '最强杆王';
                else if (u.rank.includes('星耀')) key = '清台星耀';
                else if (u.rank.includes('钻石')) key = '校球钻石';
                else if (u.rank.includes('铂金')) key = '加塞铂金';
                else if (u.rank.includes('黄金')) key = '走位黄金';
                else if (u.rank.includes('白银')) key = '推杆白银';
                else key = '沉稳青铜';
                rankCounts[key] = (rankCounts[key] || 0) + 1;
            });

            const rankDist = Object.entries(rankCounts).map(([name, value]) => ({
                name, value,
                color: {'传奇杆王':'#FFD700','荣耀杆王':'#FFD700','无双杆王':'#8B0000','最强杆王':'#FF4500','清台星耀':'#9932CC','校球钻石':'#00CED1','加塞铂金':'#E6E6FA','走位黄金':'#FFD700','推杆白银':'#C0C0C0','沉稳青铜':'#CD853F'}[name]
            }));

            echarts.init(document.getElementById('rankChart')).setOption({
                tooltip: { trigger: 'item', formatter: '{b}: {c}人 ({d}%)', textStyle: { fontSize: 14 } },
                legend: { bottom: '0%', textStyle: { color: '#fff', fontSize: 13 }, itemWidth: 12, itemHeight: 12, itemGap: 8 },
                series: [{
                    type: 'pie', radius: ['35%', '55%'], center: ['50%', '42%'],
                    data: rankDist, label: { show: false },
                    emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold' } },
                    labelLine: { show: false }, itemStyle: { borderRadius: 6 }
                }],
                color: ['#CD7F32', '#C0C0C0', '#FFD700', '#00CED1', '#E6E6FA', '#9932CC', '#FF4500', '#8B0000', '#FFD700', '#FFD700']
            });

            // 用户分层饼图
            const segCounts = {};
            venueUsers.forEach(u => { segCounts[u.segment] = (segCounts[u.segment] || 0) + 1; });
            const segments = ['核心用户', '活跃用户', '潜力用户', '流失风险', '普通用户'].map(name => ({
                name, value: segCounts[name] || 0,
                color: {'核心用户':'#FFD700','活跃用户':'#00C853','潜力用户':'#2196F3','流失风险':'#FF9800','普通用户':'#9E9E9E'}[name]
            }));

            echarts.init(document.getElementById('segmentChart')).setOption({
                tooltip: { trigger: 'item', formatter: '{b}: {c}人 ({d}%)', textStyle: { fontSize: 14 } },
                series: [{
                    type: 'pie', radius: ['35%', '60%'],
                    data: segments,
                    label: { show: true, formatter: '{d}%', fontSize: 14, color: '#fff' }
                }]
            });

            // 每日趋势
            echarts.init(document.getElementById('dailyTrendChart')).setOption({
                tooltip: { trigger: 'axis', textStyle: { fontSize: 14 } },
                legend: { data: ['活跃用户', '场次'], textStyle: { color: '#ccc', fontSize: 14 }, top: 0 },
                grid: { top: 50, right: 30, bottom: 60, left: 50 },
                xAxis: { type: 'category', data: demoData.dailyTrend.map(d => d[0]), axisLabel: { fontSize: 12, rotate: 45, color: '#aaa' } },
                yAxis: { type: 'value', axisLabel: { fontSize: 12, color: '#aaa' }, splitLine: { lineStyle: { color: '#333' } } },
                series: [
                    { name: '活跃用户', type: 'line', data: demoData.dailyTrend.map(d => Math.round(d[1] * 0.15)), smooth: true, itemStyle: { color: '#2ECC71' }, lineStyle: { width: 3 }, areaStyle: { color: 'rgba(46, 204, 113, 0.2)' } },
                    { name: '场次', type: 'line', data: demoData.dailyTrend.map(d => Math.round(d[3] * 0.15)), smooth: true, itemStyle: { color: '#F39C12' }, lineStyle: { width: 3 }, areaStyle: { color: 'rgba(243, 156, 18, 0.2)' } }
                ]
            });

            // 每周趋势
            echarts.init(document.getElementById('weeklyTrendChart')).setOption({
                tooltip: { trigger: 'axis', textStyle: { fontSize: 14 } },
                legend: { data: ['场次', '活跃用户'], textStyle: { color: '#ccc', fontSize: 14 }, top: 0 },
                grid: { top: 50, right: 30, bottom: 40, left: 50 },
                xAxis: { type: 'category', data: demoData.weeklyTrend.map(d => d[0]), axisLabel: { fontSize: 12, color: '#aaa' } },
                yAxis: { type: 'value', axisLabel: { fontSize: 12, color: '#aaa' }, splitLine: { lineStyle: { color: '#333' } } },
                series: [
                    { name: '场次', type: 'bar', data: demoData.weeklyTrend.map(d => Math.round(d[2] * 0.15)), itemStyle: { color: '#2ECC71', borderRadius: [4, 4, 0, 0] }, barWidth: 30 },
                    { name: '活跃用户', type: 'line', data: demoData.weeklyTrend.map(d => Math.round(d[3] * 0.15)), smooth: true, itemStyle: { color: '#F39C12' }, lineStyle: { width: 3 } }
                ]
            });

            // 周边球馆排名
            const allVenues = demoData.venues.map((v, i) => ({
                name: v[0], value: v[1],
                isCurrent: v[0].includes(currentVenue.substring(0, 4))
            }));

            echarts.init(document.getElementById('venueRankChart')).setOption({
                tooltip: { trigger: 'axis', textStyle: { fontSize: 14 } },
                grid: { top: 20, right: 80, bottom: 30, left: 150 },
                xAxis: { type: 'value', axisLabel: { fontSize: 12, color: '#aaa' }, splitLine: { lineStyle: { color: '#333' } } },
                yAxis: { type: 'category', data: allVenues.map(v => v.name.substring(0, 12)).reverse(), axisLabel: { fontSize: 13, color: '#ccc' } },
                series: [{
                    type: 'bar',
                    data: allVenues.map(v => ({
                        value: v.value,
                        itemStyle: { color: v.isCurrent ? '#FFD700' : '#2ECC71', borderRadius: [0, 6, 6, 0] }
                    })).reverse(),
                    barWidth: 25,
                    label: { show: true, position: 'right', color: '#fff', fontSize: 13, fontWeight: 'bold' }
                }]
            });

            // 对局模式分布
            const matchModes = demoData.matchModes || [
                {name: "抢5", value: 95000, desc: "先赢5局"},
                {name: "抢7", value: 180000, desc: "先赢7局"},
                {name: "抢9", value: 350000, desc: "17局9胜"},
                {name: "抢11", value: 125000, desc: "先赢11局"},
                {name: "抢13", value: 45000, desc: "先赢13局"}
            ];
            const modeColors = ['#2ECC71', '#3498DB', '#E74C3C', '#F39C12', '#9B59B6'];

            echarts.init(document.getElementById('matchModeChart')).setOption({
                tooltip: { trigger: 'axis', textStyle: { fontSize: 14 } },
                grid: { top: 30, right: 30, bottom: 40, left: 60 },
                xAxis: { type: 'category', data: matchModes.map(m => m.name), axisLabel: { fontSize: 13, color: '#ccc' } },
                yAxis: { type: 'value', axisLabel: { fontSize: 12, color: '#aaa' }, splitLine: { lineStyle: { color: '#333' } } },
                series: [{
                    name: '对局场次', type: 'bar',
                    data: matchModes.map((m, i) => ({
                        value: m.value,
                        itemStyle: { color: modeColors[i], borderRadius: [6, 6, 0, 0] }
                    })),
                    barWidth: 50,
                    label: { show: true, position: 'top', formatter: p => (p.value / 1000).toFixed(0) + 'K', color: '#fff', fontSize: 12 }
                }]
            });

            echarts.init(document.getElementById('matchModePieChart')).setOption({
                tooltip: { trigger: 'item', textStyle: { fontSize: 14 } },
                legend: { orient: 'vertical', right: 10, top: 'center', textStyle: { color: '#ccc', fontSize: 13 } },
                series: [{
                    name: '对局模式', type: 'pie',
                    radius: ['40%', '70%'], center: ['40%', '50%'],
                    itemStyle: { borderRadius: 8, borderColor: '#1a1a2e', borderWidth: 2 },
                    label: { show: true, position: 'outside', formatter: '{b}\\n{d}%', fontSize: 12, color: '#ccc' },
                    data: matchModes.map((m, i) => ({ name: m.name, value: m.value, itemStyle: { color: modeColors[i] } }))
                }]
            });
        }

        function updateDashboard(users) {
            const total = users.length;
            const stats = {
                totalUsers: total,
                activeUsers: users.filter(u => u.segment === '核心用户' || u.segment === '活跃用户').length,
                totalGames: users.reduce((sum, u) => sum + u.games, 0),
                avgWinRate: total > 0 ? (users.reduce((sum, u) => sum + u.winRate, 0) / total).toFixed(1) : 0,
                maxStreak: users.length > 0 ? Math.max(...users.map(u => u.streak || 0)) : 0,
                regionRank: Math.floor(Math.random() * 10) + 1
            };

            document.getElementById('totalUsers').textContent = stats.totalUsers.toLocaleString();
            document.getElementById('activeUsers').textContent = stats.activeUsers.toLocaleString();
            document.getElementById('totalGames').textContent = stats.totalGames >= 1000 ? (stats.totalGames / 1000).toFixed(1) + 'K' : stats.totalGames;
            document.getElementById('avgWinRate').textContent = stats.avgWinRate + '%';
            document.getElementById('maxStreak').textContent = stats.maxStreak;
            document.getElementById('regionRank').textContent = '第' + stats.regionRank + '名';

            const segCounts = {};
            users.forEach(u => { segCounts[u.segment] = (segCounts[u.segment] || 0) + 1; });

            document.getElementById('segVipCount').textContent = segCounts['核心用户'] || 0;
            document.getElementById('segVipPercent').textContent = total > 0 ? ((segCounts['核心用户'] || 0) / total * 100).toFixed(1) + '%' : '0%';
            document.getElementById('segActiveCount').textContent = segCounts['活跃用户'] || 0;
            document.getElementById('segActivePercent').textContent = total > 0 ? ((segCounts['活跃用户'] || 0) / total * 100).toFixed(1) + '%' : '0%';
            document.getElementById('segPotentialCount').textContent = segCounts['潜力用户'] || 0;
            document.getElementById('segPotentialPercent').textContent = total > 0 ? ((segCounts['潜力用户'] || 0) / total * 100).toFixed(1) + '%' : '0%';
            document.getElementById('segRiskCount').textContent = segCounts['流失风险'] || 0;
            document.getElementById('segRiskPercent').textContent = total > 0 ? ((segCounts['流失风险'] || 0) / total * 100).toFixed(1) + '%' : '0%';
            document.getElementById('segNormalCount').textContent = segCounts['普通用户'] || 0;
            document.getElementById('segNormalPercent').textContent = total > 0 ? ((segCounts['普通用户'] || 0) / total * 100).toFixed(1) + '%' : '0%';

            const topUsers = [...users].sort((a, b) => (b.games * 0.5 + b.winRate) - (a.games * 0.5 + a.winRate)).slice(0, 20);
            document.getElementById('topUsersTable').innerHTML = topUsers.map((u, i) => `
                <tr>
                    <td><b>${i + 1}</b></td>
                    <td>${u.id}</td>
                    <td>${u.name}</td>
                    <td><span class="rank-tag ${getRankClass(u.rank)}">${u.rank}</span></td>
                    <td><b>${u.score}</b></td>
                    <td>${u.games}</td>
                    <td>${u.winRate}%</td>
                    <td>${u.streak || 0}</td>
                    <td><span class="segment-tag ${getSegmentClass(u.segment)}">${u.segment}</span></td>
                </tr>
            `).join('');

            document.getElementById('userDetailTable').innerHTML = users.map(u => `
                <tr>
                    <td>${u.id}</td>
                    <td>${u.name}</td>
                    <td><span class="rank-tag ${getRankClass(u.rank)}">${u.rank}</span></td>
                    <td>${u.score}</td>
                    <td>${u.games}</td>
                    <td>${u.winRate}%</td>
                    <td>${u.streak || 0}</td>
                    <td><span class="segment-tag ${getSegmentClass(u.segment)}">${u.segment}</span></td>
                </tr>
            `).join('');

            renderPointsFlow(users);
        }

        function renderPointsFlow(users) {
            const pointTypes = ['球局胜利结算', '球局失败结算', '连胜奖励', '段位晋升奖励', '活动奖励'];
            const pointsFlowData = [];

            users.slice(0, 50).forEach(user => {
                const recordCount = Math.floor(Math.random() * 5) + 1;
                let balance = user.score;

                for (let i = 0; i < recordCount; i++) {
                    const type = pointTypes[Math.floor(Math.random() * pointTypes.length)];
                    let points;
                    if (type === '球局胜利结算') points = Math.floor(Math.random() * 30) + 20;
                    else if (type === '球局失败结算') points = -(Math.floor(Math.random() * 15) + 5);
                    else if (type === '连胜奖励') points = Math.floor(Math.random() * 50) + 30;
                    else points = Math.floor(Math.random() * 100) + 50;

                    balance = balance - points;
                    const daysAgo = Math.floor(Math.random() * 30);
                    const date = new Date();
                    date.setDate(date.getDate() - daysAgo);

                    pointsFlowData.push({
                        recordId: 'R' + (10000 + pointsFlowData.length),
                        userId: user.id,
                        nickname: user.name,
                        type: type,
                        points: points,
                        balance: Math.max(0, balance),
                        title: type === '球局胜利结算' ? '比赛胜利' : type === '球局失败结算' ? '比赛失败' : type,
                        time: date.toLocaleString()
                    });
                }
            });

            pointsFlowData.sort((a, b) => new Date(b.time) - new Date(a.time));

            document.getElementById('pointsFlowTable').innerHTML = pointsFlowData.slice(0, 50).map(record => `
                <tr>
                    <td>${record.recordId}</td>
                    <td>${record.userId}</td>
                    <td>${record.nickname}</td>
                    <td>${record.type}</td>
                    <td style="color: ${record.points > 0 ? '#2ECC71' : '#E74C3C'}; font-weight: bold;">${record.points > 0 ? '+' : ''}${record.points}</td>
                    <td>${record.balance}</td>
                    <td>${record.title}</td>
                    <td>${record.time}</td>
                </tr>
            `).join('');
        }

        function filterData() {
            const rankTier = document.getElementById('rankFilter').value;
            let filteredUsers = allVenueUsers.filter(u => {
                if (rankTier && !u.rank.includes(rankTier)) return false;
                return true;
            });
            updateDashboard(filteredUsers);
        }

        function getRankClass(rank) {
            if (rank.includes('传奇杆王') || rank.includes('荣耀杆王') || rank.includes('无双杆王') || rank.includes('最强杆王')) return 'rank-king';
            if (rank.includes('星耀')) return 'rank-star';
            if (rank.includes('钻石')) return 'rank-diamond';
            if (rank.includes('铂金')) return 'rank-platinum';
            if (rank.includes('黄金')) return 'rank-gold';
            if (rank.includes('白银')) return 'rank-silver';
            return 'rank-bronze';
        }

        function getSegmentClass(segment) {
            if (segment === '核心用户') return 'seg-vip';
            if (segment === '活跃用户') return 'seg-active';
            if (segment === '潜力用户') return 'seg-potential';
            if (segment === '流失风险') return 'seg-risk';
            return 'seg-normal';
        }

        function showSegment(segment) {
            alert(segment + ': ' + (allVenueUsers.filter(u => u.segment === segment).length) + '人');
        }

        // 页面加载检查登录
        checkLogin();

        // 窗口resize
        window.addEventListener('resize', () => {
            ['rankChart', 'segmentChart', 'dailyTrendChart', 'weeklyTrendChart', 'venueRankChart', 'matchModeChart', 'matchModePieChart'].forEach(id => {
                const chart = echarts.getInstanceByDom(document.getElementById(id));
                chart && chart.resize();
            });
        });
    </script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('单文件版本创建成功: index.html')
