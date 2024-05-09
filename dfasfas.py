import os
import pandas as pd

files = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('.csv') and f.startswith("I")]

for f in files:
    df = pd.read_csv(f, delimiter=';', header=0)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)
        
    print("\n\n")
