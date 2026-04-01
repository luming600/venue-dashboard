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

# 读取数据文件
with open('demo_data.js', 'r', encoding='utf-8') as f:
    data_js = f.read()

# 读取原始看板HTML
with open('球房老板看板_v2.html', 'r', encoding='utf-8') as f:
    dashboard_html = f.read()

# 创建登录页面
login_page = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>球房数据看板 - 登录</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
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
    </style>
</head>
<body>
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
            <p class="login-error" id="error">账号或密码错误</p>
        </form>
    </div>
    <script>
        const accounts = ''' + json.dumps(accounts, ensure_ascii=False) + ''';

        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const user = document.getElementById('username').value.trim();
            const pass = document.getElementById('password').value;

            if (accounts[user] && accounts[user].password === pass) {
                sessionStorage.setItem('venueName', accounts[user].venue);
                window.location.href = 'dashboard.html';
            } else {
                document.getElementById('error').classList.add('show');
            }
        });
    </script>
</body>
</html>'''

# 修改看板页面 - 添加登录检查
# 添加退出按钮样式
logout_style = '''
        .logout-btn {
            background: rgba(255,255,255,0.15);
            border: 1px solid rgba(255,255,255,0.3);
            color: #fff;
            padding: 8px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 10px;
        }
        .logout-btn:hover {
            background: rgba(231, 76, 60, 0.3);
            border-color: #E74C3C;
        }
'''
dashboard_html = dashboard_html.replace('</style>', logout_style + '</style>')

# 添加退出按钮
header_old = '''<div class="header-info">
            <p>数据时间：2026年3月</p>
            <p id="updateTime">更新时间：--</p>
        </div>'''
header_new = '''<div class="header-info">
            <p>数据时间：2026年3月</p>
            <p id="updateTime">更新时间：--</p>
            <button class="logout-btn" onclick="logout()">退出登录</button>
        </div>'''
dashboard_html = dashboard_html.replace(header_old, header_new)

# 替换初始化脚本
old_init = '''        // 当前球馆（实际使用时从登录信息获取）
        const currentVenue = "乔氏台球俱乐部";

        // 初始化
        function init() {
            document.getElementById('updateTime').textContent = '更新时间: ' + new Date().toLocaleString();
            document.getElementById('venueNameDisplay').textContent = currentVenue;

            // 筛选本店数据
            const venueUsers = demoData.allUsers.filter(u => u.venue === currentVenue);

            // 初始化图表
            initCharts(venueUsers);

            // 更新数据
            updateDashboard(venueUsers);

            // 设置分层卡片点击事件
            setupSegmentCardClick(venueUsers);
        }'''

new_init = '''        let currentVenue = "";

        // 检查登录
        function checkLogin() {
            const venue = sessionStorage.getItem('venueName');
            if (!venue) {
                window.location.href = 'login.html';
                return false;
            }
            currentVenue = venue;
            document.getElementById('venueNameDisplay').textContent = currentVenue;
            return true;
        }

        // 退出登录
        function logout() {
            sessionStorage.removeItem('venueName');
            window.location.href = 'login.html';
        }

        // 初始化
        function init() {
            if (!checkLogin()) return;

            document.getElementById('updateTime').textContent = '更新时间: ' + new Date().toLocaleString();

            // 筛选本店数据
            const venueUsers = demoData.allUsers.filter(u => u.venue === currentVenue);

            // 初始化图表
            initCharts(venueUsers);

            // 更新数据
            updateDashboard(venueUsers);

            // 设置分层卡片点击事件
            setupSegmentCardClick(venueUsers);
        }'''

dashboard_html = dashboard_html.replace(old_init, new_init)

# 内嵌数据
dashboard_html = dashboard_html.replace('<script src="demo_data.js"></script>', '<script>\n' + data_js + '    </script>')

# 保存文件
with open('login.html', 'w', encoding='utf-8') as f:
    f.write(login_page)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dashboard_html)

print('创建成功！')
print('登录页面: login.html')
print('看板页面: dashboard.html')
print('\n测试账号:')
for user, info in list(accounts.items())[:5]:
    print(f'  账号: {user:15} 密码: {info["password"]:15} 球馆: {info["venue"]}')
