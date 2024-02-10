import os 
path = '../api/1122'
for dirs in os.listdir(path):
    print("current dir: ", dirs)
    if '.json' not in dirs:
        for file in os.listdir(f"{path}/{dirs}/history"):
            if 'statistics' not in file:
                print("removing: ", f"{path}/{dirs}/history/{file}")
                os.remove(f"{path}/{dirs}/history/{file}")