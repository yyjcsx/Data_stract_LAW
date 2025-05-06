import os

def count_excel_files(directory):
    total = 0
    print(f"正在扫描目录：{os.path.abspath(directory)}")
    
    for root, dirs, files in os.walk(directory):
        # 统计当前目录的xlsx文件（排除临时文件）
        count = len([f for f in files 
                    if f.endswith('.xlsx') 
                    and not f.startswith('~$')])
        
        # 显示当前目录结果
        print(f"目录：{os.path.relpath(root, directory)}")
        print(f"文件数量：{count}")
        print("-" * 40)
        
        total += count
    
    return total

if __name__ == "__main__":
    target_dir = input("请输入要扫描的路径（支持相对/绝对路径）：").strip()
    
    if not os.path.exists(target_dir):
        print(f"错误：路径 {target_dir} 不存在")
        exit(1)
        
    total_files = count_excel_files(target_dir)
    print(f"\n扫描完成！总计Excel文件数：{total_files}")