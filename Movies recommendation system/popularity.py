import sqlite3
import numpy as np

with sqlite3.connect('moviesdb2.sqlite') as conn:
    cur = conn.cursor()
temp = cur.execute('''
            SELECT * FROM Movies''')
def cmp(a):
    return a[-1]
temp = sorted(temp, key=cmp, reverse=True)
temp = [value[1] for value in temp]
print("MOST POPULAR MOVIES ARE:-")

for i in range(10):
    print(temp[i])