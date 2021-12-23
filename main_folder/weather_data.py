"""
This python file is dedicated to reading crop data in CSV files.
"""
import csv


#########################################################################################################
# main functions
#########################################################################################################
def get_weather_data(filename: str) -> list:
    """
    This function reads a csv file containing weather data and turn it into a tuple (header, data).
    The tuple will then be filterede into     [data_1950_to_2004, data_2005_to_2014, data_2015_to_2100].
    For more information, read the docstring of read_csv_file and weather_periods
    """
    unfiltered_data = read_csv_file(filename)
    filtered_data = weather_periods(unfiltered_data)
    return filtered_data


def wanted_column(file_period_m1_m2: tuple) -> list:
    """
    Select a specific column of the weather data.
    The input is a tuple (file: str, period: int, m1: int, m2: int)
    To see how to get a specific column, read the instructions below.

    How to read this:
    - file is a string (str)
    - for period, m1 and m2:
        INPUT_1: WANTED_DATA_CHOICE_1;  INPUT_2: WANTED_DATA_CHOICE_2'; ...

    file: str
    period: 0: 1950-2004;   1: 2005-2014    2: 2015-2100
    m1: 1: median;  2: min;   3: max
    m2: 3: RCP 2.6;    6: RCP 4.5;  9: RCP 8.5
    """
    file, pd, m1, m2 = file_period_m1_m2
    data = get_weather_data(file)
    period = data[pd]
    if pd == 0:
        y_data = [row[m1] for row in period]
    else:
        y_data = [row[m1 + m2] for row in period]
    return y_data


#########################################################################################################
# helper functions
#########################################################################################################
def read_csv_file(filename: str) -> any:
    """
    Read a csv file containing weather data, and return a tuple (header, data). The header and data are lists.

    >>> unfiltered_data = read_csv_file('data/weather/precipitation.csv')
    """
    with open(filename, errors='ignore') as file:
        reader = csv.reader(file)

        headers = next(reader)
        data = [row for row in reader]

    return (headers, data)


def weather_periods(unfiltered_data: tuple) -> list:
    """
    This function takes in a tuple (headers, data) in the form of the output of read_csv_file,
    and split data (of tuple) into three lists, and return a list of these three lists:
    [data_1950_to_2004, data_2005_to_2014, data_2015_to_2100]

    For the first list, each inner list is of length 4, with the following data: year, median, min, max
    For the second and third list, each inner list is of length 13, with the following data:
        year, NULL, NULL, NULL, 2.6 median, 2.6 min, 2.6 max, 4.5 median, 4.5 min, 4.5 max, 8.5 median, 8.5 min, 8.5 max

    >>> filtered_data = weather_periods(unfiltered_data)

    """
    data_1950_to_2004 = []
    data_2005_to_2014 = []
    data_2015_to_2100 = []
    for i in range(0, 151):
        datetime_str = unfiltered_data[1][i][0].split('-')
        unfiltered_data[1][i][0] = datetime_str[0]
        unfiltered_data[1][i][0] = int(unfiltered_data[1][i][0])
        for j in range(1, len(unfiltered_data[1][i])):
            if unfiltered_data[1][i][j] != '':
                unfiltered_data[1][i][j] = float(unfiltered_data[1][i][j])
    for i in range(0, 55):
        data_1950_to_2004.append(unfiltered_data[1][i])
    for i in range(1, 4):
        unfiltered_data[1][55][i] = ''
    for i in range(55, 65):
        data_2005_to_2014.append(unfiltered_data[1][i])
    for i in range(65, 151):
        data_2015_to_2100.append(unfiltered_data[1][i])

    return [data_1950_to_2004, data_2005_to_2014, data_2015_to_2100]
