# -*- coding: utf-8 -*-
import codecs

with codecs.open('球房老板看板_v2.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the getSegmentClass function and insert after it
idx = content.find("return 'seg-normal';")
if idx != -1:
    # Find the closing brace after this
    brace_idx = content.find('}', idx)
    if brace_idx != -1:
        insert_code = '''
        
        // 用户分层卡片点击事件
        let allVenueUsers = [];
        
        function setupSegmentCardClick(users) {
            allVenueUsers = users;
            const segmentMap = {
                'vip': '核心用户',
                'active': '活跃用户',
                'potential': '潜力用户',
                'risk': '流失风险',
                'normal': '普通用户'
            };
            
            document.querySelectorAll('.seg-card').forEach(card => {
                const classes = card.className.split(' ');
                const segClass = classes.find(c => ['vip', 'active', 'potential', 'risk', 'normal'].includes(c));
                if (segClass) {
                    card.onclick = () => showUserModal(segmentMap[segClass]);
                }
            });
        }
        
        function showUserModal(segment) {
            const segmentUsers = allVenueUsers.filter(u => u.segment === segment);
            const total = segmentUsers.length;
            
            document.getElementById('modalTitle').textContent = segment + ' (' + total + '人)';
            
            const avgScore = total > 0 ? Math.round(segmentUsers.reduce((s, u) => s + u.score, 0) / total) : 0;
            const avgGames = total > 0 ? Math.round(segmentUsers.reduce((s, u) => s + u.games, 0) / total) : 0;
            const avgWinRate = total > 0 ? (segmentUsers.reduce((s, u) => s + u.winRate, 0) / total).toFixed(1) : 0;
            
            document.getElementById('modalStats').innerHTML = `
                <div class="modal-stat-card">
                    <div class="value">${total}</div>
                    <div class="label">用户数</div>
                </div>
                <div class="modal-stat-card">
                    <div class="value">${avgScore}</div>
                    <div class="label">平均积分</div>
                </div>
                <div class="modal-stat-card">
                    <div class="value">${avgGames}</div>
                    <div class="label">平均场次</div>
                </div>
                <div class="modal-stat-card">
                    <div class="value">${avgWinRate}%</div>
                    <div class="label">平均胜率</div>
                </div>
            `;
            
            const sortedUsers = segmentUsers.sort((a, b) => b.score - a.score);
            
            document.getElementById('modalUserTable').innerHTML = sortedUsers.map(u => {
                const daysAgo = Math.floor(Math.random() * 7);
                const lastActive = daysAgo === 0 ? '今天' : daysAgo + '天前';
                return `
                <tr>
                    <td>${u.id}</td>
                    <td>${u.name}</td>
                    <td><span class="rank-tag ${getRankClass(u.rank)}">${u.rank}</span></td>
                    <td><b>${u.score}</b></td>
                    <td>${u.games}</td>
                    <td>${u.winRate}%</td>
                    <td>${u.streak || 0}</td>
                    <td>${lastActive}</td>
                </tr>
            `}).join('');
            
            document.getElementById('userModal').classList.add('active');
        }
        
        function closeModal() {
            document.getElementById('userModal').classList.remove('active');
        }
        
        document.getElementById('userModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });
'''
        new_content = content[:brace_idx+1] + insert_code + content[brace_idx+1:]
        
        with codecs.open('球房老板看板_v2.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('File updated successfully')
    else:
        print('Closing brace not found')
else:
    print('Pattern not found')
