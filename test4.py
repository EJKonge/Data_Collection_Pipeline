import os
path = 'raw_data/images'
os.chdir(path)
for i in os.listdir():
    print(i)