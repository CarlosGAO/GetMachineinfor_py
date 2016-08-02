#!/usr/bin/python
import sys
def lines(file):
    for line in file:
        yield line
    yield '\n'
def user(file):
    users= []
    for data in lines(file):
        if data.strip():
            data = data.strip()
            users.append(tuple(data.split()))
        elif users:
            return users

if __name__ == '__main__':
    for a,b in user(sys.stdin):
        print a,b
