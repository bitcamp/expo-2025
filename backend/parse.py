# pylint: disable=invalid-name
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
import uuid
import random
from collections import defaultdict

from datetime import datetime, timedelta
import pytz

random.seed(10)

DRAFT_COLUMN_NAME = 'Project Status'
TEAM_COLUMN_NAME = 'Project Title'
LINK_COLUMN_NAME = 'Submission Url'
IN_PERSON_COLUMN_NAME = 'Will You Be Present To Demo In Person On Sunday?'
CHALLENGES_COLUMN_NAME = 'Opt-In Prizes'
TRACK_CHALLENGE_COLUMN_NAME = 'Bitcamp Track Challenge'
TRACK_HACK_OPT_OUT_RESPONSE = "I don't want to submit to a Bitcamp track challenge. I understand that I can still submit to the other Bitcamp sponsored challenges."
BITCAMP_PRIZE_1 = "Bitcamp Sponsored Prize Category #1"
BITCAMP_PRIZE_2 = "Bitcamp Sponsored Prize Category #2"
BITCAMP_PRIZE_3 = "Bitcamp Sponsored Prize Category #3"
ALUMNI_PRIZE_1 = "Alumni Team Prize Category #1"
ALUMNI_PRIZE_2 = "Alumni Team Prize Category #2"

hc = []
cap = []
# 1 refers to index 0 (bloomberg), 2 refers to index 1 (costar)...
category_names = []
team_names = []
links = []
all_mlh = []
in_person = []

MLH_HACKS = set([
    "[MLH] Best Use of .Tech",
    "[MLH] Best AI Application Built with Cloudflare",
    "[MLH] Best Use of MongoDB Atlas",
    "[MLH] Best Use of Gemimi API",
])

BITCAMP_TRACK_HACKS = set([
    "Best Machine Learning Track Hack - Bitcamp",
    "Best App Dev Track Hack - Bitcamp",
    "Best Cybersecurity Track Hack - Bitcamp",
    "Beginner Quantum Track Hacks - Bitcamp",
    "Best Advanced Quantum Track Hack - Bitcamp"
])

ALUMNI_HACKS = set([
    "MOST LIT HACK",
    "Prettiest Hack",
    "Hack That Made You Smile"
])

BITCAMP_HACKS = set([
    "Best App Dev Track Hack",
    "Best Cybersecurity Track Hack",
    "Best Machine Learning Track Hack",
    "Best Beginner Quantum Track Hack",
    "Best Advanced Quantum Track Hack",
    "Best Bitcamp Hack",
    "Best First-Time Hack",
    "Best Gamification Hack",
    "Best Hardware Hack",
    "Best Moonshot Hack",
    "Best Razzle Dazzle Hack",
    "Best Social Good Hack",
    "Best Sustainability Hack",
    "Best UI/UX Hack",
])

OTHER_HACKS = set([
    "Best Hack Promoting Public Health - Bloomberg",
    "Best Financial Hack - Capital One",
    "Best Digital Forensics Related Hack - Cipher Tech Solutions",
    "Best Use of GenAI in Business - Cloudforce/Microsoft",
    "Best Web Hack Using React - Peraton",
])

EXCLUDED_CHALLENGES = set([
    "People's Choice Hack - Bitcamp",
    "Beginner Quantum Track Hacks - Bitcamp",
])

'Best First-Time Hack', 'Best Advanced Quantum Track Hack', 'Best Hardware Hack', 'Best Razzle Dazzle Hack', 'Best Gamification Hack', 'Best Beginner Quantum Track Hack', 'Best Bitcamp Hack', 'Best Moonshot Hack', 'Best Sustainability Hack', 'Best Social Good Hack', 'Best UI/UX Hack', 'Best Cybersecurity Track Hack', 'Best Machine Learning Track Hack', 'Best App Dev Track Hack', 'MOST LIT HACK', 'Hack That Made You Smile', 'Prettiest Hack', 'Best Digital Forensics Related Hack - Cipher Tech Solutions', 'Best Use of GenAI in Business - Cloudforce/Microsoft', 'Best Hack Promoting Public Health - Bloomberg', 'Best Web Hack Using React - Peraton', 'Best Financial Hack - Capital One'
CHALLENGE_JUDGE_GROUPS = [
    4,  # Best First-Time Hack
    2,  # Best Advanced Quantum Track Hack
    4,  # Best Hardware Hack
    4,  # Best Razzle Dazzle Hack
    4,  # Best Gamification Hack
    2,  # Best Beginner Quantum Track Hack
    4,  # Best Bitcamp Hack
    4,  # Best Moonshot Hack
    4,  # Best Sustainability Hack
    4,  # Best Social Good Hack
    4,  # Best UI/UX Hack
    2,  # Best Cybersecurity Track Hack
    4,  # Best Machine Learning Track Hack
    4,  # Best App Dev Track Hack
    2,  # MOST LIT HACK
    4,  # Hack That Made You Smile
    4,  # Prettiest Hack
    1,  # Best Digital Forensics Related Hack - Cipher Tech Solutions
    2,  # Best Use of GenAI in Business - Cloudforce/Microsoft
    2,  # Best Hack Promoting Public Health - Bloomberg
    3,  # Best Web Hack Using React - Peraton
    2,  # Best Financial Hack - Capital One
]

TABLES = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8',
         'L1', 'L2', 'L5', 'L6', 'L7', 'L8', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'O8', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', "H8"]
random.shuffle(TABLES)

FULL_CHALLENGE_LIST = list(BITCAMP_HACKS) + list(ALUMNI_HACKS) + list(OTHER_HACKS) 

def get_challenge_maps(full_challenge_list):
    challenge_to_id = {}
    id_to_challenge = {}
    for i, challenge in enumerate(full_challenge_list):
        challenge_to_id[challenge] = i
        id_to_challenge[i] = challenge
    return challenge_to_id, id_to_challenge


# Get mapping
CHALLENGE_TO_ID, ID_TO_CHALLENGE = get_challenge_maps(FULL_CHALLENGE_LIST)


def abstract_expo_alg(hc: List[List[int]], cap: List[int], t_max: int):
    # extracting sizes
    M = len(hc)
    N = len(cap)

    # bookkeeping for valid (h, j) pairs
    valid_hj = set()
    for h, req_cat in enumerate(hc):
        for j in req_cat:
            valid_hj.add((h, j))
    hj_to_i_base = dict(
        map(tuple, map(lambda t: t[::-1], list(enumerate(valid_hj)))))

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
        b1 = np.ones(len(valid_hj))

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
        # print("Here..")
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
        # print("Now here..")
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
        if soln is None:  # failure
            a = m+1
        else:  # success
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

def process_challenges_2025(challenges):
    result = []
    MLH_challenges = []
    for challenge in challenges:
        team_challenges = challenge.split(",")
        current_challenges = []
        current_mlh_challenges = []

        for tc in team_challenges:
            tc = tc.strip()
            if tc in MLH_HACKS:
                current_mlh_challenges.append(tc)
        result.append(current_challenges)
        MLH_challenges.append(current_mlh_challenges)

    return result, MLH_challenges

def process_challenges(challenges):
    result = []
    MLH_challenges = []
    for challenge in challenges:
        team_challenges = challenge.split(",")
        current_challenges = []
        current_mlh_challenges = []

        for tc in team_challenges:
            tc = tc.strip()
            if tc in MLH_HACKS:
                current_mlh_challenges.append(tc)
            elif len(tc) > 0 and (tc not in EXCLUDED_CHALLENGES):
                current_challenges.append(tc)
        result.append(current_challenges)
        MLH_challenges.append(current_mlh_challenges)

    return result, MLH_challenges


def process_bitcamp_hacks(track_response, challenges):
    bitcamp_challenges = []
    other_challenges = []
    result = []

    for challenge in challenges:
        if challenge in BITCAMP_HACKS:
            bitcamp_challenges.append(challenge)
        else:
            other_challenges.append(challenge)
    # print(bitcamp_challenges)
    # print(other_challenges)

    if track_response in BITCAMP_TRACK_HACKS:
        max_challenges = min(2, len(bitcamp_challenges))
        result = (random.sample(bitcamp_challenges, max_challenges))
        result.append(track_response)
    else:
        max_challenges = min(3, len(bitcamp_challenges))
        result = (random.sample(bitcamp_challenges, max_challenges))

    result += other_challenges

    return result


def process(csv_file):
    types = defaultdict(lambda: str)
    projects = pd.read_csv(csv_file, keep_default_na=False, dtype=types)

    # Only grab submitted projects
    submitted_projects = projects[projects[DRAFT_COLUMN_NAME] != 'Draft']

    team_names = submitted_projects[TEAM_COLUMN_NAME].tolist()
    links = submitted_projects[LINK_COLUMN_NAME].tolist()
    # in_person = (submitted_projects[IN_PERSON_COLUMN_NAME] == 'Yes').tolist()
    # 2025
    in_person = [True for _ in range(len(team_names))]
    challenge_fields = submitted_projects[CHALLENGES_COLUMN_NAME].tolist()

    # 2025 Form Parse
    bitcamp_prize_1 = submitted_projects[BITCAMP_PRIZE_1].tolist()
    bitcamp_prize_2 = submitted_projects[BITCAMP_PRIZE_2].tolist()
    bitcamp_prize_3 = submitted_projects[BITCAMP_PRIZE_3].tolist()

    alumni_prize_1 = submitted_projects[ALUMNI_PRIZE_1].tolist()
    alumni_prize_2 = submitted_projects[ALUMNI_PRIZE_2].tolist()

    emails = submitted_projects['Team Member 1 Email'].tolist()
    # emails = submitted_projects.iloc[:, 24].tolist()
    emails = [[email] for email in emails]
    # print(submitted_projects.shape[1] - 1)
    # emails = [list(tup) for tup in zip(submitted_projects.iloc[:, 29].tolist(), submitted_projects.iloc[:, 32].tolist(
    # ), submitted_projects.iloc[:, 35].tolist(), submitted_projects.iloc[:, 38].tolist())]
    # emails = ["dn"]
    # Separate MLH and other challenges

    temp_challenges, MLH_challenges = process_challenges_2025(challenge_fields)

    # Get track challenge and limit bitcamp challenges to MAX 3
    # Not needed for 2025
    # track_response = submitted_projects[TRACK_CHALLENGE_COLUMN_NAME].tolist()

    challenges = []
    for i in range(len(temp_challenges)):
        ind_challenges = []
        if bitcamp_prize_1[i]: 
            ind_challenges.append(bitcamp_prize_1[i])
        if bitcamp_prize_2[i]: 
            ind_challenges.append(bitcamp_prize_2[i])
        if bitcamp_prize_3[i]:
            ind_challenges.append(bitcamp_prize_3[i])
        if alumni_prize_1[i]:
            ind_challenges.append(alumni_prize_1[i])
        if alumni_prize_2[i]:
            ind_challenges.append(alumni_prize_2[i])

        ind_challenges += temp_challenges[i]     
        challenges.append(ind_challenges)

    hc = []
    for ind_challenges in challenges:
        ind_hc = []
        for challenge in ind_challenges:
            ind_hc.append(CHALLENGE_TO_ID[challenge])
        hc.append(ind_hc)

    return team_names, links, in_person, challenges, MLH_challenges, hc, emails
    # return team_names, links, in_person, challenges, MLH_challenges, hc


def parse_challenge_name(challenge_name):
    if challenge_name in OTHER_HACKS:
        return challenge_name.split(" - ")
    elif challenge_name in BITCAMP_HACKS:
        return challenge_name, "Bitcamp"
    elif challenge_name in ALUMNI_HACKS:
        return challenge_name, "Alumni"
    elif challenge_name in MLH_HACKS:
        return challenge_name, "MLH"
    
    return challenge_name, "Other"


def expo_output_to_json(t, H, team_names, links, in_person_list, MLH_challenges, emails):
# def expo_output_to_json(t, H, team_names, links, in_person_list, MLH_challenges):
    eastern = pytz.timezone('US/Eastern')

    EXPO_START_TIME = "2024-04-21 12:15:00"
    EXPO_START = eastern.localize(datetime.strptime(
        EXPO_START_TIME, "%Y-%m-%d %H:%M:%S"))

    HACK_TIME = 2
    judgetime_seen = defaultdict(lambda: 1)

    result = []
    table_count = len(TABLES)
    for id, team in enumerate(H):
        team_table = TABLES[id % table_count] if in_person_list[id] else "virtual"
        team_json = {
            "id": uuid.uuid4().hex[:4] + str(id),
            "team_name": team_names[id],
            # "table": TABLES.pop() if in_person_list[id] else "virtual",
            "table": team_table,
            "in_person": in_person_list[id],
            "link": links[id],
            "emails": emails[id]
        }

        challenges = []

        for timeslot in team:
            challenge_id, start_slot = timeslot
            challenge = ID_TO_CHALLENGE[challenge_id]

            start_time = str(
                EXPO_START + timedelta(minutes=HACK_TIME*start_slot))

            challenge_name, company = parse_challenge_name(challenge)

            judge_id = challenge + str(start_slot)
            judge_group = judgetime_seen[judge_id]
            judgetime_seen[judge_id] += 1

            challenge_json = {
                "is_mlh": False,
                "challenge_name": challenge_name,
                "company": company,
                "judge": f"Judge {judge_group}",
                "start_time": start_time,
            }
            challenges.append(challenge_json)

        challenges.sort(key=lambda x: x["start_time"])

        for challenge in MLH_challenges[id]:
            challenge_name, company = parse_challenge_name(challenge)

            challenge_json = {
                "is_mlh": True,
                "challenge_name": challenge_name,
                "company": company,
                "judge": "Judge",
                "start_time": "",
            }
            challenges.append(challenge_json)

        team_json["challenges"] = challenges
        # print(team_json)
        result.append(team_json)

    return result


def main():
    # csv_file = "./projects-2024-teammates.csv"
    csv_file = "./projects-2025-new.csv"
    team_names, links, in_person, challenges, MLH_challenges, hc, emails = process(
    # team_names, links, in_person, challenges, MLH_challenges, hc = process(
        csv_file)

    print(FULL_CHALLENGE_LIST)
    print(len(FULL_CHALLENGE_LIST))
    print(len(CHALLENGE_JUDGE_GROUPS))

    # print(len(cap))
    # print(len(FULL_CHALLENGE_LIST))
    # print(len(CHALLENGE_TO_ID))
    # print(len(ID_TO_CHALLENGE))
    # for challenge_name, id in CHALLENGE_TO_ID.items():
    #     print(f'{challenge_name} - {cap[id]}')

    # print(len(cap))

    # print(hc)

    t =1
    H = [[(1, 53), (4, 11), (6, 40)], [(3, 75), (8, 69), (11, 63), (14, 48), (16, 68)], [(6, 55), (9, 53), (10, 70), (15, 25), (16, 21)], [(1, 57), (3, 61), (6, 35), (15, 11), (16, 68)], [(1, 43), (5, 26), (6, 41), (15, 60), (16, 64)], [(1, 14), (6, 21), (12, 76), (15, 62), (16, 6)], [(1, 32), (6, 13), (12, 6), (15, 80), (16, 62)], [(9, 78), (12, 45)], [(1, 47), (2, 16), (10, 40)], [(1, 61), (3, 9), (12, 74), (14, 62), (15, 47)], [(0, 24), (9, 38), (12, 7), (15, 50), (16, 1)], [(3, 53), (6, 10), (15, 71)], [(3, 22), (6, 76), (11, 69), (14, 27), (15, 20)], [(2, 31), (4, 3), (11, 53), (15, 75), (16, 4)], [(6, 62), (10, 26), (13, 76), (14, 11), (15, 5)], [(0, 35), (5, 70), (9, 4), (15, 31), (16, 82)], [(0, 2), (5, 40), (6, 58), (15, 59), (16, 4)], [(5, 10), (6, 22), (11, 35), (15, 81), (16, 71)], [(0, 79), (6, 20), (11, 78)], [(3, 67), (5, 14), (6, 66)], [(0, 71), (3, 83), (14, 43), (15, 13)], [(6, 29), (11, 71), (15, 4), (16, 65)], [(1, 2), (3, 7), (12, 75)], [(0, 24), (5, 31), (6, 9), (15, 56), (16, 0)], [(1, 49), (3, 80), (12, 25), (14, 3), (16, 55)], [(3, 18), (5, 76), (10, 78), (15, 70), (16, 53)], [(1, 6), (3, 22), (11, 23), (14, 10), (15, 18)], [(1, 12), (5, 35), (11, 51), (15, 30), (16, 76)], [(1, 21), (5, 16), (6, 2), (15, 78), (16, 5)], [(1, 1), (3, 14), (11, 31), (15, 27), (16, 78)], [(0, 71), (3, 50), (9, 38), (15, 68), (16, 43)], [(3, 62), (6, 60), (12, 72), (14, 25), (16, 63)], [(6, 75), (9, 53), (11, 19), (14, 4), (16, 55)], [(3, 74), (6, 73), (12, 63), (15, 11), (16, 10)], [(1, 39), (5, 75), (6, 60), (15, 2), (16, 31)], [(6, 30), (11, 81), (12, 53), (15, 80)], [(3, 25), (5, 63), (10, 64), (15, 17), (16, 8)], [(1, 51), (2, 49), (6, 26), (14, 29), (16, 54)], [(1, 66), (2, 75), (6, 16), (14, 81), (16, 83)], [(1, 3), (6, 0), (12, 5), (15, 53), (16, 23)], [(6, 41)], [(0, 82), (4, 77), (9, 31), (15, 65), (16, 56)], [(6, 49)], [(3, 78), (4, 3), (6, 23), (15, 12), (16, 66)], [(9, 29), (10, 10), (11, 33)], [(3, 64), (6, 61), (11, 24)], [(5, 78), (9, 57), (10, 24), (15, 77), (16, 81)], [(1, 45), (3, 64), (5, 12), (14, 11), (16, 44)], [(3, 58), (5, 13), (11, 60), (15, 78), (16, 18)], [(0, 5), (3, 68), (9, 44), (15, 66), (16, 77)], [(1, 7), (6, 44), (8, 58), (15, 52), (16, 0)], [(1, 72), (11, 73), (13, 28), (14, 12), (15, 57)], [(3, 37), (10, 62), (11, 46)], [(1, 75), (6, 7), (11, 39), (15, 2), (16, 69)], [(3, 83), (9, 76)], [(3, 34), (11, 75), (13, 17), (15, 32), (16, 58)], [(0, 9), (6, 7), (12, 54), (15, 22), (16, 19)], [(3, 79), (6, 49), (12, 83), (14, 42), (16, 28)], [(3, 12), (10, 51), (12, 59)], [(1, 71), (9, 74), (11, 56), (15, 50), (16, 29)], [(3, 11), (9, 21), (11, 67), (15, 15), (16, 13)], [(3, 52), (9, 42), (10, 14), (15, 35), (16, 57)], [(6, 30), (8, 70), (9, 13), (15, 44), (16, 23)], [(3, 35), (5, 41), (11, 77), (14, 68)], [(1, 38), (10, 25), (13, 55), (15, 6), (16, 45)], [(1, 33), (6, 24), (9, 29), (15, 69), (16, 35)], [(3, 76), (6, 4), (13, 47), (14, 18), (16, 10)], [(1, 36), (11, 64), (12, 73), (15, 40), (16, 78)], [(3, 31), (10, 57), (11, 76)], [(3, 23), (5, 33), (9, 64), (15, 73)], [(0, 19), (3, 17), (9, 70), (15, 49), (16, 56)], [(3, 6), (5, 27), (6, 12), (15, 34), (16, 41)], [(11, 29), (13, 83)], [(3, 42), (6, 51), (13, 45), (14, 50), (16, 47)], [(1, 13), (3, 51), (11, 54), (15, 36), (16, 42)], [(0, 47), (3, 76), (11, 34), (14, 1), (15, 10)], [(1, 68), (4, 23), (6, 66), (15, 46), (16, 27)], [(3, 45), (9, 48), (12, 67), (14, 21), (16, 51)], [(1, 59), (11, 40), (15, 39)], [(3, 73), (9, 15), (11, 45), (16, 11)], [(1, 50), (5, 38), (11, 59), (14, 26), (16, 14)], [(6, 37), (10, 71), (15, 36), (16, 65)], [(3, 38), (5, 65), (11, 79), (15, 26), (16, 77)], [(1, 65), (5, 11), (6, 54), (16, 33)], [(0, 8), (1, 29), (6, 12), (15, 19), (16, 21)], [(5, 83), (6, 32), (9, 48), (14, 41), (16, 54)], [(3, 20), (10, 61), (13, 6), (14, 76), (15, 67)], [(0, 37), (1, 44), (5, 54), (14, 53), (16, 26)], [(1, 28), (2, 48), (6, 69)], [(0, 21), (6, 27), (11, 16), (15, 10), (16, 13)], [(0, 67), (6, 29), (9, 25), (15, 70), (16, 44)], [(3, 38), (5, 5), (6, 19), (15, 56)], [(0, 6), (5, 3), (9, 31), (15, 1), (16, 50)], [(3, 29), (6, 57), (9, 18), (14, 80), (16, 38)], [(1, 0), (6, 46), (12, 17), (15, 4), (16, 51)], [(1, 62), (2, 16), (11, 30), (15, 57), (16, 60)], [(1, 80), (2, 76), (3, 43), (14, 1), (16, 22)], [(1, 58), (3, 59), (10, 67), (16, 7)], [(3, 32), (10, 39), (12, 54), (15, 43), (16, 80)], [(0, 74), (6, 83), (9, 39), (15, 42), (16, 46)], [(9, 45), (10, 20), (12, 16), (15, 77), (16, 60)], [(3, 18), (9, 80), (10, 67)], [(8, 9), (10, 28), (13, 40)], [(4, 47), (9, 13), (11, 37), (15, 1), (16, 48)], [(3, 69), (11, 61), (14, 82), (15, 54)], [(1, 37), (6, 5), (10, 35), (14, 44), (16, 43)], [(3, 68), (9, 46), (10, 22), (14, 34), (15, 33)], [(6, 53), (9, 23), (11, 62), (15, 41), (16, 50)], [(1, 27), (3, 51), (6, 64)], [(0, 56), (5, 37), (11, 17), (14, 6), (16, 29)], [(3, 23), (8, 5), (11, 41), (14, 70), (16, 73)], [(1, 8), (6, 25), (11, 65), (14, 28), (16, 39)], [(3, 12), (5, 20), (11, 57)], [(3, 56), (10, 31), (12, 74), (14, 7), (16, 61)], [(1, 48), (5, 74), (14, 40), (15, 30)], [(3, 2), (11, 20), (12, 38), (15, 0), (16, 49)], [(6, 4), (11, 12)], [(6, 77)], [(6, 68), (9, 81), (10, 33), (15, 63), (16, 52)], [(9, 17), (11, 82), (12, 41), (15, 40), (16, 11)], [(1, 18), (6, 83), (11, 0), (15, 5), (16, 16)], [(3, 8), (10, 0), (11, 26), (15, 64), (16, 37)], [(1, 73), (6, 68), (11, 52), (14, 26), (15, 16)], [(1, 60), (6, 34), (8, 40), (14, 24), (16, 38)], [(1, 4), (6, 69), (13, 83), (15, 37), (16, 15)], [(1, 63), (3, 52), (11, 6), (15, 26), (16, 72)], [(1, 30), (6, 9), (13, 53), (14, 52), (16, 41)], [(0, 37), (3, 66), (10, 74), (14, 57), (16, 71)], [(1, 24), (2, 7), (5, 77), (14, 13), (15, 60)], [(6, 14), (8, 6), (14, 7), (16, 5)], [(3, 58), (6, 35), (11, 36), (15, 12), (16, 1)], [(1, 54), (5, 32), (6, 34), (16, 24)], [(3, 46), (6, 16), (11, 9), (15, 58), (16, 67)], [(3, 66), (10, 82), (14, 76), (16, 36)], [(1, 34), (9, 19), (11, 25), (15, 23)], [(1, 55), (6, 72), (10, 43), (14, 75), (16, 83)], [(1, 56), (3, 14), (8, 53), (15, 59), (16, 74)], [(1, 76), (3, 21), (6, 2), (14, 38)], [(0, 46), (3, 31), (11, 70), (16, 40)], [(6, 48), (11, 42), (15, 25)], [(3, 42), (6, 72), (11, 32), (15, 31), (16, 64)], [(4, 69), (10, 31), (11, 49), (15, 28)], [(9, 4), (10, 23), (12, 70), (14, 58)], [(3, 9), (6, 78), (11, 83), (15, 27), (16, 33)], [(3, 45), (8, 3), (13, 15)], [(0, 21), (9, 5), (10, 13)], [(3, 59), (11, 66), (15, 42)], [(3, 65), (6, 47), (11, 15), (14, 63), (16, 9)], [(3, 62), (10, 17), (12, 80), (15, 7)], [(3, 17), (6, 53), (9, 36), (15, 22), (16, 49)], [(1, 67), (6, 32), (11, 47), (14, 28), (16, 20)], [(1, 74), (6, 46), (9, 1)], [(0, 50), (3, 70), (9, 1), (15, 44), (16, 62)], [(6, 51), (16, 15)], [(1, 78), (5, 55), (10, 64), (15, 9), (16, 18)], [(1, 23), (3, 80), (11, 1), (15, 38), (16, 72)], [(3, 54), (9, 67), (12, 39), (15, 73), (16, 59)], [(11, 68), (15, 82)], [(1, 10), (6, 23), (13, 39), (14, 20), (16, 19)], [(3, 25), (6, 24), (9, 9), (16, 37)], [(0, 11), (1, 20), (3, 54), (15, 19), (16, 53)], [(1, 26), (10, 25), (12, 17)], [(2, 48), (6, 47), (11, 11)], [(3, 39), (9, 63), (11, 5), (15, 15), (16, 73)], [(6, 67), (9, 43), (11, 74), (15, 29), (16, 75)], [(1, 77), (3, 6), (12, 73)], [(11, 38)], [(2, 14), (6, 26), (9, 41)], [(1, 64), (5, 8), (6, 62), (15, 51), (16, 66)], [(1, 79), (5, 52), (10, 68), (14, 47), (16, 17)], [(3, 36), (9, 30), (10, 71), (15, 48), (16, 47)], [(6, 44), (11, 14), (12, 57), (14, 51), (16, 67)], [(3, 77), (10, 15), (12, 62), (15, 18), (16, 40)], [(1, 40), (3, 53), (5, 62), (15, 48), (16, 63)], [(1, 46), (3, 11), (6, 15), (14, 14), (15, 75)], [(0, 55), (9, 25), (11, 7), (15, 21), (16, 14)], [(6, 76), (11, 13)], [(3, 32), (10, 15), (12, 26), (15, 24), (16, 2)], [(3, 28), (6, 42), (11, 22), (15, 81), (16, 31)], [(1, 52), (5, 66), (6, 17), (15, 69), (16, 12)], [(0, 59), (1, 42), (2, 61), (15, 16), (16, 58)], [(2, 37), (6, 77), (14, 66), (15, 51)], [(6, 0), (9, 37), (12, 36), (15, 45), (16, 61)], [(3, 65), (9, 28), (11, 3), (15, 76), (16, 74)], [(6, 37), (9, 45), (11, 2), (15, 6), (16, 70)], [(6, 61), (9, 39), (11, 58), (15, 34), (16, 32)], [(3, 44), (6, 54), (11, 10), (15, 24), (16, 81)], [(3, 72), (9, 33), (10, 27), (15, 68), (16, 8)], [(1, 69), (3, 73), (10, 49), (15, 28)], [(1, 17), (11, 43), (12, 28), (15, 83), (16, 45)], [(1, 31), (2, 27), (12, 47), (14, 73), (16, 26)], [(3, 30), (6, 50)], [(9, 30), (10, 75), (11, 80), (15, 55), (16, 79)], [(0, 3), (9, 40), (10, 2), (15, 35), (16, 32)], [(0, 81), (3, 19), (12, 46), (16, 34)], [(5, 25), (6, 75), (9, 77), (15, 3), (16, 28)], [(3, 34), (10, 22), (12, 45), (14, 44), (16, 59)], [(9, 27), (11, 55)], [(3, 60), (9, 82), (11, 44), (15, 61), (16, 17)], [(3, 61), (5, 29), (10, 21), (14, 16), (16, 27)], [(1, 41), (10, 35), (11, 18)], [(1, 15), (3, 2), (11, 4)], [(4, 66)], [(6, 3), (9, 14), (10, 53), (15, 67), (16, 57)], [(5, 72), (9, 9), (10, 14), (15, 7), (16, 76)], [(1, 5)], [(0, 14), (6, 40), (11, 50), (15, 61), (16, 79)], [(0, 48), (9, 7), (12, 36), (15, 66), (16, 75)], [(3, 10), (10, 3), (12, 62), (14, 49), (15, 64)], [(3, 44), (5, 49), (11, 21), (14, 14), (16, 25)], [(1, 70), (5, 57)], [(0, 68), (9, 46), (11, 27), (15, 76), (16, 52)], [(0, 44), (9, 14), (11, 28), (14, 50), (16, 69)], [(0, 33), (9, 43), (11, 48), (15, 46), (16, 12)], [(6, 33), (9, 20), (12, 68), (14, 64), (16, 46)], [(1, 16), (9, 28), (10, 57)], [(1, 11), (3, 7), (12, 72), (16, 39)], [(5, 17), (9, 67), (10, 55), (14, 10), (15, 9)], [(1, 22), (3, 1), (6, 18), (14, 47), (15, 62)], [(1, 82), (3, 35), (6, 55), (15, 83), (16, 7)], [(13, 51)], [(1, 19), (5, 39), (6, 57), (15, 8), (16, 34)], [(5, 68), (6, 5), (9, 79), (15, 33), (16, 42)], [(0, 23), (6, 14), (9, 35), (15, 53), (16, 25)], [(0, 22), (1, 9), (3, 39), (15, 74), (16, 6)], [(0, 38), (3, 60), (6, 13), (15, 17), (16, 35)], [(1, 35), (6, 25), (12, 60), (14, 46), (15, 32)], [(8, 42), (9, 21), (13, 34), (14, 56), (15, 65)], [(1, 83), (6, 19), (10, 69), (15, 71), (16, 48)], [(6, 36), (9, 8), (11, 72), (15, 37), (16, 70)], [(6, 17), (10, 2), (11, 8), (15, 20)], [(6, 15), (12, 24), (14, 2)]]

    # t, H, J = abstract_expo_alg(hc, CHALLENGE_JUDGE_GROUPS, 125)

    print(t)
    print(150 // t)
    # print(H)

    expo_output = expo_output_to_json(
        t, H, team_names, links, in_person, MLH_challenges, emails)

    output_path = '../frontend/public/expo_algorithm_results.json'

    with open(output_path, 'w') as f:
        json.dump(expo_output, f, indent=4)

    print(f"Output written to {output_path}")


if __name__ == "__main__":
    main()
