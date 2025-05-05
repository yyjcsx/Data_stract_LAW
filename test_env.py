#测试是否能成功使用代码生成excel文件并写入文件夹
import pandas as pd
import os

def test_excel_write():
    # 测试数据
    data = {
        "列1": ["数据1", "数据2", "数据3"],
        "列2": [1, 2, 3],
        "列3": ["A", "B", "C"]
    }
    df = pd.DataFrame(data)
    
    # 创建测试文件夹
    test_folder = "./地方规范性文件"
    os.makedirs(test_folder, exist_ok=True)
    
    # 测试文件路径
    test_file = os.path.join(test_folder, "test_output.xlsx")
    
    try:
        # 尝试写入Excel文件
        df.to_excel(test_file, index=False, engine='openpyxl')
        print(f"测试文件已成功生成: {os.path.abspath(test_file)}")
        
        # 验证文件是否存在
        if os.path.exists(test_file):
            print("验证成功: 文件已正确写入")
        else:
            print("验证失败: 文件未生成")
            
    except Exception as e:
        print(f"写入Excel文件时出错: {str(e)}")
        print("可能的原因:")
        print("1. 文件夹写入权限不足")
        print("2. 文件被其他程序占用")
        print("3. 防病毒软件阻止了写入操作")

if __name__ == "__main__":
    test_excel_write()

#可以写入并放入文件夹