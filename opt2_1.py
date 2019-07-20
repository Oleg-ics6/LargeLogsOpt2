import re
import sys
import os
import bisect


reg = r'\/[a-z]+'
amount = 0
succ = 0
time_arr = []
time_av = 0
req_arr = []
req_av = 0
resp_arr = []
resp_av = 0


for fname in os.listdir():
    if re.match(r'log\d+', fname):
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
time: {round(time_av)}, {time_arr[round(succ * 0.95) - 1]}, {time_arr[round(succ * 0.99) - 1]} µs
req_size: {round(req_av)}, {req_arr[round(succ * 0.95) - 1]}, {req_arr[round(succ * 0.99) - 1]} byte
resp_size: {round(resp_av)}, {resp_arr[round(succ * 0.95) - 1]}, {resp_arr[round(succ * 0.99) - 1]} byte
----------------------\n
"""
                    sys.stdout.writelines(str1)
        amount = 0
        succ = 0
        time_arr = []
        time_av = 0
        req_arr = []
        req_av = 0
        resp_arr = []
        resp_av = 0
