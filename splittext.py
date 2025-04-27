import re
import pandas as pd
from typing import List, Dict

def legal_text_to_dataframe(text: str) -> pd.DataFrame:
    """
    将法律文本按条目抽取为DataFrame
    :param text: 输入的法律文本内容（字符串）
    :return: 包含条目目录和内容的DataFrame
    """
    # 定义条目匹配正则（支持 第X条/第XX条/第X款/第X项 等格式）
    entry_pattern = re.compile(
        r'''
        ^\s*                # 行首可能的空白
        第                  # 固定起始字
        (?:[零一二三四五六七八九十百千万]+|\d+)  # 数字（中文/阿拉伯）
        (条|款|项)          # 条目类型
        \s*[:：]?\s*        # 可能的分隔符（冒号/空格）
        ''',
        re.VERBOSE | re.MULTILINE
    )

    # 分割文本为条目块和非条目块
    blocks = []
    current_block = []
    entry_starts = [m.start() for m in entry_pattern.finditer(text)] + [len(text)]  # 末尾作为终止点
    
    prev_end = 0
    for start in entry_starts:
        block = text[prev_end:start].strip()
        if block:
            blocks.append(block)
        prev_end = start

    # 解析每个块
    result: List[Dict[str, str]] = []
    other_content = []  # 存储非条目内容
    
    for block in blocks:
        first_line = block.split('\n')[0] if '\n' in block else block
        if entry_pattern.match(first_line):
            # 解析条目目录
            entry_header = entry_pattern.search(first_line).group()
            entry_content = re.sub(entry_pattern, '', block, count=1).strip()
            entry_content = re.sub(r'\s+', ' ', entry_content)  # 合并连续空白
            
            result.append({
                "条目目录": entry_header.strip(),
                "条目内容": entry_content
            })
        else:
            other_content.append(block)
    
    # 处理其它内容（合并所有非条目块）
    if other_content:
        combined_other = ' '.join(other_content)
        combined_other = re.sub(r'\s+', ' ', combined_other).strip()
        result.append({
            "条目目录": "其它内容",
            "条目内容": combined_other if combined_other else ""
        })

    # 转换为DataFrame
    df = pd.DataFrame(result)
    
    # 新增处理状态判断
    if len(df) == 1 and df.iloc[0]['条目目录'] == '其它内容':
        df['处理状态'] = '仅含其他内容'
    else:
        df['处理状态'] = '正常处理'
    
    return df


if __name__ == "__main__":
    # 测试用法律文本
    test_text = '''关于印发《生态环境执法人员行为规范》的通知 环执法〔2024〕2号 各省、自治区、直辖市生态环境厅(局),新疆生产建设兵团生态环境局,机关各部门,环境应急与事故调查中心,各督察局,各核与辐射安全监督站,各流域海域生态环境监督管理局: 为进一步加强生态环境执法队伍建设,促进严格、规范、公正、文明、廉洁执法,根据《中华人民共和国环境保护法》《中华人民共和国行政处罚法》及《生态环境行政处罚办法》等法律法规规章,结合执法工作实际,我部修订了《生态环境执法人员行为规范》,并经2023年第16次部常务会议审议通过。现印发给你们,请遵照执行。 生态环境部 2024年1月3日 (此件社会公开)
    '''
    
    # 调用函数
    result_df = legal_text_to_dataframe(test_text)
    
    # 打印结果
    print("提取结果：")
    print(result_df)