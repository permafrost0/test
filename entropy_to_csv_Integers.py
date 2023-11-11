import csv
from pyomo.environ import *
from pyomo.opt import SolverFactory
from tqdm import tqdm

STEP = 4 # 乱数の刻み 1e-□ 

SIZE = 7 # 要素数 + 1 
TOTAL = 10000 
N = 100

PATH = str(N) + "_" + str(SIZE - 1) + ".csv"
CSV_INPUT_PATH = "csv/data/" + PATH
CSV_OUTPUT_PATH_1 = "csv/result/integers/dist/" + PATH
CSV_OUTPUT_PATH_2 = "csv/result/integers/entropy/" + PATH
CSV_OUTPUT_PATH_3 = "csv/result/integers/count/" + PATH

data_list = []
results = []

with open(CSV_INPUT_PATH, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        data_dict = {i + 1: round(float(value) * TOTAL, STEP) for i, value in enumerate(row)}
        data_list.append(data_dict)


with open(CSV_OUTPUT_PATH_1, 'w', newline='') as csvfile:
    for n in tqdm(range(0, len(data_list), 2), desc="Processing", ncols=100):
        # モデルの定義
        model = ConcreteModel()
        # model.m = Var(range(1, SIZE), range(1, SIZE), domain=NonNegativeReals) 
        model.m = Var(range(1, SIZE), range(1, SIZE), domain=NonNegativeIntegers) 

        # 制約条件の定義   
        model.sum_constraint1 = ConstraintList()
        for i in range(1, SIZE):
            model.sum_constraint1.add(sum(model.m[i, j] for j in range(1, SIZE)) == data_list[n][i])
        model.sum_constraint2 = ConstraintList()
        for j in range(1, SIZE):
            model.sum_constraint2.add(sum(model.m[i, j] for i in range(1, SIZE)) == data_list[n + 1][j])
        def sum_probability_rule(model):
            return sum(model.m[i, j] for i in range(1, SIZE) for j in range(1, SIZE)) == TOTAL
        model.sum_probability_constraint = Constraint(rule=sum_probability_rule)

        # 目的関数の定義
        def entropy_rule(model):
            entropy = -sum(model.m[i, j] / TOTAL * log(model.m[i, j] / TOTAL + 1e-2) / log(2) for i in range(1, SIZE) for j in range(1, SIZE))
            return entropy
        model.obj = Objective(rule=entropy_rule, sense=minimize)

        # ソルバーの設定と実行
        solver = SolverFactory('couenne')
        solver.solve(model)

        dist = []
        for i in range(1, SIZE):
            for j in range(1, SIZE):
                dist.append(round(value(model.m[i, j]) / TOTAL, STEP))

        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(dist)


with open(CSV_OUTPUT_PATH_1, 'r') as csv_file:
    csvreader = csv.reader(csv_file)
    data_array = []
    for row in csvreader:
        data_array.append([float(element) for element in row])

ent_list = []
count_list = []

for i in range(len(data_array)):
    ent = 0
    count = 0
    for j in range((SIZE - 1) ** 2):
        if data_array[i][j] == 0:
            pass
        else:
            ent -= data_array[i][j] * log(data_array[i][j]) / log(2)
            count += 1
    ent_list.append(round(ent, 6))
    count_list.append(count)


with open(CSV_OUTPUT_PATH_2, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    for result in ent_list:
        csv_writer.writerow([result])

with open(CSV_OUTPUT_PATH_3, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    for result in count_list:
        csv_writer.writerow([result])