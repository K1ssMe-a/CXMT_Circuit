import csv
import numpy as np

# def read_csv_to_list(file_path):
#     data_list = []
#     with open(file_path, mode='r', encoding='utf-8') as file:
#         csv_reader = csv.reader(file)
#         for row in csv_reader:
#             data_list.append(row[0])
#     return data_list

# csv_files = [
#     '/Users/k1ssme/program/trace/in_API.csv',
#     '/Users/k1ssme/program/trace/in_code.csv',
#     '/Users/k1ssme/program/trace/in_conv.csv',
#     '/Users/k1ssme/program/trace/out_API.csv',
#     '/Users/k1ssme/program/trace/out_code.csv',
#     '/Users/k1ssme/program/trace/out_conv.csv'
# ]

# list_in_API = np.array(read_csv_to_list(csv_files[0])[1:], dtype=np.int32)
# list_in_code = np.array(read_csv_to_list(csv_files[1])[1:], dtype=np.int32)
# list_in_conv = np.array(read_csv_to_list(csv_files[2])[1:], dtype=np.int32)
# list_out_API = np.array(read_csv_to_list(csv_files[3])[1:], dtype=np.int32)
# list_out_code = np.array(read_csv_to_list(csv_files[4])[1:], dtype=np.int32)
# list_out_conv = np.array(read_csv_to_list(csv_files[5])[1:], dtype=np.int32)


def process(data_list: str, name: str):
    # population = np.bincount(data_list)  # 处理负数

    # 保存和加载（可选）
    # np.save(f'{name}.npy', population)
    population_loaded = np.load(f'{name}.npy')

    # 随机采样 5 个数字
    numbers = np.arange(len(population_loaded))
    sampled_numbers = np.random.choice(numbers, size=5, p=population_loaded/np.sum(population_loaded))

    print("Sampled numbers:", sampled_numbers)

if __name__ == '__main__':
    process(None, 'list_in_API')
    process(None, 'list_in_code')
    process(None, 'list_in_conv')
    process(None, 'list_out_API')
    process(None, 'list_out_code')
    process(None, 'list_out_conv')


