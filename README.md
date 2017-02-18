# EcoViz
Software package for personal economy tracking and visualization.

## How to get started
Download the four source files and store them in a directory of choice. Then when you have a new expense or income you run add_expense.py or add_income.py respectively, to save the expense/income to a data file. Now you have stored some economy data and can run ecoviz.py to visualize the data. Here the data can be visualized either for a (any) single month or for the entire time span since the beginning of expense/income tracking. Instructions for use of command line arguments can be found by providing `--help` flag to either of the three above mentioned scripts.

**Note:** The code is not fully developed so in order for ecoviz.py to work properly, there needs to exist both expense and income data, i.e. you will have to have run add_expense.py and add_income.py with some input data. Also, even if you have entered a lot of expense data, ecoviz.py will still crash if there are no income data.

## Requirements
The code is witten in Python 3.6, but I would assume (untested) any 3.x version will do the job. Unfortunaetly probably uncompatible with Python 2.7. Total list of requirements (excluding standard library modules):
- Python 3.x
- NumPy
- Matplotlib
- Pandas
- Seaborn
Although these can be installed sperately, often recommended approach is to install the Anaconda distribution found [Here](https://www.continuum.io/downloads). This Python distribution comes with a ton of useful packages for scientific computing wthout having to install any packages manually.

## What happens behind the curtains?
When you run add_expense.py and add_income.py for the first time, new directories 'expense' and 'income' are generated. In addition, directories for the relevant year and a new textfile for the month of the input data, are generated. When you add an expense/income in the e.g. same month as before, the scripts appends to the already existing textfile.

Furthermore the main script ecoviz.py utilizes the pandas module for data analysis and visualization. Here, depending on the command line arguments, expense/income data is gathered and plotted in various ways. Here one can definetly change the source if one wishes to represent the data in another way.

## Shortcomings and future development areas
1. As mentioned above, the code does not take into account that a user may only be tracking/inputting expense or income data, but not the other. Adding support for this may be done in the future.
2. The visualization for single month data is not optimal as the bar and pie chart almost shows the same thing. Any idea for something to replace the bar chart here, is welcome.
3. When using ecoviz.py with very little data, the visualization may be rather boring and not so neat looking. Although a flexible solution to this may hard to fix as the data is so limited anyway.
4. After long usage of the software the number of days/weeks/months of data may become large and thus some of the plots/tables (axis, number of rows in table, etc.) in may look like a mess, however this is untested.
