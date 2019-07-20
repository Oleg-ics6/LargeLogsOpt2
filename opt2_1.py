import re
import sys
import os
import numpy as np


def replace(arr, num):
    if num > arr[0] and num < arr[1]:
        arr[0] = num
    elif num > arr[1] and num < arr[2]:
        arr[0], arr[1] = arr[1], num
    elif num > arr[2] and num < arr[3]:
        arr[0], arr[1] = arr[1], arr[2]
        arr[2] = num
    elif num > arr[3] and num < arr[4]:
        arr[0], arr[1] = arr[1], arr[2]
        arr[2], arr[3] = arr[3], num
    elif num > arr[4]:
        arr[0], arr[1] = arr[1], arr[2]
        arr[2], arr[3] = arr[3], arr[4]
        arr[4] = num


reg = r'\/[a-z]+'
amount = 0
succ = 0
time_arr = np.zeros(5)
time_av = 0
req_arr = np.zeros(5)
req_av = 0
resp_arr = np.zeros(5)
resp_av = 0

for fname in os.listdir():
    if re.match(r'log\d+', fname):
        with open(fname, 'r') as fp:
            for line in fp:
                arr = line.split(' ')
                amount += 1
                if arr[2] < '300':
                    if int(arr[5]) > time_arr[0]:
                        replace(time_arr, int(arr[5]))
                    if int(arr[3]) > req_arr[0]:
                        replace(req_arr, int(arr[3]))
                    if int(arr[4]) > resp_arr[0]:
                        replace(resp_arr, int(arr[4]))
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
time: {round(time_av)} µs
req_size: {round(req_av)}, {req_arr[0]}, {req_arr[4]} byte
resp_size: {round(resp_av)}, {resp_arr[0]}, {resp_arr[4]} byte
----------------------\n
"""
                    sys.stdout.writelines(str1)
