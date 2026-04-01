# -*- coding: utf-8 -*-
import json

# 读取原始HTML
with open('球房老板看板_v2.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 登录页面样式
login_css = '''
        /* 登录页面样式 */
        .login-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .login-overlay.hidden {
            display: none;
        }
        .login-box {
            background: rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 40px 50px;
            width: 400px;
            border: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }
        .login-logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .login-logo h1 {
            color: #2ECC71;
            font-size: 28px;
            margin-bottom: 8px;
        }
        .login-logo p {
            color: #888;
            font-size: 14px;
        }
        .login-form .form-group {
            margin-bottom: 20px;
        }
        .login-form label {
            display: block;
            color: #ccc;
            font-size: 14px;
            margin-bottom: 8px;
        }
        .login-form input {
            width: 100%;
            padding: 14px 18px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            color: #fff;
            font-size: 16px;
            transition: all 0.3s;
        }
        .login-form input:focus {
            outline: none;
            border-color: #2ECC71;
            background: rgba(255,255,255,0.15);
        }
        .login-form input::placeholder {
            color: #666;
        }
        .login-btn {
            width: 100%;
            padding: 16px;
            background: linear-gradient(90deg, #2ECC71 0%, #27AE60 100%);
            border: none;
            border-radius: 10px;
            color: #fff;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 10px;
        }
        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(46, 204, 113, 0.4);
        }
        .login-error {
            color: #E74C3C;
            font-size: 14px;
            text-align: center;
            margin-top: 15px;
            display: none;
        }
        .login-error.show {
            display: block;
        }
        .logout-btn {
            background: rgba(255,255,255,0.15);
            border: 1px solid rgba(255,255,255,0.3);
            color: #fff;
            padding: 8px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }
        .logout-btn:hover {
            background: rgba(231, 76, 60, 0.3);
            border-color: #E74C3C;
        }
'''

# 登录HTML
login_html = '''
    <!-- 登录页面 -->
    <div class="login-overlay" id="loginOverlay">
        <div class="login-box">
            <div class="login-logo">
                <h1>球房数据看板</h1>
                <p>请登录查看您的球房数据</p>
            </div>
            <form class="login-form" onsubmit="return handleLogin(event)">
                <div class="form-group">
                    <label>账号</label>
                    <input type="text" id="loginUsername" placeholder="请输入账号" required>
                </div>
                <div class="form-group">
                    <label>密码</label>
                    <input type="password" id="loginPassword" placeholder="请输入密码" required>
                </div>
                <button type="submit" class="login-btn">登 录</button>
                <p class="login-error" id="loginError">账号或密码错误</p>
            </form>
        </div>
    </div>
'''

# 在</style>前添加登录样式
html = html.replace('</style>', login_css + '\n    </style>')

# 在<body>后添加登录HTML
html = html.replace('<body>', '<body>' + login_html)

# 在header-info中添加退出按钮
header_info_old = '''<div class="header-info">
            <p>数据时间：2026年3月</p>
            <p id="updateTime">更新时间：--</p>
        </div>'''

header_info_new = '''<div class="header-info">
            <p>数据时间：2026年3月</p>
            <p id="updateTime">更新时间：--</p>
            <button class="logout-btn" onclick="handleLogout()">退出登录</button>
        </div>'''

html = html.replace(header_info_old, header_info_new)

# 球馆账号数据
venue_accounts = {
    "qiaoshi": {"password": "qiaoshi123", "venue": "乔氏台球俱乐部"},
    "taiqiu": {"password": "taiqiu123", "venue": "台球帝国"},
    "xingji": {"password": "xingji123", "venue": "星际台球"},
    "jiuqiu": {"password": "jiuqiu123", "venue": "九球台球俱乐部"},
    "mingshi": {"password": "mingshi123", "venue": "名仕台球"},
    "jinzue": {"password": "jinzue123", "venue": "金爵台球俱乐部"},
    "haoting": {"password": "haoting123", "venue": "豪庭台球俱乐部"},
    "dianfeng": {"password": "dianfeng123", "venue": "巅峰台球"},
    "fengyun": {"password": "fengyun123", "venue": "风云台球会所"},
    "yipin": {"password": "yipin123", "venue": "壹品台球"},
    "manishikong": {"password": "manishikong123", "venue": "乌达区慢时空台球厅"},
    "wuchang": {"password": "wuchang123", "venue": "武昌万象城八楼名仕台球"},
    "bojue": {"password": "bojue123", "venue": "伯爵台球会所"},
    "tiangong": {"password": "tiangong123", "venue": "天工台球城"},
    "wangzhe": {"password": "wangzhe123", "venue": "王者台球俱乐部"},
    "shenshi": {"password": "shenshi123", "venue": "绅士台球俱乐部"},
    "guanjun": {"password": "guanjun123", "venue": "冠军台球馆"},
    "xingyun": {"password": "xingyun123", "venue": "星云台球"},
    "heiba": {"password": "heiba123", "venue": "黑八台球城"},
    "xingpai": {"password": "xingpai123", "venue": "星牌台球会所"}
}

accounts_js = "const venueAccounts = " + json.dumps(venue_accounts, ensure_ascii=False, indent=2) + ";\n"

# 登录脚本
login_script = '''
    <script>
        ''' + accounts_js + '''
        
        let currentVenue = "";
        let isLoggedIn = false;
        
        // 检查登录状态
        function checkLogin() {
            const savedVenue = sessionStorage.getItem('currentVenue');
            if (savedVenue) {
                currentVenue = savedVenue;
                isLoggedIn = true;
                document.getElementById('loginOverlay').classList.add('hidden');
                document.getElementById('venueNameDisplay').textContent = currentVenue;
                initDashboard();
            }
        }
        
        // 处理登录
        function handleLogin(e) {
            e.preventDefault();
            const username = document.getElementById('loginUsername').value.trim();
            const password = document.getElementById('loginPassword').value;
            
            if (venueAccounts[username] && venueAccounts[username].password === password) {
                currentVenue = venueAccounts[username].venue;
                isLoggedIn = true;
                sessionStorage.setItem('currentVenue', currentVenue);
                document.getElementById('loginOverlay').classList.add('hidden');
                document.getElementById('venueNameDisplay').textContent = currentVenue;
                document.getElementById('loginError').classList.remove('show');
                initDashboard();
            } else {
                document.getElementById('loginError').classList.add('show');
            }
            return false;
        }
        
        // 退出登录
        function handleLogout() {
            sessionStorage.removeItem('currentVenue');
            isLoggedIn = false;
            currentVenue = "";
            document.getElementById('loginOverlay').classList.remove('hidden');
            document.getElementById('loginUsername').value = "";
            document.getElementById('loginPassword').value = "";
        }
        
        // 初始化看板
        function initDashboard() {
            if (!isLoggedIn) return;
            document.getElementById('updateTime').textContent = '更新时间: ' + new Date().toLocaleString();
            const venueUsers = demoData.allUsers.filter(u => u.venue === currentVenue);
            initCharts(venueUsers);
            updateDashboard(venueUsers);
            setupSegmentCardClick(venueUsers);
        }
        
        // 页面加载时检查登录
        checkLogin();
'''

# 替换初始化脚本
old_init = '''        // 页面加载
        init();'''

html = html.replace(old_init, login_script)

# 保存新文件
with open('球房老板看板_v3_登录版.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('登录版看板创建成功！')
print('\n球馆账号列表：')
for username, info in venue_accounts.items():
    print(f'  账号: {username:15} 密码: {info["password"]:15} 球馆: {info["venue"]}')
