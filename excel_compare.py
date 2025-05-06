# import pandas as pd

# # 读取 Excel 文件
# excel1 = pd.read_excel('D:\LAW_py\Data_stract_LAW\processed_files2.xlsx')
# excel2 = pd.read_excel('D:\LAW_py\Data_stract_LAW\processed_test.xlsx')

# # 获取 excel1 中第一列（处理后的文件名）的所有文件名
# processed_files = excel1['处理后的文件名'].tolist()

# # 遍历 excel2 中的每一行
# for index, row in excel2.iterrows():
#     # 检查当前行的标题是否在已处理文件名列表中
#     if row['标题'] in processed_files:
#         # 如果存在，则在 O 列标注为已处理
#         excel2.at[index, 'P'] = '已处理'

# # 保存修改后的 excel2 到新文件
# excel2.to_excel('output.xlsx', index=False)    
'''数据量一大就抽风↑，速度还慢'''
'''在数据量比较大的时候会抽风↓，但是用了isin函数速度快了不少'''
import pandas as pd

# 读取 Excel 文件
excel1 = pd.read_excel('D:\\LAW_py\\Data_stract_LAW\\processed_files2.xlsx')
excel2 = pd.read_excel('D:\\LAW_py\\Data_stract_LAW\\processed_test.xlsx')

# 获取 excel1 中第一列（处理后的文件名）的所有文件名，并统一格式
processed_files = excel1['处理后的文件名'].str.strip().str.lower().tolist()

# 统一 excel2 中标题列的格式
excel2['标题'] = excel2['标题'].str.strip().str.lower()

# 使用 isin() 方法进行匹配
mask = excel2['标题'].isin(processed_files)

# 在 P 列标注为已处理
excel2.loc[mask, 'P'] = '已处理'

# 保存修改后的 excel2 到新文件
excel2.to_excel('output.xlsx', index=False)
# '''分block排查 
# D:\\LAW_py\\Data_stract_LAW\\processed_files2.xlsx 
# D:\\LAW_py\\Data_stract_LAW\\processed_test.xlsx'''
# import os
# import pandas as pd

# # 读取 excel1 数据
# excel1 = pd.read_excel(r'D:\\LAW_py\\Data_stract_LAW\\processed_files2.xlsx')
# # 获取 excel1 中第一列（处理后的文件名）的所有文件名，并统一格式
# processed_files = excel1['处理后的文件名'].str.strip().str.lower().tolist()

# # 定义分块大小
# chunk_size = 10000
# # 手动分块读取 excel2 数据
# start = 0
# while True:
#     try:
#         chunk = pd.read_excel(r'D:\\LAW_py\\Data_stract_LAW\\processed_test.xlsx', skiprows=start, nrows=chunk_size)
#         if chunk.empty:
#             break
#         # 统一当前块中标题列的格式
#         chunk['标题'] = chunk['标题'].str.strip().str.lower()
#         # 使用 isin() 方法进行匹配
#         mask = chunk['标题'].isin(processed_files)
#         # 在 P 列标注为已处理
#         chunk.loc[mask, 'P'] = '已处理'

#         # 判断 output.xlsx 文件是否存在
#         if os.path.exists('output.xlsx'):
#             # 如果文件存在，以追加模式写入数据，不写表头
#             with pd.ExcelWriter('output.xlsx', mode='a', engine='openpyxl') as writer:
#                 chunk.to_excel(writer, index=False, header=False)
#         else:
#             # 如果文件不存在，正常写入数据，写表头
#             chunk.to_excel('output.xlsx', index=False)

#         start += chunk_size
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         break