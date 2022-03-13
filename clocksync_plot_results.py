# Plot clocksync results
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('clocksync_summary.csv')

string_columns = [
    "filename",
    "phone_name",
]

# Some stats on each field
print ("Min/max per field:")
for key in df.keys():
    if key not in string_columns:
        print(" ", key, " \tmin:", df[key].min(), " \tmax:", df[key].max())

# Pull out relevant part of filename
df['shortname'] = df['filename'].str.extract(r'session_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_(.*)\.json', expand=False).str.strip()
# df.drop(string_columns, axis=1, inplace=True) # Don't plot these in the bar chart

# Horizontal bar plot with index being shortened filename
df = df.set_index("shortname")
ax = df.plot.barh()

# Optionally zoom in a bit b/c there may be serious outliers
ax.set_xlim(-2000,30000)

plt.show()
