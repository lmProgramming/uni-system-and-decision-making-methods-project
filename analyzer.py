from reader import parse_csv_files, SimulationResults
from typing import List
import matplotlib.pyplot as plt
import re
'''
mapSize;startingCreatures;timeToSpawnAFood;
hungerMult;speedMult;mitosisSpeedMult;mutationRange;bodyPartMutationChance;
intervalBetweenBirths;hungerMultFromAge;newCellCreationCostMult;aggresivnesMult;
genesCostMult;bodyPartsCostMult;initialSize;;
'''
'''
simulation time;speed gene;sensor gene;processing gene;gluttony gene;
reproduction wilness gene;energy storage capacity gene;parental empathy gene;
aggresivness gene;health gene;food preference gene;creatures count;
average creature cost;average amount of body parts;average amount of protective spikes
average amount of composters;average amount of turbines;average amount of offensive spikes;
'''

def add_space_before_capital_letters(s: str) -> str:
    for i in s:
        if i.isupper():
            s = s.replace(i, " " + i)
    return s

def convert_str_to_capitalized_words(s: str) -> str:
    return ' '.join([word.capitalize() for word in add_space_before_capital_letters(s).split(' ')])

def analyze_simulation_results(simulation_results: List[SimulationResults]):
    print("Started analyzing...")

    while True:
        initial_parameter_name = input("Enter the name of the initial parameter you want to analyze (or 'exit' to exit): ")
        
        if initial_parameter_name == 'exit':
            break
        
        initial_parameters = [result.initial_parameters.iloc[0][initial_parameter_name] for result in simulation_results]
        result_name = input("Enter the name of the result you want to analyze: ")
        results = [result.history.iloc[-1][result_name] for result in simulation_results]
        
        plt.scatter(initial_parameters, results)
        plt.xlabel(convert_str_to_capitalized_words(initial_parameter_name))
        plt.ylabel(convert_str_to_capitalized_words(result_name))
        plt.title(f'{convert_str_to_capitalized_words(initial_parameter_name)} vs {convert_str_to_capitalized_words(result_name)}')
        plt.show()
    print("Ended analyzing.")
    
if __name__ == "__main__":
    simulation_results = parse_csv_files()
    
    analyze_simulation_results(simulation_results)