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
    item_pattern = re.compile(
        r'^\s*([一二三四五六七八九十]+)[、.]\s*(.*)',
        re.MULTILINE
    )
    # 定义编、章、节匹配正则
    volume_pattern = re.compile(
        r'^(第(?:[零一二三四五六七八九十百千万]+|\d+)编)\s*(.*)',
        re.MULTILINE
    )
    chapter_pattern = re.compile(
        r'^(第(?:[零一二三四五六七八九十百千万]+|\d+)章)\s*(.*)',
        re.MULTILINE
    )
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
    
    # 修改结构层级变量初始化
    current_volume = {"index": 0, "name": "", "content": "", "number": ""}
    current_chapter = {"index": 0, "name": "", "content": "", "number": ""}
    current_section = {"index": 0, "name": "", "content": "", "number": ""}

    for block in blocks:
        first_line = block.split('\n')[0] if '\n' in block else block
        if volume_pattern.match(first_line):
            # 处理编层级
            current_volume["index"] += 1
            match = volume_pattern.match(first_line)
            current_volume["name"] = match.group(2)  # 获取"总则"部分
            current_volume["number"] = match.group(1)  # 获取"第1编"
            content = block.replace(match.group(0), '').strip()
            
            result.append({
                "编索引": current_volume["number"],
                "编名称": current_volume["name"],
                "章索引": "",
                "章名称": "",
                "节索引": "",
                "节名称": "",
                "条目目录": "",
                "条目内容": content
            })

        elif chapter_pattern.match(first_line):
            # 处理章层级
            current_chapter["index"] += 1
            match = chapter_pattern.match(first_line)
            current_chapter["name"] = match.group(2)  # 获取"基本原则"
            current_chapter["number"] = match.group(1)  # 获取"第1章"
            content = block.replace(match.group(0), '').strip()
            
            result.append({
                "编索引": current_volume["number"],
                "编名称": current_volume["name"],
                "章索引": current_chapter["number"],
                "章名称": current_chapter["name"],
                "节索引": "",
                "节名称": "",
                "条目目录": "",
                "条目内容": content
            })

        elif entry_pattern.match(first_line):
            # 处理条目（强制填充层级信息）
            entry_header = entry_pattern.search(first_line).group()
            entry_content = re.sub(entry_pattern, '', block, count=1).strip()
            
            result.append({
                "编索引": current_volume["number"],
                "编名称": current_volume["name"],
                "章索引": current_chapter["number"] if current_chapter["index"] > 0 else "",
                "章名称": current_chapter["name"] if current_chapter["index"] > 0 else "",
                "节索引": current_section["number"] if current_section["index"] > 0 else "",
                "节名称": current_section["name"] if current_section["index"] > 0 else "",
                "条目目录": entry_header.strip(),
                "条目内容": entry_content
            })
            
        elif section_pattern.match(first_line):
            # 处理节层级
            current_section["index"] += 1
            current_section["name"] = section_pattern.search(first_line).group()
            current_section["content"] = re.sub(section_pattern, '', block, count=1).strip()
            
            result.append({
                "编索引": current_volume["index"],
                "编名称": current_volume["name"],
                "章索引": current_chapter["index"],
                "章名称": current_chapter["name"],
                "节索引": current_section["index"],
                "节名称": current_section["name"],
                "节目录内容": current_section["content"],
                "条目目录": "",
                "条目内容": ""
            })
            
        elif item_pattern.match(first_line):
            # 处理"一、二、"格式的条目
            match = item_pattern.match(first_line)
            item_number = match.group(1)
            item_content = match.group(2)
            
            result.append({
                "编索引": current_volume["number"],
                "编名称": current_volume["name"],
                "章索引": current_chapter["number"] if current_chapter["index"] > 0 else "",
                "章名称": current_chapter["name"] if current_chapter["index"] > 0 else "",
                "节索引": current_section["number"] if current_section["index"] > 0 else "",
                "节名称": current_section["name"] if current_section["index"] > 0 else "",
                "条目目录": f"第{item_number}项",
                "条目内容": item_content
            })
            
        elif entry_pattern.match(first_line):
            # 处理条目（保持原有逻辑并添加层级信息）
            entry_header = entry_pattern.search(first_line).group()
            entry_content = re.sub(entry_pattern, '', block, count=1).strip()
            
            result.append({
                "编索引": current_volume["index"],
                "编名称": current_volume["name"],
                "章索引": current_chapter["index"],
                "章名称": current_chapter["name"],
                "节索引": current_section["index"],
                "节名称": current_section["name"],
                "条目目录": entry_header.strip(),
                "条目内容": entry_content,
                "编目录内容": "",
                "章目录内容": "",
                "节目录内容": ""
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

    # 转换为DataFrame前过滤空条目
    filtered_result = [
        entry for entry in result 
        if not (entry["条目目录"] == "" and entry["条目内容"] == "")
    ]

    # 转换为DataFrame
    df = pd.DataFrame(filtered_result)

    # 新增处理状态判断
    if len(df) == 1 and df.iloc[0]['条目目录'] == '其它内容':
        df['处理状态'] = '仅含其他内容'
    else:
        df['处理状态'] = '正常处理'

    return df


