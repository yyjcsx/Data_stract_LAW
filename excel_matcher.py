import pandas as pd
from tqdm import tqdm
import re  # 新增导入正则模块

def match_and_export(fileA_path, fileB_path, output_path):
    # 读取文件A（带进度条）
    print("正在读取文件A...")
    df_A = pd.read_excel(fileA_path, header=0)
    a_col_name = df_A.columns[0]
    
    # 新增标点清理逻辑（处理中文书名号等标点）
    df_A[a_col_name] = df_A[a_col_name].apply(
        lambda x: re.sub(r'[《》【】“”‘’！？，。；：、]', '', str(x))
    )
    
    # 新增中间结果输出
    cleaned_path = "清理后的文件A.xlsx"
    df_A.to_excel(cleaned_path, index=False)
    print(f"标点清理后的文件已临时保存至：{cleaned_path}")
    
    # 读取文件B（带进度条）
    print("正在读取文件B...")
    df_B = pd.read_excel(fileB_path, header=0)
    b_col_name = df_B.columns[0]
    
    # 预处理B文件数据（添加进度条）
    print("预处理B文件数据...")
    b_values = set()
    for val in tqdm(df_B[b_col_name].astype(str), desc='处理B文件值'):
        clean_val = val.strip()
        if clean_val:
            b_values.add(clean_val)
            b_values.add(clean_val[:20])
    
    # 添加匹配进度条
    print("开始匹配数据...")
    tqdm.pandas(desc='匹配进度')
    df_A['是否匹配'] = df_A[a_col_name].progress_apply(
        lambda x: any(
            # 新增精确子字符串匹配逻辑
            str(b_val) in str(x)  # B的值是A的完整子串
            or str(b_val) in str(x)[:20]  # B的值是A前20字符的子串
            for b_val in b_values
        )
    )
    
    # 输出未匹配数据
    unmatched_df = df_A[~df_A['是否匹配']].drop(columns=['是否匹配'])
    unmatched_df.to_excel(output_path, index=False)

if __name__ == "__main__":
    fileA_path = "test2.xlsx"    # 修改为实际路径
    fileB_path = "processed_files.xlsx"    # 修改为实际路径
    output_path = "未匹配结果.xlsx"
    
    match_and_export(fileA_path, fileB_path, output_path)
    print(f"未匹配数据已保存至：{output_path}")