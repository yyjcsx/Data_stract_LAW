import re
import pandas as pd
from typing import List, Dict

def legal_text_to_dataframe(text: str) -> pd.DataFrame:
    """
    将法律文本按条目抽取为DataFrame
    :param text: 输入的法律文本内容（字符串）
    :return: 包含条目目录和内容的DataFrame
    """
    # 定义条目匹配正则（支持 第X条/第X款/第X项 等格式）
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

    # 定义编、章、节匹配正则
    volume_pattern = re.compile(r'^第(?:[零一二三四五六七八九十百千万]+|\d+)编', re.MULTILINE)
    chapter_pattern = re.compile(r'^第(?:[零一二三四五六七八九十百千万]+|\d+)章', re.MULTILINE)
    section_pattern = re.compile(r'^第(?:[零一二三四五六七八九十百千万]+|\d+)节', re.MULTILINE)

    # 分割文本为条目块和非条目块
    blocks = []
    current_block = []
    entry_starts = [m.start() for m in entry_pattern.finditer(text)] + [len(text)]  # 末尾作为终止点
    volume_starts = [m.start() for m in volume_pattern.finditer(text)]
    chapter_starts = [m.start() for m in chapter_pattern.finditer(text)]
    section_starts = [m.start() for m in section_pattern.finditer(text)]
    all_starts = sorted(set(entry_starts + volume_starts + chapter_starts + section_starts))

    prev_end = 0
    for start in all_starts:
        block = text[prev_end:start].strip()
        if block:
            blocks.append(block)
        prev_end = start

    # 解析每个块
    result: List[Dict[str, str]] = []
    other_content = []  # 存储非条目内容
    volume_count = 0
    chapter_count = 0
    section_count = 0

    for block in blocks:
        first_line = block.split('\n')[0] if '\n' in block else block
        if volume_pattern.match(first_line):
            volume_count += 1
            chapter_count = 0
            section_count = 0
            result.append({
                "条目目录": volume_pattern.search(first_line).group(),
                "条目内容": re.sub(volume_pattern, '', block, count=1).strip(),
                "编目数": volume_count,
                "章目数": chapter_count,
                "节目数": section_count
            })
        elif chapter_pattern.match(first_line):
            chapter_count += 1
            section_count = 0
            result.append({
                "条目目录": chapter_pattern.search(first_line).group(),
                "条目内容": re.sub(chapter_pattern, '', block, count=1).strip(),
                "编目数": volume_count,
                "章目数": chapter_count,
                "节目数": section_count
            })
        elif section_pattern.match(first_line):
            section_count += 1
            result.append({
                "条目目录": section_pattern.search(first_line).group(),
                "条目内容": re.sub(section_pattern, '', block, count=1).strip(),
                "编目数": volume_count,
                "章目数": chapter_count,
                "节目数": section_count
            })
        elif entry_pattern.match(first_line):
            # 解析条目目录
            entry_header = entry_pattern.search(first_line).group()
            entry_content = re.sub(entry_pattern, '', block, count=1).strip()
            entry_content = re.sub(r'\s+', ' ', entry_content)  # 合并连续空白

            result.append({
                "条目目录": entry_header.strip(),
                "条目内容": entry_content,
                "编目数": volume_count,
                "章目数": chapter_count,
                "节目数": section_count
            })
        else:
            other_content.append(block)

    # 处理其它内容（合并所有非条目块）
    if other_content:
        combined_other = ' '.join(other_content)
        combined_other = re.sub(r'\s+', ' ', combined_other).strip()
        result.append({
            "条目目录": "其它内容",
            "条目内容": combined_other if combined_other else "",
            "编目数": 0,
            "章目数": 0,
            "节目数": 0
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
    test_text = '''
'''

    # 调用函数
    result_df = legal_text_to_dataframe(test_text)

    # 打印结果
    print("提取结果：")
    print(result_df)