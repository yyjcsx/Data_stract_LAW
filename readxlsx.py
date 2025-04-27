import pandas as pd
from openai import OpenAI
import json
from typing import List, Dict
import pandas as pd
client = OpenAI(api_key="sk-7131415e0904415287e26c7a990a5451", base_url="https://api.deepseek.com")
 
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
    excel_path = "79_excel8.xlsx"
    law_df = read_law_excel(excel_path)
    
    if not law_df.empty:
        # 过滤出需要处理的条目
        process_df = law_df[law_df['WordCount'] <= 10000]
        
        # 仅遍历符合条件的条目
        for _, row in process_df.iterrows():
            print(f"正在处理：{row['LawName']}")
            print(f"Article Number：{row['ArticleNumber']}")
            print(f"Word Count：{row['WordCount']} {'⚠️需要分割' if row['WordCount'] > 10000 else ''}")
            print(f"Effective Date：{row['EffectiveDate'].strftime('%Y-%m-%d') if pd.notnull(row['EffectiveDate']) else 'N/A'}")
            print(f"Word Count：{row['WordCount']}")
        
#         return df
    
#     except FileNotFoundError:
#         print(f"错误：文件 {file_path} 不存在")
#         return pd.DataFrame()
#     except Exception as e:
#         print(f"读取文件时发生错误：{str(e)}")
#         return pd.DataFrame()

# # 使用示例
# if __name__ == "__main__":
#     excel_path = "79_excel7.xlsx"  # 替换为实际文件路径
#     law_df = read_law_excel(excel_path)
#       # 打印DataFrame内容
#     if not law_df.empty:
#         print("\nDataFrame结构：")
#         print(law_df.info())
#         print("\n前5行数据：")
#         print(law_df.head())
#         print(law_df)
#     else:
#         print("读取文件失败或文件为空。")
#     for _, row in law_df.iterrows():
        #print(f"处理法律：{row['LawName']} 第{row['ArticleNumber']}条")
            name = row['LawName'][:30]  # 截取前30个字符
            content = row['Content'] 
            print(name)
            
            system_prompt = "你是一个数据提取高手"
            legal_text =content
            # 定义用户提示
            str1 = """ 你的任务是将给定的法律文本整理成特定格式的数据列表，并以json格式输出，以便能直接转化为pandas的dataframe格式使用。
            以下是需要处理的法律文本：
            <legal_text>"""

            str2 = """</legal_text>
            请按照以下步骤处理该法律文本：
            <步骤>
            1. 仔细阅读整个法律文本，识别出每个条款的相关信息，包括标题、修订描述、条款序号、条款内容和其他信息。
                - 标题：通常为法律文件的名称，一般在文本开头部分。
                - 修订描述：如果文本中有关于法律修订的说明，将其提取出来。
                - 条款序号：条款序号：用行一开始的标识如“第一条”“第二条”，或者"一、二、"等，用这个用于标识条款的顺序。一般来说，可以用来分割条款的标识应该有比较明显的特征，如换行符，开头总领等。注意这里如果没有“第几条”作为分割标准时，就要用你能识别到的最小的条款单位作为分割标准。比如有一个大的条目“一、”里面有很多小的条目(一)(二)等，要以最小的条目((一)(二))为分割单位，此时条款序号应总结为“一(一)、一(二)“这种，也就是要体现大条目和下面小条目的从属关系。
                - 条款内容：每个条款对应的具体内容。
                - 其他信息：除上述内容外，可能存在的额外信息，当不知道分类为何类型的内容就放到其他信息里。
            2. 对于识别出的每个条款，创建一个字典，包含上述五个字段（标题、修订描述、条款序号、条款内容、其他信息）。
            3. 将所有条款的字典组合成一个列表。
            4. 注意输出内容不可以丢弃输入文本的任何信息，优先将信息分类为前4类，无法归为前4类的则归为第5类“其他信息”。所有输入文本的信息都应该被分类为在上述五类中的某一个。
            </步骤>
            请以json格式输出最终结果，在[]之外不要输出任何东西，就是标准的json格式。输出示例如下：
            [
                {
                    "标题": "示例标题",
                    "修订描述": "示例修订描述",
                    "条款序号": "第一条",
                    "条款内容": "示例条款内容",
                    "其他信息": "示例其他信息"
                },
                {
                    "标题": "示例标题",
                    "修订描述": "示例修订描述",
                    "条款序号": "第二条",
                    "条款内容": "示例条款内容",
                    "其他信息": "示例其他信息"
                }
            ]
            再次注意在[]之外不要输出任何东西，就是标准的json格式,不要在回答最前面加“json"字样，直接从”[“开始输出即可。
            """
            user_prompt = str1+ legal_text+ str2
            try:
                # 调用 API
                response = client.chat.completions.create(
                    model="deepseek-chat",  # 替换为已下载的模型名称
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=1.0,
                    max_tokens=8192
                )
                #print(user_prompt)
                # 提取输出
                output = response.choices[0].message.content
                print(output)
            except Exception as e:
                print(f"调用 API 时出错: {e}")
                with open(error_log, 'a', encoding='utf-8') as f:
                    f.write(f"{name}\n")
                continue
                
                
            # 解析 JSON
            try:
                data: List[Dict] = json.loads(output)
            except json.JSONDecodeError:
                print("错误：无法解析 JSON 数据")
                with open(error_log, 'a', encoding='utf-8') as f:
                    f.write(f"{name}\n")
                continue

            

            # 转换为 DataFrame
            if data:
                df = pd.DataFrame(data)
                #print("转换后的 DataFrame：")
                print(df[["条款序号", "条款内容"]].head())  # 仅展示关键列
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
