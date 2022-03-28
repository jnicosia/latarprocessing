import json

filename = "session_2022-03-28_01-22-18.json"

print(f"INFO: Processing file '{filename}'...")

f = open(filename, 'r')

# returns JSON object as a dictionary
data = json.load(f)

# Close file
f.close()

# Pull static metadata
# phone_name = data["mobile"]["name"]

# # Iterating through the json
# objectives = data["objectives"]
# procedure_objectives = data["procedure"]["objectives"]

# Pull data and plot
latencies = []
deltaTs = []
for trip in data["clockSync"]["mobile"]["roundTrips"]:
    localSend = trip["localSend"]
    localRecv = trip["localRecv"]
    remote = trip["remote"]

    trip_latency = localRecv - localSend
    deltaT = localSend + (trip_latency / 2) - remote
    
    latencies.append(trip_latency)
    deltaTs.append(deltaT)


import matplotlib.pyplot as plt
# import numpy as np
 
#data
# x = np.random.randint(0, 50, 50)
# y = np.random.randint(0, 50, 50)
 
#scatter plot
plt.scatter(list(range(len(latencies))), latencies)
plt.scatter(list(range(len(deltaTs))), deltaTs)
 
plt.show()
# breakpoint()
