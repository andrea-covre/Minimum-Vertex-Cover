
import os
import json

algo = "LS2"
graph_name = "power" # star2
intrest_data = "quality"

times = []

for filename in os.listdir("stats"):
    if f"{graph_name}_{algo}_1000_" in filename:
        print(filename)
        with open(os.path.join("stats", filename), "r") as f:
            data = json.load(f)
            times.append(data[intrest_data][-1])

print("")

for i in times:
    print(i)