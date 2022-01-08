import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv' }

MONTHS = ['january', 'feburary', 'march', 'april', 'may', 'june']

DAYS_OF_WEEK = ['monday', 'tuesday', 'wednesday', 'thrusday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    user_city_selection = input("Choose your peferred city from (chicago, new york city, washington):").lower()
    
    while(user_city_selection not in CITY_DATA):
        user_city_selection = input("Please choose your peferred city from (chicago, new york city, washington):").lower()

    city = CITY_DATA[user_city_selection]
    # get user input for month (all, january, february, ... , june)
    user_month_selection = input("Choose your peferred month from (all, january, february, ... , june):").lower()

    while(user_month_selection not in MONTHS and user_month_selection != 'all'):
        user_month_selection = input("Please choose your peferred month from (january, february, ... , june):").lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    user_day_selection = input("Choose your peferred day from (monday, tuesday, ... sunday):").lower()
    while(user_day_selection not in DAYS_OF_WEEK and user_day_selection != 'all'):
        user_month_selection = input("Please choose your peferred day of the week from (all, monday, tuesday, ... sunday):").lower()


    print('-'*40)
    return city, user_month_selection, user_day_selection


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city)
    
   # extract month, day of week and hour from Start Time to create new columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'feburary', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Popular Day Of The Week:', popular_day_of_week)

    # display the most common start hour
    popular_start_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_start_station_and_end_station = (df['Start Station'] + '-' + df['End Station']).mode()[0].split('-')[0]
    print('Most Popular Start and End Station:', popular_start_station_and_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum(skipna=True)
    print('Total Travel Time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean(skipna=True)
    print('Mean Travel Time:', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print('User Type Counts:', user_types_counts)


    # Display counts of gender
    if "Gender" in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('Gender Counts:', gender_counts)

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        birth_year = df['Birth Year']
        # most common birth year
        most_common_year = birth_year.mode()[0]
        print("Most Common Birth Year:", most_common_year)
        # most recent birth year
        most_recent_birth_year = birth_year.max()
        print("Most Recent Birth Year:", most_recent_birth_year)
        # the most earliest birth year
        earliest_birth_year = birth_year.min()
        print("Most Earliest Birth Year:", earliest_birth_year)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw bikeshare data upon request"""

    # iterate from 0 to the number of rows in steps of 5
    for i in range(0, df.shape[0], 5):
        response = input('\nWould you like to examine the trip data? Enter yes or no.\n')
        if response.lower() != 'yes':
            break
        print(df.iloc[i: i + 5])

    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
