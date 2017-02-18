
import sys
import save_eco

help_message = """\n
---------------------------------------ABOUT---------------------------------------
Program that adds user entried income to incomes.txt file in appropriate
directory corresponding to the requested date. If no directories, with the
dates entered by user, exists, they will be automatically created.

---------------------------------------USAGE---------------------------------------
Run the script with command line arguments in either of the following formats:
1) > python add_income.py <DD/MM/YYYY> <TYPE> <AMOUNT>
2) > python add_income.py <TYPE> <AMOUNT>
3) > python add_income.py --help

--> 1) Adds an income with description <TYPE> and amount <AMOUNT> to the
       textfile <YYYY>/<MM>/incomes.txt where YYYY and MM are the year and
       month (corresponding month-name to number MM) specified by user
--> 2) Same as 1) except the date is automatically chosen to current date.
--> 3) Displays this help message.\n"""

if (__name__ == "__main__"):
	save_eco.add_economy_data("income", sys.argv)
