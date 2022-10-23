import pandas as pd
import re

sheet = pd.read_csv("enterprise-attack-v11.3.csv", 
                    header=0, 
                    usecols=["description", "tactics"])

sheet = sheet.to_numpy()

with open("filtered.csv", "w") as file:
    file.write("description,tactics\n")
    for row in sheet:
        tokens = re.findall("(\(Citation:.*\))|(\(https://.*\))|(</code>)|(<code>)", row[0])
        description = row[0] 
        description = description.replace("\n", " ")
        for token in tokens:
            for t in token:
                if t != "":
                    description = description.replace(t, "")
        tactics = row[1]
        file.write(f"\"{description}\",{tactics}\n")