###############################################################################
############################# BIKESHARE PROJECT ###############################
###############################################################################

# import useful modules
import time
import pandas as pd
import numpy as np

# define dictionaries with the relevant data
CITY_DATA = { 'chicago': '/Users/eliassimos/Desktop/bikeshare-2/chicago.csv',
              'new york city': '/Users/eliassimos/Desktop/bikeshare-2/new_york_city.csv',
              'washington': '/Users/eliassimos/Desktop/bikeshare-2/washington.csv' }

day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
month = ['January', 'February', 'March', 'April', 'May', 'June']

###############################################################################
############################# USEFUL FUNCTIONS ################################
###############################################################################

# ask for which of the 3 cities the user wants to explore
def get_city():
    city = ''
    while city.lower not in ['new york', 'chicago', 'washington']:
        city = input('CHOOSE CITY: New York (NY), Chicago (CHI) or Washington (WA)?')
        if city.lower() == 'ny':
            return 'new york city'
        elif city.lower() == 'chi':
            return 'chicago'
        elif city.lower() == 'wa':
            return 'washington'
        else:
            print('Please enter the correct city name\n')
    return city

# ask whether the users wants to filter by day, month or not filter at all
def get_filter():
    filter = ""
    while filter.lower() not in ['day', 'month', 'no filter']:
        filter = input('Would you like to filter by: DAY, MONTH or NO FILTER at all?\n')
        if filter.lower() not in ['day', 'month', 'no filter']:
            print('Please try again\n')
    return filter

# filter for month
def get_month():
    month = ""
    month_dict = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6}
    while month.lower() not in month_dict.keys():
        month = input('\nWhich month data would you like to see - JAN, FEB, MAR, APR, MAY, or JUN?\n')
        if month.lower() not in month_dict.keys():
            print('Please try again\n')
    month = month_dict[month.lower()]
    return month

# filter for day
def get_day():
    day = ""
    day_dict = {'m': 'Monday', 't': 'Tuesday', 'w': 'Wednesday', 'th': 'Thursday', 'f': 'Friday', 'sa': 'Saturday', 'sun': 'Sunday'}
    while day.lower() not in day_dict.keys():
        day = input('Which day would you like to see - MONDAY (m), TUESDAY (t), WEDNESDAY (w), THURSDAY (th), FRIDAY (f), SATURDAY (sa), SUNDAY (sun)\n')
        if day.lower() not in day_dict.keys():
            print('Please try again\n')
    day = day_dict[day.lower()]
    return day

# find the most popular month
def top_month(df):
    start_time = time.time()

    value = int(df['Start Time'].dt.month.mode())
    p_month = month[value]
    print('- MONTH: {}'.format(p_month))

# find the most popular day
def top_day(df):
    start_time = time.time()

    day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    value = int(df['Start Time'].dt.dayofweek.mode())
    p_day = day[value]
    print(' - DAY: {}'.format(p_day))

# find the most popular hour
def top_hour(df):
    start_time = time.time()

    value = int(df['Start Time'].dt.hour.mode())
    print(' - JOURNEY START HOUR: {}:00'.format(value))

# find the most popular station
def top_station(df):
    start_time = time.time()

    value_start = df['Start Station'].mode().to_string(index = False)
    value_end = df['End Station'].mode().to_string(index = False)
    print(' - START STATION: {}'.format(value_start))
    print(' - END STATION: {}'.format(value_end))

# find the most popular combo station
def top_route(df):
    start_time = time.time()

    # creates a 'trip' column which matches the start and end station for the popular_trip() function
    df['trip'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    value = df['trip'].mode().to_string(index = False)
    print(' - JOURNEY (FROM/TO): {}'.format(value))

# find the most popular travel time
def travel_time(df):
    start_time = time.time()
    total_time = df['Trip Duration'].sum()
    mins, sec = divmod(total_time, 60)
    hour, mins = divmod(mins, 60)
    print ('\nRegarding time spent journeying:')
    print(' - TOTAL TRAVEL TIME: {} hours and {} minutes'.format(hour, mins))

    mean_time = round(df['Trip Duration'].mean())
    mins, sec = divmod(mean_time, 60)
    hour, mins = divmod(mins, 60)
    print(' - MEAN TRAVEL TIME:{} hours and {} minutes'.format(hour, mins))

# user count by subs and casuals
def user_distr(df):
    start_time = time.time()

    sub = (df['User Type'] == 'Subscriber').sum()
    cust = (df['User Type'] == 'Customer').sum()
    print('\nThe distribution between subs and casual users was: \n - SUBSCRIBERS: {} \n - CASUAL USER: {}'.format(sub, cust))

# user count by gender
def gender_distr(df):
    start_time = time.time()

    male = (df['Gender'] == 'Male').sum()
    female = (df['Gender'] == 'Female').sum()
    print('\nThe distribution by gender looked like: \n - MALES: {} \n - FEMALES: {}'.format(male, female))

# user count by DOB
def dob_stats(df):
    start_time = time.time()

    dob_min = int(df['Birth Year'].min())
    dob_max = int(df['Birth Year'].max())
    dob_mode = int(df['Birth Year'].mode())
    print('\nAnd some stats on the age of people that travelled in the selected window: \n - OLDEST was born in: {} \n - YOUNGEST was born in: {} \n - MOST COMMON year of birth was: {}\n'.format(dob_min, dob_max, dob_mode))

# display data in batches of 5
def display_data(df):
    start = 0
    end = 5
    choice = ''
    while choice.lower() not in ['y', 'n']:
        choice = input('Do you want to view indiviual trip data? Type \'Y\' or \'N\'\n')
        if choice.lower() not in ['y', 'n']:
            print('Please try again\n')
        elif choice.lower() == "y":
            print(df.iloc[start:end])

            while True:
                sec_choice = input('\nDo you want to view more trip data? Type \'Y\' or \'N\'\n')
                if sec_choice.lower() not in ['y', 'n']:
                    print('Please try again\n')
                elif sec_choice.lower() == "y":
                    start += 5
                    end += 5
                    print(df.iloc[start:end])
                elif sec_choice == "n":
                    return
        elif choice.lower() == "n":
            return
    return

###############################################################################
############################ MAIN PROGRAM LOGIC ###############################
###############################################################################

def main():
    while True:
        # Read city name (Either New York, Chicago or Washington)
        city = get_city()

        # Read csv file for the city selected
        df = pd.read_csv(CITY_DATA[city], parse_dates = ['Start Time', 'End Time'])
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        print()
        # Read month and day
        filters = get_filter()
        if filters == 'month':
            month = get_month()
            df['month'] = df['Start Time'].dt.month
            df = df[df['month'] == month]
            print()
        elif filters == 'day':
            day = get_day()
            df['day'] = df['Start Time'].dt.weekday_name
            df = df[df['day'] == day]
            print()
        # OUTPUT
        print ('In the timeframes you selected, the following were the MOST POPULAR:')
        if filters == 'none':
            top_month(df)
        if filters == 'none' or filters == 'month':
            top_day(df)
        top_hour(df)
        top_station(df)
        top_route(df)
        travel_time(df)
        user_distr(df)
        gender_distr(df)
        dob_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter Y or N.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
