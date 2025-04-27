import pandas as pd
from openai import OpenAI
import json
from typing import List, Dict
import pandas as pd
from splittext2 import legal_text_to_dataframe
 
error_log = "error_log.txt"
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
            usecols="A,C,D,E,F,G,H,I,K,L,M"
        )
        
        # 重命名列（根据Excel列字母对应到DataFrame的列索引）
        column_mapping = {
            df.columns[0]: "LawName",
            df.columns[1]: "ArticleNumber",
            df.columns[2]: "IssuingAuthority",
            df.columns[3]: "Domain",
            df.columns[4]: "ReleaseDate",
            df.columns[5]: "EffectiveDate",
            df.columns[6]: "IsCurrent",
            df.columns[7]: "LawType",
            df.columns[8]: "ReleaseYear",
            df.columns[9]: "Content",
            df.columns[10]: "WordCount"
        }
        df = df.rename(columns=column_mapping)
        
        # 添加过滤条件（阈值设为10000）
        df = df[df['WordCount'] <= 10000]
        
        # 转换日期格式
        date_columns = ["ReleaseDate", "EffectiveDate"]
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

        
        df['备注'] = df.apply(lambda row: "文本过大，需要手动分割一下" if row['WordCount'] > 10000 else "", axis=1)
        
        # 保存修改后的Excel（需要安装openpyxl）
        df.to_excel(file_path, index=False, engine='openpyxl')
        
        # 添加遍历功能示例
        print("开始遍历法律条目：")
        for index, row in df.iterrows():
            print(f"\n条目 {index + 1}:")
            print(f"Law Name：{row['LawName']}")
            print(f"Article Number：{row['ArticleNumber']}")
            print(f"Word Count：{row['WordCount']} {'⚠️需要分割' if row['WordCount'] > 10000 else ''}")
            print(f"Effective Date：{row['EffectiveDate'].strftime('%Y-%m-%d') if pd.notnull(row['EffectiveDate']) else 'N/A'}")
            print(f"Word Count：{row['WordCount']}")
        
        return df
    
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 不存在")
        return pd.DataFrame()
    except Exception as e:
        print(f"读取文件时发生错误：{str(e)}")
        return pd.DataFrame()

# 使用示例
def read_law_excel(file_path):
    try:
        # 读取Excel文件（移除过滤条件）
        df = pd.read_excel(
            file_path,
            engine='openpyxl',
            header=0,
            usecols="A,C,D,E,F,G,H,I,K,L,M"
        )
        
        # 重命名列（保持原样）
        column_mapping = {
            df.columns[0]: "LawName",
            df.columns[1]: "ArticleNumber",
            df.columns[2]: "IssuingAuthority",
            df.columns[3]: "Domain",
            df.columns[4]: "ReleaseDate",
            df.columns[5]: "EffectiveDate",
            df.columns[6]: "IsCurrent",
            df.columns[7]: "LawType",
            df.columns[8]: "ReleaseYear",
            df.columns[9]: "Content",
            df.columns[10]: "WordCount"
        }
        df = df.rename(columns=column_mapping)
        
        # 添加标识列
        df['ProcessingFlag'] = df['WordCount'].apply(lambda x: "需人工处理" if x > 10000 else "")
        
        # 生成新文件名（在原文件名后加_processed）
        processed_path = file_path.replace(".xlsx", "_processed.xlsx")
        
        # 保存到新文件
        df.to_excel(processed_path, index=False, engine='openpyxl')
        
        return df
    
    except Exception as e:
        print(f"错误：{str(e)}")
        return pd.DataFrame()

# 修改遍历部分
if __name__ == "__main__":
    excel_path = "79_excel9.xlsx"
    law_df = read_law_excel(excel_path)
    
    if not law_df.empty:
        # 过滤出需要处理的条目
        #process_df = law_df[law_df['WordCount'] <= 10000]
        
        # 仅遍历符合条件的条目
        for _, row in law_df.iterrows():
            print(f"正在处理：{row['LawName']}")
            print(f"Article Number：{row['ArticleNumber']}")
            print(f"Word Count：{row['WordCount']}")
            print(f"Effective Date：{row['EffectiveDate'].strftime('%Y-%m-%d') if pd.notnull(row['EffectiveDate']) else 'N/A'}")
            print(f"Word Count：{row['WordCount']}")
        

            name = row['LawName'][:30]  # 截取前30个字符
            content = row['Content'] 
            print(name)
            result_df = legal_text_to_dataframe(content)


            

            # 转换为 DataFrame
            if not result_df.empty:  # 修改此处判断条件
                df = result_df
                print(df[["条目目录", "条目内容"]].head())
            else:
                print("数据为空或解析失败")
                with open(error_log, 'a', encoding='utf-8') as f:
                    f.write(f"{name}\n")
                continue
                
            #name = "国务院办公厅关于印发《国家自然灾害救助应急预案》的通知"
            # 生成Excel文件
            try:
                with pd.ExcelWriter("{}.xlsx".format(name), engine='xlsxwriter') as writer:
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

                print("文件已成功生成：{}.xlsx".format(name))
            except Exception as e:
                print(f"生成Excel文件时出错：{str(e)}")
                with open(error_log, 'a', encoding='utf-8') as f:
                    f.write(f"{name}\n")
                continue
