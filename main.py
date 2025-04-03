from pandas.core.frame import DataFrame
from imports import *
from data_cleaning import clean_csv_files, clean_dataframes
from data_analysis import correlation_matrix, remove_outliers
from model_training import regress, compare_models

# Step 1: Clean CSV files
clean_csv_files()

# Step 2: Parse data
simulation_results: List[SimulationResults] = parse_csvs()
initial_parameters: DataFrame = DataFrame(
    [result.parameters.iloc[0] for result in simulation_results])
results: DataFrame = DataFrame([result.get_last_history()
                                for result in simulation_results])

# Step 3: Clean dataframes
initial_parameters, results = clean_dataframes(initial_parameters, results)

# Step 4: Analyze data
correlation_matrix(initial_parameters)
correlation_matrix(results)

# Step 5: Remove outliers
ANALYZED = "average creature cost"
df_1: DataFrame = initial_parameters.copy()
df_1[ANALYZED] = results[ANALYZED]
df_1 = remove_outliers(df_1, ANALYZED)

# Step 6: Train and compare models
X: DataFrame = df_1.drop(columns=[ANALYZED])
y = df_1[ANALYZED]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
regress(X_scaled, y)
models = [LinearRegression(), Lasso(), RandomForestRegressor(),
          GradientBoostingRegressor()]
results = compare_models(X_scaled, y, models)
print(results)
