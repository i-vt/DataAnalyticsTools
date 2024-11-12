import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

def plot_histogram(file_path):
    # Read dates from the file
    with open(file_path, 'r') as file:
        dates = file.readlines()
    dates = [date.strip() for date in dates]  # Clean up newlines

    # Convert string dates to datetime objects for accurate sorting and manipulation
    dates = [datetime.strptime(date, '%Y%m%d') for date in dates]

    # Count the occurrences of each date
    date_counts = Counter(dates)

    # Sort dates for plotting; sorted by the datetime objects ensures chronological order
    sorted_dates = sorted(date_counts.items())
    dates, counts = zip(*sorted_dates)  # Unpack the sorted dates and their counts

    # Convert datetime objects back to strings for display, if needed
    dates = [date.strftime('%Y-%m-%d') for date in dates]

    # Create histogram
    plt.figure(figsize=(14, 6))
    plt.bar(dates, counts, color='blue')
    plt.xlabel('Date')
    plt.ylabel('Number of Modifications')
    plt.title('Histogram of File Modifications by Date')
    plt.xticks(rotation=45)  # Rotate dates for better visibility
    plt.tight_layout()  # Adjust layout to make room for label rotation
    plt.show()

plot_histogram('mod_dates.txt')
