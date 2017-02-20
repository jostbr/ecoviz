
import os
import sys
import time

def add_economy_data(exp_or_inc, cmd_line_args):
	"""Function that gets called by both add_expense.py and add_income.py and depending on
	by which, appends the expense or income to the appropriate (correct date) data file."""
	from add_expense import help_message as ehelp	# To be able to show help for add_expense.py
	from add_income import help_message as ihelp	# To be able to show help for add_expense.py

	# -------------------- HANDLING COMMAND LINE ARGUMENTS --------------------
	if ((len(cmd_line_args) == 2) and (cmd_line_args[1] == "--help")):
		if (exp_or_inc == "expense"):
			print(ehelp)

		else:
			print(ihelp)

		sys.exit()

	elif (len(sys.argv) == 3):						# If user doesen't specify date.
		economy_date = time.strftime("%d/%m/%Y")	# Assume current date
		economy_type = cmd_line_args[1]
		economy_amount = cmd_line_args[2]

	elif (len(sys.argv) == 4):				# If user specifies all parameters
		economy_date = cmd_line_args[1]
		economy_type = cmd_line_args[2]
		economy_amount = cmd_line_args[3]

	else:
		print("Error: Invalid use of cmd-line args; see 'python add_{}.py --help'".format(exp_or_inc))
		sys.exit()

	# Creating dictionary to hold months to simplify needed cmd-line input.
	months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
		7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

	economy_year = economy_date[6:]								# Extract year from date
	economy_month = economy_date[3:5]							# Extract month form date
	source_dir = os.path.dirname(os.path.abspath(__file__))		# Directory of this script
	economy_folder_path = os.path.join(source_dir, exp_or_inc)	# Directory expense/income

	if (not os.path.isdir(economy_folder_path)):	# If folder for economy_year doesn't exist
		os.makedirs(economy_folder_path)			# Create the directory

	relevant_directory = os.path.join(economy_folder_path, economy_year)

	if (not os.path.isdir(relevant_directory)):		# If folder for year doesn't exist
		os.makedirs(relevant_directory)				# Create the directory

	relevant_file = economy_month + "-" + months[int(economy_month)] + ".txt"	# Name of data file
	file_path = os.path.join(relevant_directory, relevant_file)					# Path to data file

	if (not os.path.exists(file_path)):										# If file for month doesn't exist
		with open(file_path, "w") as economy_file:
			economy_file.write("{} for".format(exp_or_inc) + \
				months[int(economy_month)] + " " + economy_year + ":\n")	# Create header for data file
			economy_file.write("-------------------------------\n")			# Decoration

	# Open and append user entered economy to relevant_file.
	with open(file_path, "a") as economy_file:
		economy_file.write("{:10} - {:13} - {:7}\n".format(economy_date, economy_type, economy_amount))
