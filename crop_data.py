"""
This python file is dedicated to reading crop data in CSV files.
"""
import csv


#########################################################################################################
# main functions
#########################################################################################################
def get_crop_rating(filename: str) -> list:
    """
    Calling this function to get this specific crop's crop rating of each census division across 2005
    to 2014. This function returns the crop ratings as a list (a list of 19 inner lists, each representing
    a census division, and each inner list has 10 entries representing the crop rating from 2004 to 2005 to 2014

    >>> stat = 'data/crop/csv/Barley.csv'
    >>> get_crop_rating(stat)
    """
    unfiltered_data = read_csv_file(filename)
    filtered_data = crop_production(unfiltered_data)
    all_crop_rating = crop_rating_by_year(filtered_data)

    return all_crop_rating


def six_crop_rating() -> list:
    """
    This function uses get_crop_rating several times to get crop ratings for the following crops:
    ['All_wheat', 'Spring_wheat', 'Barley', 'Oats', 'Canola', 'Tame_hay'].
    Note that not all data is used in the interactive application/report.

    six_crop_rating returns a list. The first entry of the list contains the header:
    ['All_wheat', 'Spring_wheat', 'Barley', 'Oats', 'Canola', 'Tame_hay'], while the second entry of the list contains
    all the ratings.

    Read the following example for more information on how to use this function.

    >>> ratings = six_crop_rating()
    To access the all the crop ratings of one specific crop, access ratings[crop_index], where crop_index is the index
    position where the crop appears in the header.

    To access the crop rating of a specific row of one specific crop, access ratings[crop_index][k], where crop_index
    is the index position where the crop appears in the header, and k is the row index.

    Note that the census division number is NOT equal to the row index k.
    Conversion table below:

    To access C.D. 1 to 5, k = C.D. - 1
    To access C.D. 6 AND 15, k = 5
    To access C.D. 7 to 14, k = C.D. - 1
    To access C.D. 16 to 19, k = C.D. - 2
    To access All C.D. (total), k = 18
    """
    all_wheat = get_crop_rating('data/crop/csv/All_wheat.csv')
    spring_wheat = get_crop_rating('data/crop/csv/Spring_wheat.csv')
    barley = get_crop_rating('data/crop/csv/Barley.csv')
    oats = get_crop_rating('data/crop/csv/Oats.csv')
    canola = get_crop_rating('data/crop/csv/Canola.csv')
    tame_hay = get_crop_rating('data/crop/csv/Tame_hay.csv')
    return [['All_wheat', 'Spring_wheat', 'Barley', 'Oats', 'Canola', 'Tame_hay'],
            [all_wheat, spring_wheat, barley, oats, canola, tame_hay]]


def average_crop_rating() -> list:
    """
    This function returns a list, with the first element as the header:
    ['All_wheat', 'Spring_wheat', 'Barley', 'Oats', 'Canola', 'Tame_hay'];
    The second element is the average crop_ratings across all census division across 2005 to 2014, and
    the inner elements represent the crop in the same index position as the inner elements.
    """
    ratings = six_crop_rating()
    crop_ratings = []
    for crop in range(0, 6):
        crop_rating = 0
        for i in range(0, 18):
            for j in range(0, 10):
                crop_rating += ratings[1][crop][i][j]
        crop_ratings.append(round(crop_rating / 190, 2))
    return [['All_wheat', 'Spring_wheat', 'Barley', 'Oats', 'Canola', 'Tame_hay'], crop_ratings]


def average_crop_rating_per_cd() -> list:
    """
    This function returns a list, which contains 6 inner lists.
    Each inner list contains the average crop rating across 2005 to 2014 of each C.D..
    Note that the position of the inner list represents the crop in the same index position in
    ['All_wheat', 'Spring_wheat', 'Barley', 'Oats', 'Canola', 'Tame_hay'].
    """
    ratings = six_crop_rating()
    all_ratings_per_crop_per_cd = []
    for crop in range(0, 6):
        this_crop_rating_all_cd = []
        for i in range(0, 19):
            crop_rating_this_cd = 0
            for j in range(0, 10):
                crop_rating_this_cd += ratings[1][crop][i][j]
            this_crop_rating_all_cd.append(round(crop_rating_this_cd / 10, 2))
        all_ratings_per_crop_per_cd.append(this_crop_rating_all_cd)

    return all_ratings_per_crop_per_cd


#########################################################################################################
# helper functiosn
#########################################################################################################
def read_csv_file(filename: str) -> any:
    """
    Read a csv file containing crop data, and return a tuple (header, data). The header and data are lists.

    >>> File = 'data/crop/csv/Barley.csv'
    >>> unfiltered_data = read_csv_file(File)
    """
    with open(filename, errors='ignore') as file:
        reader = csv.reader((line.replace('\0', '') for line in file))

        headers = next(reader)
        data = [row for row in reader]

    return (headers, data)


def crop_production(unfiltered_data: tuple) -> list:
    """
    This function takes in a tuple (headers, data) in the form of the output of read_csv_file,
    and split data (of tuple) into three lists, and return a list of these three lists:
    [seeded_per_acre, yield_per_acre, production_total]

    >>> filtered_data = crop_production(unfiltered_data)
    """
    seeded_per_acre = []
    yield_per_acre = []
    production_total = []
    for i in range(0, 19):
        seeded_per_acre.append(unfiltered_data[1][i])
    for i in range(19, 38):
        yield_per_acre.append(unfiltered_data[1][i])
    for i in range(38, 57):
        production_total.append(unfiltered_data[1][i])

    return [seeded_per_acre, yield_per_acre, production_total]


def crop_rating_by_year(filtered_data: list) -> list:
    """
    A crop rating is a simple term for measuring how well the crop production was that year.
    It is equivalent of production per acre seeded (tonnes per acre).
    crop_rating_by_year returns a list of 19 lists; Each inner lists represents the crop rating of
    one census division of Alberta from 2005 to 2014.

    If either production_total or seeded_per_acre is not available, the entry returns 0.

    >>> crop_rating_by_year(filtered_data)
    """
    all_crop_rating = []    # list to be returned

    for i in range(0, 19):  # for each C.D. in filtered data
        cd_crop_rating = []     # the inner list for each C.D.
        for j in range(1, 11):  # for year in C.D.
            if filtered_data[2][i][j] != '-' and filtered_data[0][i][j] != '-':
                production = filtered_data[2][i][j].replace(',', '')
                acre_seeded = filtered_data[0][i][j].replace(',', '')
                year_rating = float(production) / float(acre_seeded)
                cd_crop_rating.append(year_rating)
            else:   # entry returns 0 if no data is available
                cd_crop_rating.append(0)
        all_crop_rating.append(cd_crop_rating)

    return all_crop_rating
