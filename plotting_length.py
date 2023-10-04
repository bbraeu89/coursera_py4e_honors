import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Connect to the SQLite database
conn = sqlite3.connect('protein.sqlite')

# Extract data from the database using pandas
df = pd.read_sql_query("SELECT sequence_length, lineage FROM Protein_info", conn)

# Close the connection
conn.close()

# Get unique lineages
lineages = df['lineage'].unique()

# Assign a unique color to each lineage using the 'tab20' colormap
colors = plt.cm.tab20(np.linspace(0, 1, len(lineages)))
color_map = {lineage: color for lineage, color in zip(lineages, colors)}

# Plot each entry's sequence length colored by its lineage
for lineage, color in color_map.items():
    lineage_data = df[df['lineage'] == lineage]
    plt.hist(lineage_data['sequence_length'], bins=50, alpha=0.6, label=lineage, color=color)

plt.xlabel('Length')
plt.ylabel('Frequency')
plt.title('Histogram of Sequence Length Colored by Lineage')
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()