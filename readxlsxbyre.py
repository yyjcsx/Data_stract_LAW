import pandas as pd
from openai import OpenAI
import json
from typing import List, Dict
import pandas as pd
from splittext2 import legal_text_to_dataframe
import os
error_log = "error_log.txt"
undoxlsxflag = False
def read_law_excel(file_path):
    """
    读取法律Excel文件并转换为结构化DataFrame
    :param file_path: Excel文件路径
    :return: 包含法律信息的DataFrame
    """
    try:
        # 读取Excel文件（使用openpyxl引擎支持.xlsx格式）
        df = pd.read_excel(
            file_path,
            engine='openpyxl',
            header=0,
            usecols="A,B,C,D,E,F,G,H,I,J,K,L"
        )
        

        # 添加遍历功能示例
        print("开始遍历法律条目：")
        for index, row in df.iterrows():
            print(f"\n条目 {index + 1}:")
           
        
        return df
    
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 不存在")
        return pd.DataFrame()
    except Exception as e:
        print(f"读取文件时发生错误：{str(e)}")
        return pd.DataFrame()


# 修改保存逻辑，在最后保存带标记的原始文件
if __name__ == "__main__":
    excel_path = "0428_2.xlsx"
    law_df = read_law_excel(excel_path)
    
    if not law_df.empty:
        # 新增问题标签列
        law_df['问题标签'] = ''
        
        # 过滤出需要处理的条目
        #process_df = law_df[law_df['WordCount'] <= 10000]
        
        # 仅遍历符合条件的条目
        for _, row in law_df.iterrows():
            print(f"正在处理：{row['标题']}")
            # print(f"Article Number：{row['ArticleNumber']}")
            
            # print(f"Effective Date：{row['EffectiveDate'].strftime('%Y-%m-%d') if pd.notnull(row['EffectiveDate']) else 'N/A'}")
            
        

            name = row[1][:30]  # 截取前30个字符
            content = row[11] 
            print(name)
            result_df = legal_text_to_dataframe(content)

            # 添加法律元数据到结果DataFrame
            meta_data = {
                "标题": row[0],
                "法律名词": row[1],
                "发布文号": row[2],
                "机构": row[3],
                "类别": row[4],
                "发布日期": row[5],
                "实施日期": row[6],
                "有效性": row[7],
                "效力级别": row[8],
                "省份": row[9],
                "所属年份": row[10],
                
            }
            
            # 将元数据合并到每个条目
            for col_name, value in meta_data.items():
                result_df[col_name] = value

            # 转换为 DataFrame
            if not result_df.empty:
                df = result_df
                print(df[["条目目录", "条目内容"]].head())
                
                # 新增问题标签处理逻辑
                if '处理状态' in df.columns:
                    problem_rows = df[df['处理状态'] == '仅含其他内容']
                    if not problem_rows.empty:
                        original_index = row.name
                        law_df.loc[original_index, '问题标签'] = '不是按照条分类的'
                        print(f"标记问题行：{original_index}")
                        undoxlsxflag = True
            else:
                print("数据为空或解析失败")
                with open(error_log, 'a', encoding='utf-8') as f:
                    f.write(f"{name}\n")
                continue
                
            #name = "国务院办公厅关于印发《国家自然灾害救助应急预案》的通知"
            # 生成Excel文件（新增条件判断）
            if pd.isnull(law_df.loc[row.name, '问题标签']) or law_df.loc[row.name, '问题标签'] == '':  # 只在无问题标签时生成
                try:
                    # 新增文件夹创建逻辑
                    efficacy_level = row[8]  # 获取效力级别
                    folder_path = f"./{efficacy_level}"
                    os.makedirs(folder_path, exist_ok=True)
                    
                    # 修改文件保存路径
                    file_path = os.path.join(folder_path, f"{name}.xlsx")
                    
                    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False, sheet_name=name)
                        
                        # 获取工作表和设置可见性 (xlsxwriter方式)
                        workbook = writer.book
                        worksheet = writer.sheets[name]
                        
                        # 自动调整列宽
                        for i, col in enumerate(df.columns):
                            # 获取列的最大宽度
                            max_len = max((
                                df[col].astype(str).map(len).max(),  # 数据最大长度
                                len(str(col))  # 列名长度
                            ))
                            # 设置列宽，稍微加宽一点
                            worksheet.set_column(i, i, max_len + 2)

                    print(f"文件已成功生成：{file_path}")
                except Exception as e:
                    print(f"生成Excel文件时出错：{str(e)}")
                    with open(error_log, 'a', encoding='utf-8') as f:
                        f.write(f"{name}\n")
                    continue
            else:
                undoxlsxflag = False

        # 循环结束后保存带标记的原始文件
        marked_path = excel_path.replace(".xlsx", "_marked.xlsx")
        law_df.to_excel(marked_path, index=False, engine='openpyxl')
        print(f"已生成标记文件：{marked_path}")
