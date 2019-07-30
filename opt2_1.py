import re
import sys
import bisect


reg = r'\/[a-z]+'
amount = 0
succ = 0
curr_succ = 0
time_arr = []
time_av = 0
req_arr = []
req_av = 0
resp_arr = []
resp_av = 0


for fname in sys.argv[1:]:
    print(fname)
    with open(fname, 'r') as fp:
        for line in fp:
            arr = line.split(' ')
            amount += 1
            if arr[2] < '300':
                bisect.insort(time_arr, int(arr[5]))
                bisect.insort(req_arr, int(arr[3]))
                bisect.insort(resp_arr, int(arr[4]))
                succ += 1
                curr_succ += 1
                if succ == 1:
                    time_av = int(arr[5])
                    req_av = int(arr[3])
                    resp_av = int(arr[4])
                else:
                    time_av = time_av * (succ - 1) / succ + int(arr[5]) / succ
                    req_av = req_av * (succ - 1) / succ + int(arr[3]) / succ
                    resp_av = resp_av * (succ - 1) / succ + int(arr[4]) / succ
                str1 = f"""\
{re.match(reg, arr[-1]).group(0)}
OK: {succ}/{amount} {round(succ / amount * 100, 1)}%
time: {round(time_av)}, {time_arr[round(curr_succ - 0.05 * succ - 1)]}, {time_arr[round(curr_succ - 0.01 * succ - 1)]} µs
req_size: {round(req_av)}, {req_arr[round(curr_succ - 0.05 * succ - 1)]}, {req_arr[round(curr_succ - 0.01 * succ - 1)]} byte
resp_size: {round(resp_av)}, {resp_arr[round(curr_succ - 0.05 * succ - 1)]}, {resp_arr[round(curr_succ - 0.01 * succ - 1)]} byte
----------------------\n
"""
            if amount == 10_000:
                fper = round(len(time_arr) * 0.95)
                del time_arr[0:fper]
                del req_arr[0:fper]
                del resp_arr[0:fper]
                curr_succ -= fper
            elif amount % 10_000 == 0:
                fper = round((curr_succ / succ - 0.05) * succ)
                del time_arr[0:fper]
                del req_arr[0:fper]
                del resp_arr[0:fper]
                curr_succ -= fper
                sys.stdout.writelines(str1)
    amount = 0
    succ = 0
    time_arr = []
    time_av = 0
    req_arr = []
    req_av = 0
    resp_arr = []
    resp_av = 0
    curr_succ = 0
