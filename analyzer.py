from reader import parse_csv_files

def analyze_simulation_results(simulation_results):
    print("Started analyzing...")
    
    for result in simulation_results:
        print(result)
    
    print("Ended analyzing.")
    
if __name__ == "__main__":
    simulation_results = parse_csv_files()
    
    analyze_simulation_results(simulation_results)