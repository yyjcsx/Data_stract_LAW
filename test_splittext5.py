import pandas as pd
from splittext5 import legal_text_to_dataframe

def test_length_based_split():
    test_text = """
第1编 总则
第1章 基本原则

这里是一个超过400字符的测试段落。法律应当遵循以下原则：（此处省略重复文本）...该段落将被分割成多个块。根据法律条文的具体内容，系统需要自动识别段落中的自然分割点，当累计字符数接近400时，在最近的句号或分号处进行分割。本测试旨在验证分割逻辑的准确性和可靠性，确保分割后的每个文本块长度不超过400字符且保持语义完整性。最终生成的DataFrame应包含正确的'第X块'条目目录和对应的文本内容。该测试用例将验证以下功能点：1. 长段落智能分割 2. 块编号自动生成 3. 编章节信息保留。

第2章 权利保护
三、民事权利的具体内容...
"""

    df = legal_text_to_dataframe(test_text)
    
    # 验证基本结构
    # assert isinstance(df, pd.DataFrame)
    # assert not df.empty
    
    # # 验证分割块数
    # long_paragraph_entries = df[df["条目目录"].str.startswith("第") & df["条目目录"].str.contains("块")]
    # assert len(long_paragraph_entries) >= 2, "应至少分割成2个块"
    
    # # 验证最大长度
    # assert all(len(content) <= 400 for content in long_paragraph_entries["条目内容"])
    
    # # 验证块编号连续性
    # block_numbers = [int(entry.split("第")[1].split("块")[0]) 
    #                 for entry in long_paragraph_entries["条目目录"]]
    # assert block_numbers == sorted(block_numbers), "块编号应连续递增"
    
    # # 验证编章节保留
    # assert df[df["编名称"] == "总则"]["章名称"].iloc[0] == "基本原则"
    
    # print("所有分割测试通过！")
    print(df)
if __name__ == "__main__":
    test_length_based_split()