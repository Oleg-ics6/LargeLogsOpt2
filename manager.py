import os
import re
from multiprocessing import Process


def run_shell(*names):
    str1 = "xfce4-terminal -e 'python opt2_1.py " + " ".join(names) + "' -H"
    os.system(str1)


if __name__ == '__main__':
    fnames = [i for i in os.listdir() if re.match(r'log\d+', i)]
    num = 0
    procs = []
    for i in range(4):
        proc = Process(target=run_shell, args=(fnames[num:num + 25]))
        procs.append(proc)
        proc.start()
        num += 25
    for proc in procs:
        proc.join()
