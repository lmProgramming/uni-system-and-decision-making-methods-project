from reader import parse_csv_files, SimulationResults
from typing import List
import matplotlib.pyplot as plt
import re
from sklearn.linear_model import LinearRegression
import numpy as np
from text_aux import convert_str_to_capitalized_words
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


def analyze_simulation_results(simulation_results: List[SimulationResults]):
    print("Started analyzing...")

    while True:
        initial_parameter_name = input("Enter the name of the initial parameter you want to analyze (or 'exit' to exit): ")
        if initial_parameter_name == 'exit':
            break        
        
        train_data_coef = 0.8
        train_data_amount = int(len(simulation_results) * train_data_coef)
        test_data_amount = len(simulation_results) - train_data_amount
        
        initial_parameters = [result.initial_parameters.iloc[0] for result in simulation_results]
        initial_parameter_selected = [init[initial_parameter_name] for init in initial_parameters]
        result_name = input("Enter the name of the result you want to analyze: ")
        results = [result.get_last_history()[result_name] for result in simulation_results]
        
        reg = LinearRegression().fit(initial_parameters[:train_data_amount], results[:train_data_amount])
        print(reg.coef_)
        print(reg.score(initial_parameters, results))
        
        for i in zip(initial_parameters[train_data_amount:], results[train_data_amount:]):
            print(f'Predicted: {reg.predict([i[0]])}, Real: {i[1]}')
        
        plt.scatter(initial_parameter_selected, results)
        plt.xlabel(convert_str_to_capitalized_words(initial_parameter_name))
        plt.ylabel(convert_str_to_capitalized_words(result_name))
        plt.title(f'{convert_str_to_capitalized_words(initial_parameter_name)} vs {convert_str_to_capitalized_words(result_name)}')
        plt.show()
    print("Ended analyzing.")
    
if __name__ == "__main__":
    simulation_results = parse_csv_files()
    
    analyze_simulation_results(simulation_results)