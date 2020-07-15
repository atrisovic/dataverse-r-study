import glob

file_list = glob.glob("*.R")
file_list.extend(glob.glob('*.r'))

print(file_list)

from subprocess import PIPE, CalledProcessError, check_call, Popen, TimeoutExpired

error_col = []

for f in file_list:

    # R 4.0
    p3 = Popen(['/opt/conda/envs/r_4.0.1/bin/Rscript', f], \
        stdout=PIPE, stderr=PIPE)

    res40 = ""

    try:
        stdout, stderr = p3.communicate(timeout=600)
        if p3.returncode != 0:
            res40 = stderr.splitlines()[-1]
        else:
            res40 = "success"
    except TimeoutExpired:
        p3.kill()
        stdout, stderr = p3.communicate()
        res40 = "time limit exceeded"

    # R 3.6
    p2 = Popen(['/opt/conda/envs/r_3.6.0/bin/Rscript', f], \
        stdout=PIPE, stderr=PIPE)

    res36 = ""

    try:
        stdout, stderr = p2.communicate(timeout=600)
        if p2.returncode != 0:
            res36 = stderr.splitlines()[-1]
        else:
            res36 = "success"
    except TimeoutExpired:
        p2.kill()
        res36 = "time limit exceeded"
        stdout, stderr = p2.communicate()

    # R 3.2
    p = Popen(['ln -s /lib/x86_64-linux-gnu/libreadline.so.7.0 /lib/x86_64-linux-gnu/libreadline.so.6;/opt/conda/envs/r_3.2.1/bin/Rscript', f], \
        stdout=PIPE, stderr=PIPE)

    res32 = ""

    try:
        stdout, stderr = p.communicate(timeout=600)
        if p.returncode != 0:
            res32 = stderr.splitlines()[-1]
        else:
            res32 = "success"
    except TimeoutExpired:
        p.kill()
        res32 = "time limit exceeded"
        stdout, stderr = p.communicate()


    with open('run_log.csv','a') as fw:
        fw.write("{},{},{},{}\n".format(f, \
            res32.decode("utf-8") if type(res32) is bytes else res32, \
                res36.decode("utf-8") if type(res36) is bytes else res36, \
                    res40.decode("utf-8") if type(res40) is bytes else res40))

