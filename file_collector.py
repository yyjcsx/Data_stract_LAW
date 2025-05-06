import os
import pandas as pd

def collect_excel_names(root_dir):
    data = []
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.xlsx') and not file.startswith('~$'):
                # 修改文件名处理逻辑：保留原始标点符号
                clean_name = os.path.splitext(file)[0]  # 正确去除扩展名
                short_name = clean_name[:30]  # 直接截取前30字符保留所有符号
                
                data.append({
                    "完整路径": os.path.join(root, file),
                    "处理后的文件名": short_name
                })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    target_dir = input("请输入要扫描的根目录路径：").strip()
    
    if not os.path.exists(target_dir):
        print(f"错误：路径 {target_dir} 不存在")
        exit(1)
        
    df = collect_excel_names(target_dir)
    
    output_path = "processed_files.xlsx"
    df.to_excel(output_path, index=False, engine='openpyxl')
    print(f"处理完成！共收集 {len(df)} 个文件，结果已保存至：{output_path}")

'''
已经处理的数量187695个
1.4G文件数量共计192700条
还有5005条没有处理
'''