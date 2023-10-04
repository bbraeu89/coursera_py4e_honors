import urllib.request, urllib.parse, urllib.error
import json
import ssl
import gzip
from io import BytesIO
from urllib.parse import quote
import sqlite3



# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('protein.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Protein_info')

cur.execute('''CREATE TABLE IF NOT EXISTS Protein_info
    (id INTEGER PRIMARY KEY, uniprot_id VARCHAR(20), organism_name VARCHAR(100),
     lineage VARCHAR(100), protein_sequence TEXT, sequence_length INT, lineage_average_length FLOAT)''')

user_input = input("Enter your query: ")
encoded_query = quote(user_input)
url = f'https://rest.uniprot.org/uniprotkb/stream?compressed=true&format=json&query=({encoded_query})'
print('Retrieving', url)


uh = urllib.request.urlopen(url, context=ctx)
data = uh.read()

# Decompress the gzipped data
buffer = BytesIO(data)
with gzip.GzipFile(fileobj=buffer) as f:
    decompressed_data = f.read().decode('utf-8')

print('Retrieved', len(decompressed_data), 'characters')
data = json.loads(decompressed_data)

lengths_by_lineage = {}
for item in data["results"]:
    try:
        lng = item["organism"]["lineage"][1]
        sequence_length = len(item["sequence"]["value"])

        # If the lineage is not in the dictionary, add an empty list
        if lng not in lengths_by_lineage:
            lengths_by_lineage[lng] = []

        lengths_by_lineage[lng].append(sequence_length)
    except IndexError:
        continue

# Calculate the average lengths by lineage
averages_by_lineage = {}
for lineage, lengths in lengths_by_lineage.items():
    total_entries = len(lengths)
    average_length = sum(lengths) / total_entries
    averages_by_lineage[lineage] = average_length

    print(f"Total number of entries for {lineage}: {total_entries}")
    print(f"Average sequence length for {lineage}: {average_length:.2f}\n")

if "results" in data:
    for item in data["results"]:
            try:
                uniprot_id = (item["primaryAccession"])
                organism_name = (item["organism"]["scientificName"])
                lineage = (item["organism"]["lineage"][1])
                protein_sequence = (item["sequence"]["value"])
                sequence_length = (len(item["sequence"]["value"]))
                lineage_average_length = averages_by_lineage.get(lineage, 0) 
                cur.execute('''INSERT INTO Protein_info (uniprot_id, organism_name, lineage, protein_sequence, sequence_length, lineage_average_length)
                            VALUES (?,?,?,?,?,?)''', (uniprot_id, organism_name, lineage, protein_sequence, sequence_length, lineage_average_length))
                            
                            
            except (KeyError, IndexError) as e:
                # Handle specific errors or just continue
                continue

conn.commit()



