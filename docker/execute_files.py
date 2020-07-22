def execute_files(f):
    from subprocess import PIPE, CalledProcessError, check_call, Popen, TimeoutExpired

    # rerun f without using 'source'
    p3 = Popen(['/opt/conda/envs/r_4.0.1/bin/Rscript', f], \
        stdout=PIPE, stderr=PIPE)
    res = ""

    try:
        stdout, stderr = p3.communicate(timeout=3600)
        if p3.returncode != 0:
            res = stderr.splitlines()[-5:-1]
            res = b' '.join(res)
            res_str = res.decode("utf-8") if type(res) is bytes else res
            import re
            ret =re.findall(r'(?:Error).*', res_str)
        else:
            ret = "success"
    except TimeoutExpired:
        p3.kill()
        stdout, stderr = p3.communicate()
        ret = "time limit exceeded"
    
    return ret