#!/usr/bin/python

from os import environ
from time import strftime, localtime, sleep

f = file(environ["TMP"] + "/access.txt", "w")
while True:
    f.write(strftime("%Y-%m-%dT%H:%M:%S\n", localtime()))
    f.flush()
    sleep(30)
