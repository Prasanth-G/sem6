import pandas

moviedata = pandas.read_csv('ratings.csv', header=0)

grouped_movies = moviedata.groupby('movieId')

for index, movie in grouped_movies:
    print(movie.describe())
    input()

'''
+ Descriptive summary :
    * Distribution
    * Central Tendency
        - Mean
        - Meadian
        - Mode
    * Dispersion
        - Variance
        - Standard Deviation
    * Correlations
'''


