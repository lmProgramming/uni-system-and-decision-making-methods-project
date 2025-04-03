from imports import *


def clean_csv_files() -> None:
    for file in [file for file in os.listdir("data") if file.startswith("Attempt")]:
        file_path: str = f"data/{file}"
        with open(file_path, "r") as f:
            lines: list[str] = f.readlines()
        if lines[0].strip().endswith(";"):
            print(f"Fixing file {file_path}")
            lines[0] = lines[0].strip()[:-1] + "\n"
        with open(file_path, "w") as f:
            f.writelines(lines)


def clean_dataframes(initial_parameters: DataFrame, results: DataFrame) -> tuple[DataFrame, DataFrame]:
    initial_parameters = initial_parameters.drop(
        columns=[
            "hungerMult", "speedMult", "mitosisSpeedMult", "newCellCreationCostMult",
            "initialSize", "fullyRandomiseStartingGenes", "allCreaturesStartAsDesignedCreature",
            "startAsACreature", "colorfulCells", "speedGeneOn", "sensorGeneOn",
            "processingGeneOn", "gluttonyGeneOn", "reproductionGeneOn", "storageGeneOn",
            "parentEmpathyGeneOn", "aggresivnessGeneOn", "healthGeneOn", "foodPreferenceGeneOn",
            "fightingPermitted"
        ]
    ).dropna()

    results = results.drop(
        columns=["simulation time", "food preference gene"]
    ).loc[:, ~results.columns.str.contains('^Unnamed')]

    return initial_parameters, results
