import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from scipy import optimize
import itertools
from typing import List, Dict, Tuple, Optional
import random
import json


hc = []
cap = []
#1 refers to index 0 (bloomberg), 2 refers to index 1 (costar)...
category_names = []
team_names = []
links = []
all_mlh = []
in_person = []

def process(csv_file):
    global category_names, team_names, links
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        #for every each category row in the csv, split by commas to get each category
        for row in reader:
            if (row[2].strip() == "Draft"):
                continue
            team_name = row[0].strip()
            team_names.append(team_name)
            link = row[1].strip()
            links.append(link)

            in_person.append(row[15].strip())
            
            categories = row[9].split(',')
            append = []
            mlh = []
            for category in categories:
                if category.strip():
                    #for every category, ignore MLH
                    if not category.strip().endswith("Major League Hacking"):
                        #append it to the array for that hack
                        append.append(category.strip())
                        #if it isn't in the cap array, add it
                        if category.strip() not in cap:
                            cap.append(category.strip())
                    else:
                        mlh.append(category.strip())
            hc.append(append)
            all_mlh.append(mlh)
        category_names = cap.copy()
        #assume one judging group for each category
        for i in range(0, len(cap)):
            cap[i] = 1

        #check if group signed up for more than three bitcamp categories. if true, remove bitcamp categories until = 3
        for sub_arr in hc:
            bitcamp_count = sum(1 for s in sub_arr if s.endswith('Bitcamp'))
            if bitcamp_count > 3:
                bitcamp_indices = [i for i, s in enumerate(sub_arr) if s.endswith('Bitcamp')]
                indices_to_remove = random.sample(bitcamp_indices, bitcamp_count - 3)
                sub_arr[:] = [s for i, s in enumerate(sub_arr) if i not in indices_to_remove]

        #change hc to index numbering
        for i in range(0, len(hc)):
            for j in range(0, len(hc[i])):
                hc[i][j] = category_names.index(hc[i][j])

csv_file = "backend/bitcamp-2023-projects.csv"
process(csv_file)
# print(hc)
# print(cap)
# print()

# print(category_names)
cap = [5, 2, 5, 4, 4, 4, 4, 4, 4, 2, 4, 4, 1, 4, 4, 1, 4]
# print(team_names)

def abstract_expo_alg(hc: List[List[int]], cap: List[int], t_max: int):
    # extracting sizes
    M = len(hc)
    N = len(cap)
    
    # bookkeeping for valid (h, j) pairs
    valid_hj = set()
    for h, req_cat in enumerate(hc):
        for j in req_cat:
            valid_hj.add((h, j))
    hj_to_i_base = dict(map(tuple, map(lambda t: t[::-1], list(enumerate(valid_hj)))))

    def solve_expo(T: int):
        # index bookkeeping
        num_var = len(valid_hj) * T
        def hjt_to_i(h: int, j: int, t: int) -> int:
            return len(valid_hj) * (t-1) + hj_to_i_base[(h, j)]

        # first condition
        A1 = np.zeros((len(valid_hj), num_var))
        for x, (h, j) in enumerate(valid_hj):
            for t in range(T):
                A1[x, hjt_to_i(h, j, t)] = 1
        b1= np.ones(len(valid_hj))

        # second condition
        A2 = np.zeros((N*T, num_var))
        for x, (j, t) in enumerate(itertools.product(range(N), range(T))):
            for h in range(M):
                if (h, j) not in valid_hj:
                    continue
                A2[x, hjt_to_i(h, j, t)] = 1
        b2 = np.repeat(cap, T)

        # third condition
        A3 = np.zeros((M*T, num_var))
        for x, (h, t) in enumerate(itertools.product(range(M), range(T))):
            for j in range(N):
                if (h, j) not in valid_hj:
                    continue
                A3[x, hjt_to_i(h, j, t)] = 1
        b3 = np.ones(M*T)

        # solve linear program
        x = scipy.optimize.milp(
            c=-np.ones(num_var),
            constraints=[
                scipy.optimize.LinearConstraint(A1, 0, b1),
                scipy.optimize.LinearConstraint(A2, 0, b2),
                scipy.optimize.LinearConstraint(A3, 0, b3)
            ],
            bounds=scipy.optimize.Bounds(lb=0, ub=1),
            integrality=1
        ).x
        if int(sum(x)) < len(valid_hj):
            return None

        # interpret solution
        H = [list() for _ in range(M)]
        J = [list() for _ in range(N)]
        for j in range(N):
            J[j] = [list() for _ in range(T)]
            for h in range(M):
                if (h, j) not in valid_hj:
                    continue
                for t in range(T):
                    if x[hjt_to_i(h, j, t)] == 1.0:
                        H[h].append((j, t))
                        J[j][t].append(h)
        return (H, J)

    # return solve_expo(t_max)
    # binary search:
    a, b = 1, t_max
    while a < b-1:
        m = int(np.ceil((a+b)/2))
        soln = solve_expo(m)
        if soln is None: # failure
            a = m+1
        else: # success
            b = m

    # check when 2 left
    if a == b:
        t = a
    else:
        if solve_expo(a) is None:
            t = b
        else:
            t = a

    # return optimal solution
    H, J = solve_expo(t)
    return (t, H, J)

t, H, J = abstract_expo_alg(hc, cap, 32)
# print(t)
# print()
# print(H)
# print()
# print(J)

for i in range(len(H)):
    for j in range(len(H[i])):
        H[i][j] = (category_names[H[i][j][0]], H[i][j][1])

# print(H)

final_cat_names = []

# print(category_names)

for val in category_names:
    if (val[val.index("- ") + 2: ] != "Bitcamp"):
        final_cat_names.append(val[val.index("- ") + 2: ] + " - " + val[0:val.index(" -")])
    else:
        final_cat_names.append(val)

combined = []

tables = []
for i in range(20):
    letter = chr(ord('A') + i)
    if letter == 'K' or letter == 'L':
        tables.extend([letter + str(j) for j in range(1, 13) if j not in (3, 4, 5)])
    else:
        tables.extend([letter + str(j) for j in range(1, 13)])

judge = "Judge"
max = 0

tableCounter = 0
in_person_count = 0
for i in range(0, len(in_person)):
    if in_person[i] == "Yes":
        in_person_count += 1
in_person_arr = random.sample(range(in_person_count), in_person_count)

for i in range(len(team_names)):
    H_new = []
    if (H[i] != []):
        for j in range(len(H[i])):
            if (H[i][j][0][H[i][j][0].index("- ") + 2: ] == "Bitcamp"):
                H_new.append([H[i][j][0][0:H[i][j][0].index(" -")], H[i][j][0][H[i][j][0].index("- ") + 2: ], judge, H[i][j][1]])
            else:
                H_new.append([H[i][j][0][H[i][j][0].index("- ") + 2: ], H[i][j][0][0:H[i][j][0].index(" -")], judge, H[i][j][1]])
            
            if H[i][j][1] > max:
                max = H[i][j][1]
    
    H_new.sort(key=lambda x: x[-1])

    for category in all_mlh[i]:
        append = []
        append.append(category.split(" - "))
        H_new.append(append[0])


    if in_person[i] == "Yes":
        data = [
            ["Yes", tables[in_person_arr[tableCounter]]],
            team_names[i],
            H_new,
        ]
        tableCounter += 1
    else:
        data = [
            ["No"],
            team_names[i],
            H_new,
        ]
    combined.append(data)
print(max)

names_links = []
for i in range(len(team_names)):
    names_links.append([team_names[i], links[i]])

data = {
    "t": t,
    "H": H,
    "J": J,
    "category_names": final_cat_names,
    "team_names": names_links,
    "combined_values": combined,
    "total_times" : max
}

with open('frontend/public/expo_algorithm_results.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
