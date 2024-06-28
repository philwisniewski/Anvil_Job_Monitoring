#!/bin/sh

# Retrieves a list of users which have been stealing time >:(

# File to write outputs from sacct to
history_file_name="history.csv"

# Minimum time users must have used to be considered
time_threshold=60

# Threshold for percentage wasted time
percent_threshold=0.5

# Remove csv file if it exists
rm -f $history_file_name

# Number of months of data to retrieve
number_of_months=1

# Get dates for sacct
today=$(date +%F)
one_month_ago=$(date -d "-$number_of_months month" +%F)

# Run sacct and put data in history_file_name
sacct -a -X -S $one_month_ago -E $today --parsable2 -o State,JobID,Account,TimelimitRaw,ElapsedRaw > $history_file_name

# Make sure python is loaded
# idk if cron jobs are different
module load anaconda

python job_cop.py $history_file_name $time_threshold $percent_threshold
