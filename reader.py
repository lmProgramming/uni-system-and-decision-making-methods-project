from dataclasses import dataclass
import os
from typing import List, Optional
import pandas as pd
import re
from datetime import datetime

DATA_FOLDER = "data\\"

ENDED_PREMATURELY = "Ended prematurely - over 200 creatures"

@dataclass(frozen=True)
class SimulationResults:
    index: int
    date: datetime
    initial_parameters: pd.DataFrame
    history: pd.DataFrame
    
    @property
    def ended_prematurely(self) -> bool:
        return self.history.iloc[-1]["simulation time"] == ENDED_PREMATURELY
    
    def get_last_history(self) -> pd.Series:
        row: pd.Series = self.history.iloc[-1]
        if self.ended_prematurely:
            return self.history.iloc[-2]
        return row
    
    def __str__(self) -> str:
        return f"Result {self.index} - {self.date.strftime('%d.%m.%Y %H-%M-%S')}, rows count: {self.history.shape[0]}"

def parse_csv_files(data_path = Optional(str), limit_of_logs: int=None) -> List[SimulationResults]:
    if data_path is None:
        data_path = os.path.join(os.getcwd(), DATA_FOLDER)
        
    print("Started parsing...")
    
    files: List[str] = [file for file in os.listdir(data_path) if file.endswith('.csv')]
    
    initial_settings: List[str] = [file for file in files if file.startswith('Initial settings')]
    
    simulation_results: List[SimulationResults] = []
    
    error_count = 0
    
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
            
            simulation_results.append(SimulationResults(index, date, initial_settings_df, attempt_df))
        except IndexError:
            error_count += 1
            print(f"Index error while parsing file {initial_settings_filename}")
        except Exception as e:
            error_count += 1
            print(f"Error parsing file {initial_settings_filename}: {e}")
            
        if limit_of_logs is not None and len(simulation_results) >= limit_of_logs:
            break
        
    print(f"Ended parsing. Parsed files: {len(simulation_results)}, errors: {error_count}")
            
    simulation_results.sort(key=lambda x: x.index)
    
    return simulation_results


if __name__ == "__main__":    
    data_path: str = os.path.join(os.getcwd(), DATA_FOLDER)
    
    results: List[SimulationResults] = parse_csv_files(data_path)   

    for result in results:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            print(result.initial_parameters)
            print(result.history)
            input("Press Enter to continue...")
