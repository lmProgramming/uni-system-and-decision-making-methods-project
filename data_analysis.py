from imports import *


def correlation_matrix(df: pd.DataFrame) -> None:
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.corr(), annot=True, cmap='viridis', fmt='.2f')
    plt.show()


def correlation_column(df: pd.DataFrame, column: str) -> None:
    plt.figure(figsize=(12, 8))
    corr: DataFrame = df.corr()[[column]].drop(column)
    sns.heatmap(corr, annot=True, cmap='viridis', fmt='.2f')
    plt.show()


def detect_outliers(df: pd.DataFrame, column_name: str) -> pd.Series:
    mean: float = df[column_name].mean()
    std: float = df[column_name].std()
    threshold: float = 3 * std
    return (df[column_name] < (mean - threshold)) | (df[column_name] > (mean + threshold))


def remove_outliers(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    outliers = detect_outliers(df, column_name)
    return df[~outliers]
