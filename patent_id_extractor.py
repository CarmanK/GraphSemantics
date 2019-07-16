# Make shift HashMap
ids = []
for i in range(10000000):
    ids.append(-1)

with open('./input_data/cit-Patents.txt', 'r') as input_file:
    lines = input_file.readlines()

# Write the unique patent IDs to a file
with open('./input_data/patent_ids.txt', 'w') as output_file:
    for i in range(4, len(lines)):
        from_to_id = lines[i].split('\t')
        id1 = int(from_to_id[0])
        id2 = int(from_to_id[1][:-1])
        if ids[id1] == -1:
            ids[id1] = id1
            output_file.write(str(id1) + '\n')
        if ids[id2] == -1:
            ids[id2] = id2
            output_file.write(str(id2) + '\n')