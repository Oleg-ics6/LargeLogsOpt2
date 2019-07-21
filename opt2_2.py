import gzip
import shutil
import os
import re
from multiprocessing import Process


def gzipper(*fnames):
    for fname in fnames:
        with open(fname, 'rb') as f_in:
                with gzip.open(fname + '.gz', 'wb', 5) as f_out:
                    shutil.copyfileobj(f_in, f_out, 20_000_000)


fnames = [i for i in os.listdir() if re.match(r'log\d+', i)]
count = 0
procs = []


for i in range(4):
    proc = Process(target=gzipper, args=(fnames[count:count + 25]))
    procs.append(proc)
    proc.start()
    count += 25


for proc in procs:
    proc.join()