import sys, os

for line in sys.stdin:

    cmd = "echo -ne \"%s\" | ba/hadoop_main.py" % line

    os.system(cmd)
