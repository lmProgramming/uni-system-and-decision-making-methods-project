from dataclasses import dataclass
import os
from typing import List, Optional
import pandas as pd
import re
from datetime import datetime

def calculate_health_body_cost(health_gene):
    return health_gene * 20

def calculate_body_part_cost(data):
    return (data["average amount of offensive spikes"] + data["average amount of composters"]) * 6 + data["average amount of turbines"] * 8 + data["average amount of protective spikes"] * 3

def calculate_average_cost(initials, data):
    energyRequiredFromGenes = (data["sensor gene"] + data["speed gene"] + data["energy storage capacity gene"] + data["health gene"] + data["aggresivness gene"] * 2) * 8 * initials["genesCostMult"]
    energyRequiredFromBody = 15 + calculate_health_body_cost(data["health gene"]) + calculate_body_part_cost(data) * initials["bodyPartsCostMult"]

    return energyRequiredFromGenes + energyRequiredFromBody

def fix(data: pd.DataFrame, initials: pd.DataFrame):
    for i in range(data.shape[0]):
        data.loc[data.index[i], 'average creature cost'] = calculate_average_cost(initials, data.iloc[i]).squeeze()
    return data
    
def parse_csvs() -> None:
    data_path = 'data'
    print("Started parsing...")
    
    files: List[str] = [file for file in os.listdir(data_path) if file.endswith('.csv')]
        
    initial_settings: List[str] = [file for file in files if file.startswith('Initial settings')]
    
    error_count = 0
    skipped_count = 0
    
    for initial_settings_filename in initial_settings:
        try:
            m: re.Match[str] | None = re.fullmatch(r'Initial settings (?P<index>\d+) - (?P<date>\d\d.\d\d.\d\d\d\d \d\d-\d\d-\d\d).csv', initial_settings_filename)
            
            if m is None:
                raise ValueError(f"Filename {initial_settings_filename} does not match the expected pattern")
            
            index = int(m.group('index'))
            date: datetime = datetime.strptime(m.group('date'), "%d.%m.%Y %H-%M-%S")
            
            initial_settings_df: pd.DataFrame = pd.read_csv(os.path.join(data_path, initial_settings_filename), delimiter=';', header=0, decimal=",")
            
            attempt_filename: str = f"Attempt {index} - {date.strftime('%d.%m.%Y %H-%M-%S')}.csv"
            attempt_df: pd.DataFrame = pd.read_csv(os.path.join(data_path, attempt_filename), delimiter=';', header=0, decimal=",")
            attempt_df['creatures count'] = attempt_df['creatures count'].astype(int)
            
            attempt_df = fix(attempt_df, initial_settings_df)
            print(attempt_df["average creature cost"])
            print(attempt_filename)
            attempt_df.to_csv(f"data/{attempt_filename}", index=False, sep=';', decimal=',')
            
        except IndexError:
            error_count += 1
            print(f"Index error while parsing file {initial_settings_filename}")
        except Exception as e:
            error_count += 1
            print(f"Error parsing file {initial_settings_filename}: {e}")

# Save the modified data back to the same CSV file
#data.to_csv('data/Attempt 0 - 09.05.2024 09-41-59.csv', index=False)
parse_csvs()