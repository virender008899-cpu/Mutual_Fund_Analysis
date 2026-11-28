import os

for root, folders, files in os.walk("data"):
    for file in files:
        if file.endswith(".csv"):
            print(os.path.join(root, file))