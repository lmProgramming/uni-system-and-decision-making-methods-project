from dataclasses import dataclass
import os
from typing import List
import pandas as pd
import re
from datetime import datetime

DATA_FOLDER = "data\\"

@dataclass(frozen=True)
class SimulationResults:
    index: int
    date: datetime
    initial_parameters: pd.DataFrame
    results: pd.DataFrame
    
    def __str__(self) -> str:
        print(f"Result {self.index} - {self.date.strftime('%d.%m.%Y %H-%M-%S')}, rows count: {self.results.shape[0]}")

data_path: str = os.path.join(os.getcwd(), DATA_FOLDER)

def parse_csv_files(data_path) -> List[SimulationResults]:
    print("Started parsing...")
    
    files = [file for file in os.listdir(data_path) if file.endswith('.csv')]
    
    initial_settings = [file for file in files if file.startswith('Initial settings')]
    
    simulation_results: List[SimulationResults] = []
    
    error_count = 0
    
    for initial_settings_filename in initial_settings:
        try:
            m = re.fullmatch(r'Initial settings (?P<index>\d+) - (?P<date>\d\d.\d\d.\d\d\d\d \d\d-\d\d-\d\d).csv', initial_settings_filename)
            
            index = int(m.group('index'))
            date: datetime = datetime.strptime(m.group('date'), "%d.%m.%Y %H-%M-%S")
            
            initial_settings_df: pd.DataFrame = pd.read_csv(os.path.join(data_path, initial_settings_filename), delimiter=';', header=0)
            
            attempt_filename: str = f"Attempt {index} - {date.strftime('%d.%m.%Y %H-%M-%S')}.csv"
            attempt_df: pd.DataFrame = pd.read_csv(os.path.join(data_path, attempt_filename), delimiter=';', header=0)
            
            simulation_results.append(SimulationResults(index, date, initial_settings_df, attempt_df))
        except IndexError:
            error_count += 1
            print(f"Index error while parsing file {initial_settings_filename}")
        except Exception as e:
            error_count += 1
            print(f"Error parsing file {initial_settings_filename}: {e}")
        
    print(f"Ended parsing. Parsed files: {len(simulation_results)}, errors: {error_count}")
            
    return simulation_results


if __name__ == "__main__":
    results: List[SimulationResults] = parse_csv_files(data_path)   

    for result in results:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            print(result.initial_parameters)
            print(result.results)
            input("Press Enter to continue...")
