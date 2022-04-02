import json
import matplotlib.pyplot as plt

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
 
#scatter plot
fig = plt.figure()
plt.scatter(list(range(len(latencies))), latencies)
plt.scatter(list(range(len(deltaTs))), deltaTs)

plt.legend(["round-trip latency" , "deltaT"])
plt.xlabel("sample number")
plt.ylabel("ms")

# plt.show()
fig = plt.figure()

plt.scatter(latencies, deltaTs)
plt.xlabel("latency")
plt.ylabel("deltaT")
plt.show()
