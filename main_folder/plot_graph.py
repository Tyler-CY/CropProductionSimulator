"""
This file is dedicated to plotting graphs, including but not limited to plotting graphs of past crop production,
graphs of past weather report, graphs of future crop production prediction.
"""
from matplotlib import pyplot as plt
import matplotlib as mpl
import crop_data    # to get all crop ratings using six_crop_rating
import weather_data     # to use wanted_column function
import math

# resets matplotlib to default mode
mpl.rcParams.update(mpl.rcParamsDefault)


#########################################################################################################
# main functions for plotting data related to crops
#########################################################################################################
def plot_graph(crop_cd: tuple) -> None:
    """
    This function takes in a tuple(crop: str, cd: int) and plots the graph of the crop rating of a specific crop in
    the census division chosen.

    Instructions to enter your choice of census division:
        Conversion table below:

        To access C.D. 1 to 5, k = C.D. - 1
        To access C.D. 6 AND 15, k = 5
        To access C.D. 7 to 14, k = C.D. - 1
        To access C.D. 16 to 19, k = C.D. - 2
        To access All C.D. (total), k = 18
    """
    ratings = crop_data.six_crop_rating()
    gg = ratings[0]
    crop_index = gg.index(crop_cd[0])

    label = 18
    if 0 <= crop_cd[1] <= 4:
        label = crop_cd[1] + 1
    elif crop_cd[1] == 5:
        label = '6 & 15'
    elif 6 <= crop_cd[1] <= 13:
        label = crop_cd[1] + 1
    elif 14 <= crop_cd[1] <= 17:
        label = crop_cd[1] + 2
    elif crop_cd[1] == 18:
        label = 'Total'

    x = [x for x in range(2005, 2015)]
    y = ratings[1][crop_index][crop_cd[1]]
    plt.plot(x, y, label=str(label), marker='o')

    plt.xlabel('Year')
    plt.ylabel('Crop Rating')
    plt.title(crop_cd[0] + ' Rating in Census Division ' + str(label))
    plt.legend()
    plt.grid(True, linewidth=1)
    plt.show()


# UPDATED
def plot_crop_rating_by_year(data) -> None:
    """
    This function takes in string of the crop type (e.g. 'Barley') and plots the graph of the average crop rating
     of that crop across 2005 to 2014.
    """
    x = [x for x in range(2005, 2015)]
    y = data
    plt.plot(x, y, label=str('crop'), marker='o')
    plt.grid(True, linewidth=1)
    plt.show()


#########################################################################################################
# main functions for plotting data related to weather
#########################################################################################################
def plot_column(file_period_m1_m2: tuple) -> None:
    """
    Select a specific column of the weather data, and plot the selected column of weather data.
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
    pd = file_period_m1_m2[1]
    x_data = []

    y_data = weather_data.wanted_column(file_period_m1_m2)
    if pd == 0:
        x_data = [x for x in range(1950, 2005)]
    elif pd == 1:
        x_data = [x for x in range(2005, 2015)]
    elif pd == 2:
        x_data = [x for x in range(2015, 2101)]

    label = str(file_period_m1_m2[0].split('/')[2].split('.')[0])
    plt.plot(x_data, y_data, label=str(label))
    plt.xlabel('Year')
    plt.ylabel('Weather Data')
    plt.title(label)
    plt.grid(True, linewidth=1)
    plt.legend()
    plt.show()


#########################################################################################################
# main functions for simulation
#########################################################################################################
def mix_plot(two_data: list, pd) -> None:
    """
    Plot 2 kinds of data (e.g., weather + crop)
    This function takes a list of two lists of the same dimension/length and the period).
    """
    x_data = []

    if pd == 0:
        x_data = [x for x in range(1950, 2005)]
    elif pd == 1:
        x_data = [x for x in range(2005, 2015)]
    elif pd == 2:
        x_data = [x for x in range(2015, 2101)]

    for data in two_data:
        plt.plot(x_data, data, label=str('TODO'))
    plt.xlabel('Year')
    plt.ylabel('Weather Data')
    plt.title('Weather and Crop Rating prediction')
    plt.legend()
    plt.grid(True, linewidth=1)
    plt.show()


def mix_subplots(two_data: list, pd) -> None:
    """
    Plot 2 kinds of data (e.g., weather + crop)
    This function takes a list of two lists of the same dimension/length and the period).
    two_data is a list with the first element as weather data, second element as crop data
    """
    x_data = []

    if pd == 0:
        x_data = [x for x in range(1950, 2005)]
    elif pd == 1:
        x_data = [x for x in range(2005, 2015)]
    elif pd == 2:
        x_data = [x for x in range(2015, 2101)]

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
    ax1.plot(x_data, two_data[0], label=str('Weather'))
    ax2.plot(x_data, two_data[1], label=str('Crop Rating'))
    ax1.set_title('Weather and Crop Rating prediction')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Weather')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Crop')

    ax1.legend()
    ax2.legend()

    ax1.grid(True, linewidth=1)
    ax2.grid(True, linewidth=1)

    plt.show()


def simulate(data: list, scenario: list) -> None:
    """
    This function stimulates weather and crop production from 2015 to 2100.
    The first parameter is a list: the first element is a list of weather data and the second element is crop string
    The second parameter is a list of scenario: [Census division (ROW), m1: mean/mode/median, m2: RCP(3,6,9)]
    """
    crop_index = crop_data.six_crop_rating()[0].index(data[1])
    crop_data_1 = crop_data.six_crop_rating()[1][crop_index][scenario[0]]
    weather_1 = weather_data.wanted_column((data[0], 1, scenario[1], scenario[2]))
    r = pearson(crop_data_1, weather_1)
    coef = regression(weather_1, crop_data_1)
    weather_2 = weather_data.wanted_column((data[0], 2, scenario[1], scenario[2]))
    crop_data_2 = []
    for k in range(0, len(weather_2) - 1):
        next_year_rating = crop_data_1[9] + coef[1] * r * (weather_2[k + 1] - weather_2[k]) * 3.5
        crop_data_2.append(next_year_rating)
        if k == len(weather_2) - 2:
            crop_data_2.append(next_year_rating)
    mix_subplots([weather_2, crop_data_2], 2)


#########################################################################################################
# helper functions for simulate
#########################################################################################################

def regression(x_data: list, y_data: list) -> tuple:
    """
    a function for generating a simple regression model. Returns a tuple (a, b), which satisfies the equation
    y = a + bx
    """
    x_mean = sum(x_data) // len(x_data)
    y_mean = sum(y_data) // len(y_data)
    numerator = 0
    denominator1 = 0
    denominator2 = 0
    for i in range(0, len(x_data)):
        temp_x = x_data[i] - x_mean
        temp_y = y_data[i] - y_mean
        numerator += temp_x * temp_y
        denominator1 += temp_x ** 2
        denominator2 += temp_y ** 2

    b = numerator / denominator1
    a = y_mean - b * x_mean
    return (a, b)


def pearson(x_data: list, y_data: list) -> float:
    """
    Find the correlation between a set of data x_data and another set y_data
    """
    x_mean = sum(x_data) // len(x_data)
    y_mean = sum(y_data) // len(y_data)
    numerator = 0
    denominator1 = 0
    denominator2 = 0
    for i in range(0, len(x_data)):
        temp_x = x_data[i] - x_mean
        temp_y = y_data[i] - y_mean
        numerator += temp_x * temp_y
        denominator1 += temp_x ** 2
        denominator2 += temp_y ** 2
    return numerator / math.sqrt(denominator1 * denominator2)
