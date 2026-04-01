# -*- coding: utf-8 -*-
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

base_path = r"c:\Users\陆鸣\Desktop\杆杆响天梯赛"

# 读取所有md文件
doc_contents = {}

for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith('.md') and not file.startswith('~$'):
            # 提取文档ID (如 P-01, O-02, D-02-01 等)
            file_id = file.split(' ')[0] if ' ' in file else file.replace('.md', '')
            # 支持 P-01, D-02-01 等格式
            if (('-' in file_id and len(file_id) <= 8) or file_id.startswith('D-0') or file_id.startswith('P-0') or file_id.startswith('O-0')):
                md_path = os.path.join(root, file)
                try:
                    with open(md_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    doc_contents[file_id] = content
                    print(f"读取: {file_id} - {file}")
                except Exception as e:
                    print(f"跳过: {file} - {str(e)}")

# 生成JavaScript对象
js_content = "const docContents = {\n"
for doc_id, content in doc_contents.items():
    # 转义内容中的特殊字符
    escaped_content = content.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
    js_content += f"    '{doc_id}': `{escaped_content}`,\n"
js_content += "};\n"

# 保存到文件
output_path = os.path.join(base_path, "doc_contents.js")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"\n完成！共处理 {len(doc_contents)} 个文档")
print(f"输出文件: {output_path}")
