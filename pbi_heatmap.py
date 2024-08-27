import os, uuid, matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot
import pandas

import sys
sys.tracebacklimit = 0

os.chdir(r'C:\Users\lizal\Documents\LAB Tech\LT Consult\Par Excellence\Par 360\repo-pbi')
dataset = pandas.read_csv('input_df.csv')

matplotlib.pyplot.figure(figsize=(5.55555555555556,4.16666666666667), dpi=72)
matplotlib.pyplot.show = lambda args=None,kw=None: matplotlib.pyplot.savefig(str(uuid.uuid1()))
# Original Script. Please update your script content here and once completed copy below section back to the original editing window #
# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset = pandas.DataFrame(Year, Quarter, Month, Day, Scan Times Daily Average per Location and Individual)
# dataset = dataset.drop_duplicates()

# Paste or type your script code here:

# CODE
import matplotlib.pyplot as plt
import calendar
import numpy as np
from matplotlib.colors import ListedColormap

# CLEANING DATA

# Map month names to numbers and create the 'Date' column
month_mapping = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}

dataset['Month_Num'] = dataset['Month'].map(month_mapping)

# Convert Year, Month_Num, and Day to strings and pad day and month
dataset['Year'] = dataset['Year'].astype(str)
dataset['Month_Num'] = dataset['Month_Num'].astype(str).str.zfill(2)
dataset['Day'] = dataset['Day'].astype(str).str.zfill(2)

# Concatenate to form a 'YYYY-MM-DD' format and convert to datetime
dataset['Date'] = pandas.to_datetime(dataset['Year'] + '-' + dataset['Month_Num'] + '-' + dataset['Day'])

# Drop unnecessary columns to avoid any further issues
dataset = dataset.drop(columns=['Month', 'Month_Num'])


# PLOT

# Define a custom colormap: white for no data, green for 0, red for 1 and above
colors = ['white', 'green', 'red']
cmap = ListedColormap(colors)

# Group by year and month
grouped = dataset.groupby([dataset['Date'].dt.year, dataset['Date'].dt.month])

# Get unique combinations of year and month
year_month_combinations = grouped.size().index.tolist()  # This gives a list of (year, month) tuples

# Calculate the number of rows and columns
ncols = int(np.ceil(np.sqrt(len(year_month_combinations))))
nrows = int(np.ceil(len(year_month_combinations) / ncols))

# Set up the plotting area with multiple columns
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8 * ncols, 2.5 * nrows))

# Ensure axes is a 2D array for consistent indexing
axes = np.atleast_2d(axes)

# Loop through each year and month combination
for ax, (year, month) in zip(axes.flat, year_month_combinations):
    # Get the first weekday and the number of days in the month
    month_cal = calendar.monthcalendar(year, month)
    
    # Initialize calendar grid with -1 for no data (white)
    cal_data = np.full_like(month_cal, -1, dtype=int)
    
    # Update the grid with data
    for i, week in enumerate(month_cal):
        for j, day in enumerate(week):
            if day != 0:
                day_value = dataset[(dataset['Date'].dt.year == year) & (dataset['Date'].dt.month == month) & (dataset['Date'].dt.day == day)]['Scan Times Daily Average per Location and Individual'].sum()
                if day_value == 0:
                    cal_data[i, j] = 0  # Green for 0
                elif day_value > 0:
                    cal_data[i, j] = 1  # Red for 1 and above
    
    # Plot the grid with custom colormap
    ax.imshow(cal_data, cmap=cmap, aspect='auto', interpolation='none', vmin=-1, vmax=1)
    
    # Set the labels for the days of the week
    ax.set_xticks(np.arange(7))
    ax.set_xticklabels(['S', 'M', 'T', 'W', 'T', 'F', 'S'], fontsize=12)
    ax.xaxis.set_ticks_position('top')  # Move the x-ticks to the top
    ax.xaxis.set_label_position('top')  # Set the label position to the top
    ax.set_facecolor('white')  # Set the background color to white
    
    # Plot day numbers
    for i, week in enumerate(month_cal):
        for j, day in enumerate(week):
            if day != 0:
                ax.text(j, i, str(day), ha='center', va='center', color='black')
    
    # Set the title for each month
    ax.set_title(f'{calendar.month_name[month]} {year}', fontsize=16, pad=20)  # Add padding to move title down
    
    # Calculate and set week numbers on the y-axis
    week_numbers = []
    for week in month_cal:
        first_day = next((day for day in week if day != 0), None)
        if first_day:
            week_number = pandas.Timestamp(year=year, month=month, day=first_day).isocalendar()[1]
            week_numbers.append(week_number)

    ax.set_yticks(np.arange(len(week_numbers)))
    ax.set_yticklabels([f'W{k}' for k in week_numbers], fontsize=12)

    # Remove tick markers
    ax.tick_params(left=False, top=False, bottom=False, right=False)
    
    # Hide the grid lines and the frame of the axis
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

# Turn off any unused subplots
for ax in axes.flat[len(year_month_combinations):]:
    ax.axis('off')

# Adjust layout to avoid overlap
plt.subplots_adjust(hspace=0.5, wspace=0.3)  # Increase space between subplots
plt.tight_layout()
plt.show()