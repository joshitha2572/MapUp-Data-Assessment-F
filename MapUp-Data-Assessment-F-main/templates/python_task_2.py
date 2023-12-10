import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    df_merged = df.merge(df[['id_1', 'id_2', 'distance']], how='inner', on=['id_1', 'id_2'])
    distance_matrix = df_merged.groupby(['id_1', 'id_2'])['distance'].mean()
    distance_matrix = distance_matrix.unstack()

    return distance_matrix


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    unrolled_df = df.stack().reset_index()
    unrolled_df.columns = ['id_start', 'id_end', 'distance']

    return unrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold = reference_avg_distance * 0.1
    filtered_df = df[(df['id_start'] != reference_id) &
                   (df['distance'].abs() <= (reference_avg_distance + threshold))]

    return filtered_df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    toll_rates = {'moto': 0.1, 'car': 0.2, 'rv': 0.3, 'bus': 0.4, 'truck': 0.5}
    df['toll'] = df['distance'] * df['car'].map(toll_rates)

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    time_intervals = {
    (6, 9): 1.2,
    (16, 19): 1.1,
    }

    df['hour'] = pd.to_datetime(df['startTime']).dt.hour
    for start_hour, multiplier in time_intervals.items():
        df.loc[(df['hour'] >= start_hour[0]) & (df['hour'] < start_hour[1]), 'toll'] *= multiplier

    return df
