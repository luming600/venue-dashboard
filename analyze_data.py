# -*- coding: utf-8 -*-
"""
天梯赛用户运营数据分析工具
用于分析从后台导出的Excel数据
"""

import pandas as pd
import os
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

class LadderDataAnalyzer:
    """天梯赛数据分析器"""

    def __init__(self, ladder_file=None, points_file=None):
        self.ladder_df = None
        self.points_df = None

        if ladder_file and os.path.exists(ladder_file):
            self.load_ladder_data(ladder_file)
        if points_file and os.path.exists(points_file):
            self.load_points_data(points_file)

    def load_ladder_data(self, file_path):
        """加载用户天梯数据"""
        try:
            self.ladder_df = pd.read_excel(file_path)
            print(f"已加载用户天梯数据: {len(self.ladder_df)} 条记录")
            return True
        except Exception as e:
            print(f"加载天梯数据失败: {e}")
            return False

    def load_points_data(self, file_path):
        """加载积分流水数据"""
        try:
            self.points_df = pd.read_excel(file_path)
            print(f"已加载积分流水数据: {len(self.points_df)} 条记录")
            return True
        except Exception as e:
            print(f"加载积分流水失败: {e}")
            return False

    def analyze_ladder_data(self):
        """分析用户天梯数据"""
        if self.ladder_df is None:
            print("请先加载用户天梯数据")
            return

        print("\n" + "="*60)
        print("用户天梯数据分析报告")
        print("="*60)

        # 基础统计
        print(f"\n【基础统计】")
        print(f"总用户数: {len(self.ladder_df)}")

        if '总场次' in self.ladder_df.columns:
            total_games = self.ladder_df['总场次'].sum()
            avg_games = self.ladder_df['总场次'].mean()
            print(f"总场次: {total_games}")
            print(f"人均场次: {avg_games:.1f}")

        if '胜率(%)' in self.ladder_df.columns:
            avg_winrate = self.ladder_df['胜率(%)'].mean()
            print(f"平均胜率: {avg_winrate:.1f}%")

        # 段位分布
        if '当前段位' in self.ladder_df.columns:
            print(f"\n【段位分布】")
            rank_dist = self.ladder_df['当前段位'].value_counts().head(10)
            for rank, count in rank_dist.items():
                print(f"  {rank}: {count}人 ({count/len(self.ladder_df)*100:.1f}%)")

        # 胜率分布
        if '胜率(%)' in self.ladder_df.columns:
            print(f"\n【胜率分布】")
            bins = [0, 30, 50, 70, 85, 100]
            labels = ['0-30%', '30-50%', '50-70%', '70-85%', '85-100%']
            self.ladder_df['胜率区间'] = pd.cut(self.ladder_df['胜率(%)'], bins=bins, labels=labels)
            winrate_dist = self.ladder_df['胜率区间'].value_counts()
            for range_name, count in winrate_dist.items():
                print(f"  {range_name}: {count}人")

        # 地域分布
        if '省份' in self.ladder_df.columns:
            print(f"\n【地域分布 Top10】")
            province_dist = self.ladder_df['省份'].value_counts().head(10)
            for province, count in province_dist.items():
                print(f"  {province}: {count}人")

        # 高价值用户
        if '赛事积分' in self.ladder_df.columns:
            print(f"\n【Top10 高价值用户】")
            top_users = self.ladder_df.nlargest(10, '赛事积分')[['用户昵称', '当前段位', '赛事积分', '胜率(%)']]
            for i, row in top_users.iterrows():
                print(f"  {row['用户昵称']}: {row['赛事积分']}积分, {row['当前段位']}, 胜率{row['胜率(%)']}%")

        # 连胜统计
        if '历史最高连胜次数' in self.ladder_df.columns:
            max_streak = self.ladder_df['历史最高连胜次数'].max()
            avg_streak = self.ladder_df['历史最高连胜次数'].mean()
            print(f"\n【连胜统计】")
            print(f"最高连胜记录: {max_streak}")
            print(f"平均最高连胜: {avg_streak:.1f}")

    def analyze_points_data(self):
        """分析积分流水数据"""
        if self.points_df is None:
            print("请先加载积分流水数据")
            return

        print("\n" + "="*60)
        print("积分流水数据分析报告")
        print("="*60)

        # 基础统计
        print(f"\n【基础统计】")
        print(f"积分流水记录数: {len(self.points_df)}")

        if '积分变动' in self.points_df.columns:
            total_points = self.points_df['积分变动'].sum()
            avg_points = self.points_df['积分变动'].mean()
            print(f"积分发放总量: {total_points}")
            print(f"场均积分: {avg_points:.1f}")

        # 业务类型分布
        if '业务类型' in self.points_df.columns or '标题' in self.points_df.columns:
            type_col = '业务类型' if '业务类型' in self.points_df.columns else '标题'
            print(f"\n【业务类型分布】")
            type_dist = self.points_df[type_col].value_counts()
            for type_name, count in type_dist.items():
                print(f"  {type_name}: {count}次")

        # 球馆活跃度
        if '球馆' in self.points_df.columns:
            print(f"\n【球馆活跃度 Top10】")
            venue_dist = self.points_df['球馆'].value_counts().head(10)
            for venue, count in venue_dist.items():
                print(f"  {venue}: {count}条记录")

        # 用户活跃度
        if '用户ID' in self.points_df.columns:
            unique_users = self.points_df['用户ID'].nunique()
            print(f"\n活跃用户数: {unique_users}")

    def calculate_user_segments(self):
        """计算用户分层"""
        if self.ladder_df is None:
            print("请先加载用户天梯数据")
            return None

        print("\n" + "="*60)
        print("用户分层运营分析")
        print("="*60)

        # 添加分层字段
        def get_segment(row):
            games = row.get('总场次', 0) or 0
            winrate = row.get('胜率(%)', 0) or 0

            # 简化的分层逻辑
            if winrate >= 70 and games >= 50:
                return '核心用户'
            elif games >= 30 and winrate >= 50:
                return '活跃用户'
            elif winrate >= 60 and games < 30:
                return '潜力用户'
            elif games >= 30 and winrate < 50:
                return '流失风险'
            else:
                return '普通用户'

        self.ladder_df['用户分层'] = self.ladder_df.apply(get_segment, axis=1)

        # 统计分层
        print(f"\n【用户分层统计】")
        segment_dist = self.ladder_df['用户分层'].value_counts()
        total = len(self.ladder_df)

        for segment, count in segment_dist.items():
            percent = count / total * 100
            print(f"  {segment}: {count}人 ({percent:.1f}%)")

        # 运营建议
        print(f"\n【运营建议】")
        suggestions = {
            '核心用户': '提供VIP专属权益、优先客服服务、专属赛事邀请',
            '活跃用户': '推送技巧教学内容、定期活动通知、积分奖励',
            '潜力用户': '重点培养、邀请参与高端赛事、提供专业指导',
            '流失风险': '召回活动、大额积分奖励、定向触达激活',
            '普通用户': '基础服务、引导参与入门活动、新手福利'
        }
        for segment, suggestion in suggestions.items():
            print(f"  {segment}: {suggestion}")

        return self.ladder_df

    def export_analysis(self, output_dir='.'):
        """导出分析结果"""
        if self.ladder_df is not None:
            # 导出带分层的用户数据
            if '用户分层' not in self.ladder_df.columns:
                self.calculate_user_segments()

            output_file = os.path.join(output_dir, f'用户分层数据_{datetime.now().strftime("%Y%m%d")}.xlsx')
            self.ladder_df.to_excel(output_file, index=False)
            print(f"\n已导出分析结果: {output_file}")

    def generate_report(self, output_file='运营数据报告.txt'):
        """生成文字报告"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("天梯赛用户运营数据报告\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")

            if self.ladder_df is not None:
                f.write("【用户天梯数据概览】\n")
                f.write(f"总用户数: {len(self.ladder_df)}\n")
                if '总场次' in self.ladder_df.columns:
                    f.write(f"总场次: {self.ladder_df['总场次'].sum()}\n")
                if '胜率(%)' in self.ladder_df.columns:
                    f.write(f"平均胜率: {self.ladder_df['胜率(%)'].mean():.1f}%\n")
                f.write("\n")

            if self.points_df is not None:
                f.write("【积分流水数据概览】\n")
                f.write(f"流水记录数: {len(self.points_df)}\n")
                if '积分变动' in self.points_df.columns:
                    f.write(f"积分发放总量: {self.points_df['积分变动'].sum()}\n")
                f.write("\n")

        print(f"\n报告已生成: {output_file}")


def main():
    """主函数"""
    print("="*60)
    print("天梯赛用户运营数据分析工具")
    print("="*60)

    # 查找数据文件
    data_dir = os.path.dirname(os.path.abspath(__file__))
    ladder_files = [f for f in os.listdir(data_dir) if '天梯' in f and f.endswith(('.xlsx', '.xls', '.csv'))]
    points_files = [f for f in os.listdir(data_dir) if '积分' in f and f.endswith(('.xlsx', '.xls', '.csv'))]

    analyzer = LadderDataAnalyzer()

    # 尝试自动加载数据
    if ladder_files:
        print(f"\n发现天梯数据文件: {ladder_files[0]}")
        analyzer.load_ladder_data(os.path.join(data_dir, ladder_files[0]))

    if points_files:
        print(f"\n发现积分数据文件: {points_files[0]}")
        analyzer.load_points_data(os.path.join(data_dir, points_files[0]))

    # 运行分析
    if analyzer.ladder_df is not None:
        analyzer.analyze_ladder_data()
        analyzer.calculate_user_segments()

    if analyzer.points_df is not None:
        analyzer.analyze_points_data()

    # 导出结果
    if analyzer.ladder_df is not None or analyzer.points_df is not None:
        analyzer.export_analysis(data_dir)
        analyzer.generate_report(os.path.join(data_dir, '运营数据报告.txt'))

    print("\n分析完成!")


if __name__ == '__main__':
    main()
