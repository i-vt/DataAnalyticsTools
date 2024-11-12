import matplotlib.pyplot as plt

def plot_histogram(file_path):
    # Read days from the file
    with open(file_path, 'r') as file:
        days = file.readlines()
    days = [day.strip() for day in days]  # Clean up newlines

    # Count the occurrences of each day
    day_counts = {}
    for day in days:
        if day in day_counts:
            day_counts[day] += 1
        else:
            day_counts[day] = 1

    # Data for plotting
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    counts = [day_counts.get(day, 0) for day in days_of_week]

    # Create histogram
    plt.figure(figsize=(10, 6))
    plt.bar(days_of_week, counts, color='blue')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Modifications')
    plt.title('Histogram of File Modifications by Day of the Week')
    plt.show()

plot_histogram('mod_days.txt')
