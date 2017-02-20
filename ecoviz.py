#!/usr/bin/env python3

import os
import sys
import time
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn

help_message = """\n
---------------------------------------ABOUT---------------------------------------
Program that lets user see statistics over expenses and income for either one
single month or for all time since the beginning of user expense tracking.

---------------------------------------USAGE---------------------------------------
Run the script with command line arguments in either of the following formats:
1) > python add_expense.py
2) > python add_expense.py now
3) > python add_expense.py <MM/YYYY>
4) > python add_expense.py --help

--> 1) Displays statistics for all time since the beginning of usage.
--> 2) Displays statistics for current month
--> 3) Displays statistics for the specific month MM/YYYY
--> 4) Displays this help message\n"""

def get_single_month_dataframe(text_path):
	"""Function that takes a file path to a economy text data file,
	reads it, extracts data and returns it in a pandas DataFrame."""
	economy_data = dict()	# To store economy_data for dataframe below

	with open(text_path, "r") as txt_file:
		economy_dates = list()				# To store dates for expense/income
		economy_types = list()				# To store type of expense/income
		economy_amounts = list()			# To store amount for one expense/income

		for line_num, line in enumerate(txt_file):
			if (line_num >= 2):
				splitted_line = line.split()						# List of "words"
				economy_dates.append(splitted_line[0])				# Append exp/inc date
				economy_types.append(splitted_line[2])				# Append exp/inc type
				economy_amounts.append(float(splitted_line[4]))		# Append exp/inc amount

	for etype in economy_types:
		economy_data[etype] = [eamount if economy_types[i] == etype else 0 \
			for i, eamount in enumerate(economy_amounts)]				# Fill dictionary

	return pd.DataFrame(economy_data, index = economy_dates)	# Dataframe with one month data


def get_single_month_economy_data(economy_type, month, year):
	"""Function that takes an economy type (either 'Expense' or 'Income')
	as well as a string month and year in order to extract data from the
	file corresponding to the particular month and year. Data is returned
	in a DataFrame through as call to get_single_month_dataframe()."""
	source_dir = os.path.dirname(os.path.abspath(__file__))	# Directory of this script
	economy_dir = os.path.join(source_dir, economy_type)	# Set to either 'expense' or 'income'
	year_dir = os.path.join(economy_dir, year)				# Relevant year for reuqested file

	for filename in os.listdir(year_dir):
		if (filename.startswith(month)):
			text_filename = filename 						# Identify relevant filename

	text_path = os.path.join(year_dir, text_filename)		# Path to requested file
	return get_single_month_dataframe(text_path)


def get_multi_month_economy_data(economy_type):
	"""Function that takes an economy type (either 'expense' or 'income')
	and collects data from text files for all existing years and months.
	Then combines all this data in one massive DataFrame and returns it."""
	source_dir = os.path.dirname(os.path.abspath(__file__))	# Directory of this script
	economy_dir = os.path.join(source_dir, economy_type)	# Set to either 'expense' or 'income'
	monthly_frames = list()		# To store list of dataframes each with monthly data

	for curr_year in os.listdir(economy_dir):				# Loop through all years
		year_dir = os.path.join(economy_dir, curr_year)

		if (os.path.isdir(year_dir)):						# If curr_year is a directory
			for monthly_file in os.listdir(year_dir):		# For all files in curr_year directory
				if (monthly_file.endswith(".txt")):								# If file is a text file
					text_path = os.path.join(year_dir, monthly_file)			# Path to text file
					monthly_frames.append(get_single_month_dataframe(text_path))

	combined_frames = pd.concat(monthly_frames)			# Concatenate all dataframes into one massive
	combined_frames[pd.isnull(combined_frames)] = 0.0 	# Change all generated NaN values to 0.0
	
	return combined_frames

def fill_missing_dates(data):
	"""Function that takes in a dataframe and converts the index from string
	to contain datelike-objects. Then fills in missing dates between the entries
	in the index and return back the updated dataframe."""
	data = data.groupby(data.index, sort = False).sum()		# Combine/sum data for same dates
	reformatted_index = list()

	for date in data.index:
		reformatted_date = date[-4:] + "-" + date[3:5]+ "-" + date[0:2]		# New date format
		reformatted_index.append(reformatted_date)							# Store date in new format

	data.index = pd.DatetimeIndex(reformatted_index)							# Make index of dates
	date_interval = pd.date_range(reformatted_index[0], reformatted_index[-1])	# Generate date range
	data = data.reindex(date_interval, fill_value = 0.0)		# Fill in missing dates
	return data

def compute_and_viz_fft(data, economy_type):
	"""Computes and plots the Fast Fourier Transofrm of the input data."""
	N = len(data.index)								# Number of sample points
	delta_t = 1.0 									# Number of days between data points
	frequency = np.fft.fftfreq(N, delta_t)			# Array of corresponding frequencies
	fftransform = np.fft.fft(np.array(data)) / N 	# Fast Fourier Transorm of data
	plt.plot(frequency[1:int(N/2)], abs(fftransform[1:int(N/2)]))

def generate_single_month_bar_stats(exp_data, inc_data, date):
	"""Function that generates a bar plot of the different types of expense
	and income for the particular month the data is relevant for."""
	exp_data = fill_missing_dates(exp_data).sum(0)					# Fill missing dates and sum column wise
	inc_data = fill_missing_dates(inc_data).sum(0)					# Fill missing dates and sum column wise
	table_data = pd.concat([exp_data, inc_data], axis = 1).sum(1)	# Concatenate expense and income data
	table_data[pd.isnull(table_data)] = 0.0 						# Replace all possible NaN values with 0.0

	is_income = np.zeros(len(table_data.index))						# To track which elements in inc_data.index is in table_data.index

	# Find out which elements in inc_data.index is in table_data.index
	# and store results in a True/False array where indices correspond.
	for i in range(len(inc_data.index)):
		if (inc_data.index[i] in table_data.index):
			is_income[list(table_data.index).index(inc_data.index[i])] = True

		else:
			is_income[i] = False

	is_income = pd.DataFrame(is_income, columns = ["is_income"], index = table_data.index)	# Make dataframe to concatenate
	table_data = pd.concat([table_data, is_income], axis = 1)								# make is_income a column in table_data
	table_data.columns = ["Expense/Income", "is_income"]									# Name columns

	plt.subplot(1, 2, 1)
	plt.style.use("ggplot")
	table_data["Expense/Income"].plot(kind = "bar", color = table_data.is_income.map(\
		{True: seaborn.xkcd_rgb["periwinkle"], False: seaborn.xkcd_rgb["coral"]}))		# Plot bar with color depending on if is_income == True
	plt.axhline(0, color = "k")

	plt.title("Expense (red) and income (purple) for {}.\nTotal expense: {:.2f}, Total income: {:.2f}, Net gain: {:.2f}".format(\
		date, sum(exp_data), sum(inc_data), sum(inc_data) - sum(exp_data)), fontsize = 12)	


def generate_pie_chart(data, economy_type, date, multi_mode = False, plot_loc = 1):
	"""Function that produces a pie chart over the input dataframe. Subplot calls are
	split up since thi function is used both for multi-month and single month stats."""
	if (multi_mode == True):			# Subplot layout depends on multi mode
		plt.subplot(1, 3, 3)			# Covers 3 rows and 1 column at location 2

	else:
		plt.subplot(1, 2, plot_loc)		# Covers 3 rows and 1 column at location plot_loc

	data = data.sum(0)		# Sum column-wise to get total expense for each category
	data.name = ""			# To supress sidewyas name ("None") for pie chart
	autopct = lambda frac: "{:.2f},- ({:.1f}%)".format((frac * sum(data)) / 100.0, frac)
	explode = [3 / data[i]**(1/2) for i in range(len(data))]	# Some array for exploding pie

	plt.style.use("seaborn-deep")
	data.plot.pie(title = "Pie chart of {} for {}".format(\
		economy_type, date, economy_type, sum(data)), autopct = autopct, fontsize = 8, \
		explode = explode, shadow = True)
	plt.axis("equal")

def visualize_economy_over_time(exp_data, inc_data):
	"""Function that takes in expense and income dataframes for all time and does various
	analysis as well as visualizing the data in table, graph, bar and pie chart forms."""
	exp_data = fill_missing_dates(exp_data).sum(1)	# Fill missing dates and sum rowwise to combine categories for each date
	inc_data = fill_missing_dates(inc_data).sum(1)	# Fill missing dates and sum rowwise to combine categories for each date

	plt.style.use("ggplot")
	plt.subplot(3, 3, 2)	# Subplot for daily expense graph
	exp_data.plot(label = "Daily expense", legend = True, sharex = True)
	plt.title("Graphs starting since {}".format(str(exp_data.index[0])[:10]), fontsize = 15)

	weekly_exp_data = exp_data.resample("W").sum()
	plt.subplot(3, 3, 5)	# Subplot for weekly expense graph
	weekly_exp_data.plot(ax = plt.gca(), style = "--", label = "Weekly expense", legend = True, sharex = False)
	weekly_exp_data.plot(ax = plt.gca(), style = ".", label = "", legend = False, sharex = False)

	monthly_exp_data = exp_data.resample("M").sum()		# Resample to get monthly expense data

	if (inc_data.empty is not True):	# Only use income data when any data exists.
		monthly_inc_data = inc_data.resample("M").sum()									# Resample on monthly freq
		monthly_comb_data = pd.concat([monthly_exp_data, monthly_inc_data], axis = 1)	# Concatenate exp/inc data
		monthly_comb_data.columns = ["Monthly expense", "Monthly income"]				# Rename columns

	else:
		monthly_comb_data = monthly_inc_data	# If no income data exists, use only expense data

	plt.subplot(3, 3, 8)	# Subplot for monthly expense graph
	ax = monthly_comb_data.plot(ax = plt.gca(), x = monthly_comb_data.index, \
		kind = "bar", legend = True, sharex = True)
	ticklabels = [""] * len(monthly_comb_data.index)										# Initate all labels to empty strings
	ticklabels[::1] = [item.strftime('%b %d') for item in monthly_comb_data.index[::1]] 	# Every ticklable shows month and day
	ticklabels[::4] = [item.strftime('%b %d\n%Y') for item in monthly_comb_data.index[::4]]	# Every 4th ticklabel includes year
	ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
	plt.gcf().autofmt_xdate()
	#color = "#694489"	# Best color ever!

	plt.subplot(1, 3, 1)	# Subplot for statistics table expense graph
	daily_mean_data = exp_data.resample("M").mean()
	daily_max_data = exp_data.resample("M").max()
	net_gain_data = monthly_comb_data["Monthly income"] - monthly_comb_data["Monthly expense"]						# Compute difference
	table_data = pd.concat([daily_mean_data, daily_max_data, monthly_comb_data, net_gain_data], axis = 1)			# Merge to one df
	table_data.columns = ["Daily mean\nexpense", "Daily max\nexpense", "Expense", "Income", "Net gain"]				# Columns in table
	table_data.index = pd.Series(table_data.index).dt.date 															# Extract only date
	table_data.index = [table_data.index[i].strftime("%b\n%Y") for i in range(len(table_data.index))]				# Make index readable
	total_row = pd.DataFrame([[el for el in table_data.sum(0)]], columns = table_data.columns, index = ["Total"])	# Row with sums of columns
	table_data = pd.concat([table_data, total_row], axis = 0)														# Merge total row at bottom
	table_data["Daily mean\nexpense"][-1] = np.mean(table_data["Daily mean\nexpense"][:-1])							# Use mean as total (not sum)
	seaborn.heatmap(table_data, annot = True, fmt = ".0f", linewidths = 0.5, cmap = "coolwarm", cbar = False)		# Generate table
	plt.title("Month-by-month statistics", fontsize = 15)															# Add title to table


if (__name__ == "__main__"):
	if ("--help" in sys.argv):
		print(help_message)
		sys.exit()

	elif (len(sys.argv) == 1):
		plt.figure(figsize = (18, 8.5))
		exp_data = get_multi_month_economy_data("expense")
		inc_data = get_multi_month_economy_data("income")
		generate_pie_chart(exp_data, "expense", "all time", multi_mode = True)
		visualize_economy_over_time(exp_data, inc_data)
		#compute_and_viz_fft(fill_missing_dates(exp_data).sum(1), "expense")

	elif((len(sys.argv) == 2) and (sys.argv[1] == "now")):
		plt.figure(figsize = (12, 6))
		exp_data = get_single_month_economy_data("expense", time.strftime("%m"), time.strftime("%Y"))
		inc_data = get_single_month_economy_data("income", time.strftime("%m"), time.strftime("%Y"))
		generate_single_month_bar_stats(exp_data, inc_data, time.strftime("%m/%Y"))
		generate_pie_chart(exp_data, "expense", time.strftime("%m/%Y"), plot_loc = 2)

	elif((len(sys.argv) == 2) and (re.search(r"\d+/\d+", sys.argv[1]) is not None)):
		plt.figure(figsize = (12, 6))
		exp_data = get_single_month_economy_data("expense", sys.argv[1][:2], sys.argv[1][3:])
		inc_data = get_single_month_economy_data("income", sys.argv[1][:2], sys.argv[1][3:])
		generate_single_month_bar_stats(exp_data, inc_data, sys.argv[1])
		generate_pie_chart(exp_data, "expense", sys.argv[1], plot_loc = 2)

	else:
		print("Error: Invalid use of cmd-line args; see 'python ecoviz.py --help'\n")
		

	plt.show()
