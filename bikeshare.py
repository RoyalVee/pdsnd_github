import time
import pandas as pd
import numpy as np

#dictionary of city data options
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city will you like to analyze (chicago, new york city, washington) : ").lower().strip()
    city_list = ["chicago", "new york city", "washington"]
    while city not in city_list:
        print(
            "\t Oops! Invalid city entry. Kindly enter one of the following cities chicago, new york city or washington to analyze")
        city = input("Enter name of the city to analyze: ").lower().strip()

    # get user input for month (all, january, february, ... , june)
    month = input("Enter name of the month you wish to filter the data by, or 'all\' to apply no month filter: ").lower().strip()
    month_list = ["all", "january", "february", "march", "april", "may", "june", "july", "august", "september",
                  "october", "november", "december"]
    while month not in month_list:
        print(
            "\t Oops! Invalid month filter entry. Kindly enter one of the following month: \n \t\t January, February, March, April, May, June, July, August, September, October, November, December \n \t\t or 'all\' to apply no month filter")
        month = input("Enter name of the month to filter by, or 'all\' to apply no month filter: ").lower().strip()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter name of the day of week to filter by, or 'all\' to apply no day filter:  ").lower().strip()
    day_list = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    while day not in day_list:
        print(
            "\t allOops! Invalid day filter entry. Kindly enter one of the following day of the week: \n \t\t Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. \n \t\t or 'all\' to apply no month filter")
        day = input("Enter name of the day of week to filter by, or 'all\' to apply no day filter:  ").lower().strip()


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Filter data set to user specifcation.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])       #Load the specified data to df

    #convert the data type for Start time and End time to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])

    #Split the Start time and end time into month, day and hour colums
    df["Start Month"] = df["Start Time"].dt.month
    df["Start Day"] = df["Start Time"].dt.day_name()
    df["Start Hour"] = df["Start Time"].dt.hour

    df["End Month"] = df["End Time"].dt.month
    df["End Day"] = df["End Time"].dt.day_name()
    df["End Hour"] = df["End Time"].dt.hour

    #filtering the dataset based on specified entry. 
    if month != "all":      # filter data by month given
        month_list = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
                  "october", "november", "december"]
        month = month_list.index(month) + 1
        df = df[df["Start Month"] == month]

    if day != "all":
        df = df[df["Start Day"] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print("Based on the data filter specification provided the following analysis were derived.\n")
    # display the most common month
    peak_start_month = df["Start Month"].mode()[0] - 1
    peak_end_month = df["End Month"].mode()[0] - 1

    month_list = ["january", "february", "marcch", "april", "may", "june", "july", "august", "september",
                  "october", "november", "december"]

    print("\t The highest number of bike travel started in {} and most bike ride ended in {}\n".format(month_list[peak_start_month], month_list[peak_end_month]))

    # display the most common day of week
    common_weekday = df["Start Day"].mode()[0]

    print("\t The most common week day for bike riding is {}\n".format(common_weekday))

    # display the most common start hour
    common_start_hour = df["Start Hour"].mode()[0]
    common_end_hour = df["End Hour"].mode()[0]

    print("\t Most ride started at about the {}th hour while most ride ended about the {}th hour \n".format(common_start_hour,common_end_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_stn = df["Start Station"].mode()[0]
    print("\t The most popular start station is {} \n".format(common_start_stn))

    # display most commonly used end station
    common_end_stn = df["End Station"].mode()[0]
    print("\t The most popular end station is {} \t".format(common_end_stn))

    # display most frequent combination of start station and end station trip

    df["Start and End Stn"] = df["Start Station"] + df["End Station"]    #Concating both start and end station to produce a new column which is a combination of the two locations

    #filtering out the start and end station for the most frequent combination on the "Start and End Stn" column in the data set
    start_comb = df['Start Station'][df["Start and End Stn"] == df["Start and End Stn"].mode()[0]].unique()[0]
    end_comb = df['End Station'][df["Start and End Stn"] == df["Start and End Stn"].mode()[0]].unique()[0]

    print("\t The most frequent combination of start and end station trip is \"{}\" and \"{}\" respectively. \n".format(start_comb, end_comb))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""


    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_trip_duration = df["Trip Duration"].sum()

    print("\t The total trip duration for the specified data is : {} \n".format(total_trip_duration))

    # display mean travel time
    average_trip_duration = df["Trip Duration"].mean()
    print("\t The average trip duration is :  {} \n".format(average_trip_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = dict(df.groupby(["User Type"])["User Type"].count())
    print("\n \t The bike Users type distribution is given below: \n \t\t User Type \t\t Total ")
    for user_type in user_types.keys():
        print("\t\t {} : \t {}".format(user_type, user_types[user_type]))

    # Display counts of gender
    try:    #some of the data set does not have a gender column. handling the expection
        user_genders = dict(df.groupby(["Gender"])["Gender"].count())
        print("\n \t The bike users gender distribution is given below: \n \t\t Gender \t Total ")
        for user_gender in user_genders.keys():
            print("\t\t {} : \t {}".format(user_gender, user_genders[user_gender]))
    except:
        print("\t There is currently no gender classification in the specified city bike data \n")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year_of_birth = list(df["Birth Year"].dropna().sort_values(ascending=True).head(1))
        print("\n \t The earliest year of birth for the bike users in the data specified is : {} \n".format(int(earliest_year_of_birth[0])))

        most_recent_year_of_birth = list(df["Birth Year"].dropna().sort_values(ascending=False).head(1))
        print("\t The most recent year of birth for the bike users in the data specified is : {} \n".format(int(most_recent_year_of_birth[0])))

        most_common_year_of_birth = int(df["Birth Year"].mode()[0])
        print("\t The most common year of birth for the bike users in the data specified is : {} \n".format(most_common_year_of_birth))
    except:
        print("\t There is currently no year of birth data for the city selected \n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df):
    """
        Display the data set used for the analysis in steps of 5 rows based on user interest.

        Args:
            (dataframe) df - dataframe used for the analysis
        """

    # delete the combination column created
    df = df.drop(columns=["Start and End Stn"], axis=1)

    answer = input("Do you wish to see the first 5 rows of the raw data set? (yes or no): ").lower().strip() #requsting user consent to display the dataset

    #index position holder for viewing the data set rows in step of 5's
    start_index = 0
    end_index = 10

    # while loop to keep requesting user consent to see more of the raw data
    while answer == "yes" and end_index <= df.size:
        print(df[start_index: end_index])
        start_index = end_index
        end_index += 5
        answer = input("Do you wish to see the next first 5 rows of the raw data? (yes or no) : ").lower().strip()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
