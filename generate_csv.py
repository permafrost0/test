import csv
import random

SIZE = 3 # 要素数 - 1
STEP = 10000 # 刻み
N = 10 # 組み合わせ数

CSV_INPUT_FILE = "csv/data/" + str(N) + "_" + str(SIZE + 1) + ".csv"

with open(CSV_INPUT_FILE, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    for _ in range(N * 2):
        rand_list = [0]
        data_list = []
        while SIZE + 1 > len(rand_list):
            n = random.randrange(0, 1 * STEP, 1) / STEP
            if n not in rand_list:
                rand_list.append(n)
        rand_list.sort()
        rand_list.append(1)
        for i in range(SIZE + 1):
            data_list.append(round(rand_list[i + 1] - rand_list[i], 4))
        csv_writer.writerow(data_list)

