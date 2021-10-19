import time

filePath = 'access.log'

f = open(filePath, 'r')

last_position = None
while True:
    lines = f.readlines()
    w = open('access.log.2', 'w')
    w.writelines(lines)
    w.close()
    print (f.tell())
    time.sleep(10)

w.close()
f.close()

# last_pos = f.tell()
# print (last_pos)
# line = f.readline()
# last_pos = f.tell()
# print (last_pos)
# f.seek(last_pos)
# print(f.readline())