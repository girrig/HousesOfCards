from main import Player
import json
import pickle

obj = Player("frank", "1", [0, 2, 1, 0], 7, [])
list = [1, 2, 34, 54, 5, 48]
dict = {"key": "value", "tuber": 3}

with open("testsave.json", "w") as f:
    json.dump([obj.__dict__, obj.__dict__], f)
f.close()

with open("testsave.json", "r") as f:
    jsondata = json.load(f)
    print(jsondata)
f.close()

with open('testpickle.dat', 'wb') as f:
    pickle.dump([obj, list, dict], f)

with open('testpickle.dat', 'rb') as f:
    newplayer, newlist, newdict = pickle.load(f)

print(newplayer)
print(newlist)
print(newdict)
