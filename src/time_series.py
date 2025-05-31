from typing import List
import pandas as pd
import numpy as np

def get_time_series(transactions: List[dict], token_transfers: List[dict],
                    own_address: str):
    df = pd.DataFrame(transactions + token_transfers)
    df = df[df['from'] == own_address]
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    hour_counts = df['hour'].value_counts().sort_index()

    # Ensure all 24 hours are represented (fill 0 where no data)
    full_hour_counts = pd.Series([hour_counts.get(i, 0) for i in range(24)],
                                 index=range(24))
    # Convert to numpy for rolling sum
    counts_array = np.array(full_hour_counts.tolist())
    # Duplicate the array to handle wrap-around for circular window
    counts_double = np.concatenate([counts_array,
                                    counts_array[:7]])  # 24 + 7 = 31 elements
    # Find 8-hour rolling sum and get the start index of the minimum sum
    window_sums = np.convolve(counts_double, np.ones(8, dtype=int),
                              'valid')[:24]
    min_start_hour = np.argmin(window_sums)
    if min_start_hour < 12:
        timezone = "UTC-" + str(min_start_hour)
    else:
        timezone = "UTC+" + str(24 - min_start_hour)
    return {
        "timezone": timezone,
        "counts": full_hour_counts.to_list(),
    }
