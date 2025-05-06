import re
import pandas as pd
from typing import List, Dict

def split_by_length(text: str, max_length=400) -> List[str]:
    """按段落末尾就近分割文本"""
    # 添加三个正则表达式定义
    volume_pattern = re.compile(r'^第([零一二三四五六七八九十百千万]+)编\s*(.*)')
    chapter_pattern = re.compile(r'^第([零一二三四五六七八九十百千万]+)章\s*(.*)') 
    section_pattern = re.compile(r'^第([零一二三四五六七八九十百千万]+)节\s*(.*)')
    
    blocks = []
    current_block = []
    current_len = 0
    
    # 先按自然段落分割
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    for para in paragraphs:
        # 处理编章节段落（保持原有逻辑）
        if any(re_pattern.match(para) for re_pattern in [volume_pattern, chapter_pattern, section_pattern]):
            blocks.append(para)
            continue
            
        # 普通段落处理
        if len(para) <= max_length:
            blocks.append(para)
        else:
            # 按句号就近分割
            sentences = re.split(r'(。|；)', para)
            buffer = ''
            for sent in sentences:
                if len(buffer) + len(sent) > max_length and buffer:
                    blocks.append(buffer)
                    buffer = sent
                else:
                    buffer += sent
            if buffer:
                blocks.append(buffer)
    
    return blocks

def legal_text_to_dataframe(text: str) -> pd.DataFrame:
    # 正则表达式定义
    volume_pattern = re.compile(r'^第([零一二三四五六七八九十百千万]+)编\s*(.*)')
    chapter_pattern = re.compile(r'^第([零一二三四五六七八九十百千万]+)章\s*(.*)')
    section_pattern = re.compile(r'^第([零一二三四五六七八九十百千万]+)节\s*(.*)')

    blocks = split_by_length(text)
    
    # 初始化数据结构
    result = []
    current_volume = {"number": "", "name": ""}
    current_chapter = {"number": "", "name": ""}
    current_section = {"number": "", "name": ""}

    # 修改处理逻辑，优先处理编章节
    block_counter = 1  # 块计数器现在放在循环内部重置
    for block in blocks:
        first_line = block.split('\n')[0] if '\n' in block else block
        
        # 处理编层级
        if volume_pattern.match(first_line):
            match = volume_pattern.match(first_line)
            current_volume = {
                "number": f"第{match.group(1)}编",
                "name": match.group(2)
            }
            block_counter = 1  # 重置块计数器
            result.append({
                "编索引": current_volume["number"],
                "编名称": current_volume["name"],
                "章索引": "",
                "章名称": "",
                "条目目录": "",
                "条目内容": block.replace(match.group(0), '').strip()
            })
            continue
            
        # 处理章层级
        if chapter_pattern.match(first_line):
            match = chapter_pattern.match(first_line)
            current_chapter = {
                "number": f"第{match.group(1)}章",
                "name": match.group(2)
            }
            block_counter = 1  # 重置块计数器
            result.append({
                "编索引": current_volume["number"],
                "编名称": current_volume["name"],
                "章索引": current_chapter["number"],
                "章名称": current_chapter["name"],
                "条目目录": "",
                "条目内容": block.replace(match.group(0), '').strip()
            })
            continue
            
        # 处理普通段落（保持字数分割）
        result.append({
            "条目目录": f"第{block_counter}块",
            "条目内容": block,
            "编索引": current_volume["number"],
            "编名称": current_volume["name"],
            "章索引": current_chapter["number"],
            "章名称": current_chapter["name"]
        })
        block_counter += 1

    # 过滤空条目并创建DataFrame
    df = pd.DataFrame([x for x in result if x["条目内容"].strip()])
    return df[["编索引", "编名称", "章索引", "章名称", "条目目录", "条目内容"]]