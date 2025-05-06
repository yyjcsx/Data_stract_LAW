import pandas as pd
from splittext3 import legal_text_to_dataframe1

# 测试包含中文数字编号的法律文本
test_text = """
第1编 总则
第1章 基本原则

一、为了保护民事权益，维护社会秩序，适应中国特色社会主义发展要求，制定本法。
本法的解释权归最高人民法院所有。

二、民事主体的人身权利、财产权利以及其他合法权益受法律保护，任何组织或者个人不得侵犯。

第2章 民事权利
三、民事主体从事民事活动，应当遵循自愿原则，按照自己的意思设立、变更、终止民事法律关系。

【其他内容】本法自公布之日起施行。
"""

def test_chinese_number_entries():
    df = legal_text_to_dataframe1(test_text)
    
    # 验证基本结构
    # assert isinstance(df, pd.DataFrame)
    # assert not df.empty
    # assert {"编索引", "编名称", "章索引", "章名称", "条目目录", "条目内容"}.issubset(df.columns)
    
    # # 验证编章节信息
    # assert df[df["条目目录"] == "一、"]["编名称"].iloc[0] == "总则"
    # assert df[df["条目目录"] == "三、"]["章名称"].iloc[0] == "民事权利"
    
    # # 验证中文数字条目
    # entries = df[df["条目目录"].str.contains("、")]
    # assert len(entries) >= 3, "应至少解析出3个中文数字条目"
    
    # # 验证条目内容完整性
    # first_entry = df[df["条目目录"] == "一、"]["条目内容"].iloc[0]
    # assert "最高人民法院" in first_entry
    
    # print("测试通过！")
    print(df)  # 打印DataFrame以查看结果，方便调试和检查

if __name__ == "__main__":
    test_chinese_number_entries()