import pandas as pd
import numpy as np


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    df_traffic = pd.read_csv("datasets/dataset-1.csv")

    car_matrix = df_traffic.pivot_table(values="car", index="id_1", columns="id_2")

    return car_matrix

    


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df_traffic = pd.read_csv("datasets/dataset-1.csv")
    type_count = df_traffic["car"].value_counts().to_dict()

    return type_count


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    df_traffic = pd.read_csv("datasets/dataset-1.csv")
    df_mean = df_traffic["bus"].mean()
    bus_indexes = df_traffic[(df_traffic["bus"] > 2 * df_mean)].index.tolist()

    return bus_indexes



def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    df_traffic = pd.read_csv("datasets/dataset-1.csv")
    df_average_truck = df_traffic.groupby("route")["truck"].mean()
    filtered_routes = df_average_truck[df_average_truck > 7].index.tolist()

    return filtered_routes


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    conditions = [
        (matrix["id_1"] == matrix["id_2"]),
        (matrix["car"] > matrix["truck"]),
    ]
    values = [2, 0.5]
    matrix["car"] = np.where(np.select(conditions, values), matrix["car"], matrix["car"])

    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df1 = pd.read_csv("datasets/dataset-1.csv")
    df2 = pd.read_csv("datasets/dataset-2.csv")
    merged_df = df1.merge(
        df2[["id", "id_2", "startDay", "endDay"]], on="id_2"
    )

    days_covered = merged_df.groupby(["id_1", "id_2"])["startDay"].diff().max() + 1
    seven_day_coverage = days_covered >= 7

    merged_df["time_diff"] = pd.to_timedelta(merged_df["endTime"] - merged_df["startTime"])
    hours_covered = merged_df.groupby(["id_1", "id_2", "startDay"])["time_diff"].sum() / timedelta(hours=1)
    twentyfour_hour_coverage = (hours_covered >= 24).all()

    completeness_check = seven_day_coverage & twentyfour_hour_coverage

    return completeness_check

