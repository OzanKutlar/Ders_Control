import pandas as pd
import re
import sys


def main():
    if len(sys.argv) != 3:
        print("Wrong arguments.")
        print("Usage : py add.py {ClassCode} {ClassDataFile}")
        return

    fileToAdd = 'eklenenders.csv'

    originalDersler = pd.read_csv(fileToAdd, encoding='utf-8-sig')

    fileToUse = sys.argv[2]

    newDersler = pd.read_csv(fileToUse, encoding='utf-8-sig')

    foundRow = newDersler[newDersler['Section'] == sys.argv[1]]

    if foundRow.empty:
        print("No Such Class exists.")
        sys.exit()

    # Append the found row to the original DataFrame
    originalDersler = pd.concat([originalDersler, foundRow], ignore_index=True)

    originalDersler.to_csv(fileToAdd, index=False, encoding='utf-8-sig')

    print(f"Class with code {sys.argv[2]} has been successfully added.")


if __name__ == "__main__":
    main()
