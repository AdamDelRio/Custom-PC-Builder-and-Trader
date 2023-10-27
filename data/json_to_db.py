import json
from sys import argv

def main():
    if len(argv) == 1:
        filename = input("filename: ")
    else:
        filename = argv[1]

    path = f"./data/json/{filename}"
    with open(path, "r") as f:
        data = json.load(f)

    schema = [key for key in data[0].keys()]

    ### INSERT to inventory table return ID and put inventory id in insert table
    


if __name__ == "__main__":
    main()