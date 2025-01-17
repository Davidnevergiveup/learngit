import csv
import random
import time
from datetime import datetime

# 记录已记忆单词的时间
memory_log = {}

# 从CSV文件中读取单词列表
def load_words(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题
        return [row[0] for row in reader]

# 保存记忆记录到日志文件
def save_memory_log(log_file):
    with open(log_file, 'w', encoding='utf-8') as file:
        for word, timestamps in memory_log.items():
            file.write(f"{word}: {', '.join(timestamps)}\n")

# 加载记忆记录
def load_memory_log(log_file):
    try:
        with open(log_file, 'r', encoding='utf-8') as file:
            for line in file:
                word, timestamps = line.strip().split(': ')
                memory_log[word] = timestamps.split(', ')
    except FileNotFoundError:
        pass

# 获取已记忆单词的索引范围
def get_memory_ranges(words):
    indices = sorted([words.index(word) for word in memory_log if word in words])
    if not indices:
        return "无已记忆单词"
    
    ranges = []
    start = indices[0]
    for i in range(1, len(indices)):
        if indices[i] != indices[i - 1] + 1:  # 中断
            ranges.append((start, indices[i - 1]))
            start = indices[i]
    ranges.append((start, indices[-1]))
    
    return ', '.join(f"{a+1}-{b+1}" if a != b else f"{a+1}" for a, b in ranges)

# 主函数
def main():
    csv_file = "processed_content.csv"  # 单词CSV文件
    log_file = "memory_log.txt"         # 记忆日志文件
    words = load_words(csv_file)
    load_memory_log(log_file)

    while True:
        print("\n已记忆单词索引范围：")
        print(get_memory_ranges(words))

        start = int(input("\n请输入要记忆的起始单词序号：")) - 1
        end = int(input("请输入要记忆的结束单词序号："))
        selected_words = words[start:end]

        times_to_review = int(input("\n请输入每个单词要记忆的次数："))
        mode = input("请选择记忆模式（顺序: 's', 随机: 'r'）：").strip().lower()

        print("\n开始记忆...")
        start_time = time.time()
        for _ in range(times_to_review):
            if mode == 'r':
                random.shuffle(selected_words)
            for word in selected_words:
                print(word)
                input("按回车键继续...")
                if word not in memory_log:
                    memory_log[word] = []
                memory_log[word].append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        end_time = time.time()

        print(f"\n本次记忆完成，总耗时 {end_time - start_time:.2f} 秒")
        save_memory_log(log_file)

        cont = input("\n是否继续记忆？（是: 'y', 否: 'n'）：").strip().lower()
        if cont != 'y':
            print("感谢使用！")
            break

if __name__ == "__main__":
    main()