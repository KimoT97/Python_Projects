import time
import pandas as pd
import numpy as np

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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    print('First, Enter your desired Location (Chicago, New York City, Washington):')
    city = input().lower()
    cities = ('chicago', 'new york city', 'washington')
    while True:
        if city in cities:
           break
        print('Location not available, Please try again using this list')
        print('Availabe locations (Chicago, New York City, Washington)')
        print('Please enter your desired Location (Chicago, New York City, Washington):')
        city = input().lower()
    
    # TO DO: get user input for month (all, january, february, ... , june)
    print('Next, Enter your desired Month (all, january, february, ... , june):')
    month = input().lower()
    months=('all','january','february','march','april','may','june')
    while True:
       if month in months:
         break
       print('Incorrect input')
       print('Only choose months from january to june')
       print('Please enter your desired month (all, january, february, ... , june):')
       month = input().lower()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('Lastly, Enter your desired day of the week (Monday, Tuesday, ... , Sunday):')
    day = input().lower()
    days=('all','monday','tuesday','wednesday','thursday','friday','saturday','sunday')
    while True:
        if day in days:
          break
        print('Incorrect input')
        print('Please enter your desired day of the week (Monday, Tuesday, ... , Sunday):')
        day = input().lower()

    print('-'*40)
    return city, month, day


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

    df = pd.read_csv(CITY_DATA[city])
        # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
        # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    # filter by month if applicable
    if month != 'all':
            # use the index of the months list to get the corresponding int
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = (months.index(month)+1)
            # filter by month to create the new dataframe
            df = df[df['month']==month]
        # filter by day of week if applicable
    if day != 'all':
            # filter by day of week to create the new dataframe
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
            day = (days.index(day))
            df = df[df['day_of_week']==day]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    months=('January','Febuary','March','April','May','June')
    popular_month=months[popular_month-1]
    print('Most Popular Start Month:', popular_month)
    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    popular_day_of_week = df['day_of_week'].mode()[0]
    days=('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
    popular_day_of_week=days[popular_day_of_week]
    print('Most Popular Start Day of the Week:', popular_day_of_week)
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    if popular_hour>12 and popular_hour!=24:
        popular_hour=popular_hour-12
        print('Most Popular Start Hour:', popular_hour,'pm')
    elif popular_hour==12:
        print('Most Popular Start Hour:', popular_hour,'noon')  
    elif popular_hour==24 or popular_hour==0:
        popular_hour=12
        print('Most Popular Start Hour:', popular_hour,'midnight')
    else:
        print('Most Popular Start Hour:', popular_hour,'am')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print ('Most Popular starting station:', popular_start_station, '\n')
    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print ('Most Popular ending station:', popular_end_station, '\n')

    # TO DO: display most frequent combination of start station and end station trip
    Start_End_Combination = ('\nStarting Station: '+df['Start Station']+'\nEnding Station: '+df['End Station']).mode()[0]
    print ('Most Popular trip: ', Start_End_Combination)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time=df['Trip Duration'].sum()
    minutes, seconds = divmod(total_travel_time, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    print ('Total Travel Time: ',int(days),'days,',int(hours),'hours,',int(minutes),'minutes and',int(seconds),'seconds')
    # TO DO: display mean travel time
    average_travel_time=df['Trip Duration'].mean()
    minutes, seconds = divmod(average_travel_time, 60)
    hours, minutes = divmod(minutes, 60)
    print ('Average Travel Time: ',int(hours),'hours,',int(minutes),'minutes and',int(seconds),'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    try:
       user_types = df['User Type'].value_counts()
       print('User Types:\n')
       print(user_types.to_string())
    except:
       print('No Data Available on user types.')
    # TO DO: Display counts of gender
    try:
       gender = df['Gender'].value_counts()
       print('\nGender ratio:\n')
       print(gender.to_string())
    except:
        print('\nNo Data Available on gender.')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
       birth_year_max = int(df['Birth Year'].max())
       birth_year_min = int(df['Birth Year'].min())
       birth_year_average = int(df['Birth Year'].mean())
       print ('\nOldest Birth Year:', birth_year_min) 
       print ('Youngest Birth Year:', birth_year_max) 
       print ('Average Birth Year:', birth_year_average) 
    except:
        print('\nNo Data Available on birth years.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
       """Displays raw data of bikeshare users."""
       i = 0
       raw = input("Would you like to view bikashare raw data?, enter Yes or No:\n").lower() # TO DO: convert the user input to lower case using lower() function
       pd.set_option('display.max_columns',50)

       while True:            
           if raw == 'no':
              break
           elif raw == 'yes':
              print(df.iloc[i:(i+5)]) # TO DO: appropriately subset/slice your dataframe to display next five rows
              raw = input("<Would you like to view more raw data?, enter yes or no:\n>").lower() # TO DO: convert the user input to lower case using lower() function
              i += 5
           else:
              raw = input("\nInvalid Input, Please enter only 'Yes' or 'No'\n").lower()


def main():
    while True:
       city, month, day = get_filters()
       df = load_data(city, month, day)

       time_stats(df)
       station_stats(df)
       trip_duration_stats(df)
       user_stats(df)
       display_raw_data(df)
       
       restart = input('\nWould you like to restart? Enter yes or no.\n')
       if restart.lower() == 'no':
            break
       if restart.lower() == 'yes':
            continue
       if restart.lower() != 'yes' or restart.lower() != 'no':
            while True:
                print('\nInvalid Input? Only enter yes or no.\n')
                restart = input().lower() 
                if restart == 'yes' or restart == 'no':
                   break
       if restart.lower() == 'no':
            break


if __name__ == "__main__":
	main()
