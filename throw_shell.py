#!/usr/bin/env python

import subprocess
import os


def throw_shell(cmd):
    print('Running...\n + {cmd} + \n'.format(cmd=cmd))
    tmp = subprocess.Popen(cmd, cwd=os.getcwd(),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           shell=True,
                           universal_newlines=True)
    stdout, stderr = tmp.communicate()
    return stdout, stderr


if __name__ == "__main__":
    print(throwshell("echo 'Hello World'")[0])
