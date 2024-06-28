import sys
import pandas as pd
import numpy as np

if __name__=="__main__":
    try:
        print(sys.argv)
        # File name to read from
        file_name = sys.argv[1]
        # Minimum time in minutes
        time_threshold = int(sys.argv[2])
        # Percentage wasted walltime to reach out at
        percent_threshold = float(sys.argv[3])
    except:
        print("Error: Must include filename and threshold value")
        sys.exit(-1)

    df = pd.read_csv(file_name, delimiter="|")
    df = df[df['State'] == 'COMPLETED']
    df['ElapsedMins'] = df['ElapsedRaw'].replace('UNLIMITED', 60*24*60).astype('int32') / 60
    df['TimelimitMins'] = df['TimelimitRaw'].replace('UNLIMITED', 60*24*60).astype('int32') / 60
    df['WastedWallTime'] = df['TimelimitMins'] - df['ElapsedMins']

    result = df.groupby('Account').agg(
        n_jobs=('TimelimitMins', 'count'),
        average_requested_walltime=('TimelimitMins', 'mean'),
        average_used_walltime=('ElapsedMins', 'mean'),
        average_wasted_walltime=('WastedWallTime', 'mean'),
        total_requested_walltime=('TimelimitMins', 'sum'),
        total_used_walltime=('ElapsedMins', 'sum'),
        total_wasted_walltime=('WastedWallTime', 'sum')
    ).reset_index()

    result['percent_wasted_walltime'] = result['total_wasted_walltime'] / result['total_requested_walltime']

    job_thieves = result[(result['percent_wasted_walltime'] > percent_threshold) & (result['total_requested_walltime'] > time_threshold)]

    print(job_thieves[['Account', 'percent_wasted_walltime', 'total_wasted_walltime', 'total_requested_walltime', 'n_jobs']])

    sys.exit(0)
