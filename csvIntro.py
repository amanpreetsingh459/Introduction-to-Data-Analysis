"""import unicodecsv

enrollments = []
f = open('/home/aman/Desktop/Udacity/Introduction to Data Analysis/enrollments.csv', 'rb')
reader = unicodecsv.DictReader(f)

for row in reader :
    enrollments.append(row)
    
f.close()

print enrollments[0]
print enrollments[1]
"""

#using with option to avoid the use of close() function
"""import unicodecsv

enrollments = []
with open('/home/aman/Desktop/Udacity/Introduction to Data Analysis/enrollments.csv', 'rb') as f:
    reader = unicodecsv.DictReader(f)

    for row in reader :
        enrollments.append(row)
    

print enrollments[0]
print enrollments[1]
"""
#'/home/aman/Desktop/Udacity/Introduction to Data Analysis/enrollments.csv'
#use enrollments = list(reader) to convert iterator into a list


import unicodecsv

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)  #iterator 'reader' has been converted into a list


#Fixing data types-----------------------------------------

from datetime import datetime as dt

# Takes a date as a string, and returns a Python datetime object. 
# If there is no date given, returns None
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')

# Takes a string which is either an empty string or represents an integer,
# and returns an int or None.
def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)

enrollments = read_csv("/home/aman/Desktop/Udacity/Introduction to Data Analysis/enrollments.csv")
daily_engagement =read_csv("/home/aman/Desktop/Udacity/Introduction to Data Analysis/daily_engagement.csv")
project_submissions = read_csv("/home/aman/Desktop/Udacity/Introduction to Data Analysis/project_submissions.csv")

# Clean up the data types in the enrollments table
for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])

#print enrollments[0]

#getting the number of unique rows in each table

def get_unique_students(data):
    unique_students = set()
    for data_point in data:
        unique_students.add(data_point['account_key'])
    return unique_students


#print("Total number of rows in enrollments.csv: ")
#print len(enrollments)

unique_enrolled_students = get_unique_students(enrollments)
#print("Total number of Unique Rows in enrollments.csv: ")
#print len(unique_enrolled_students)


for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])


#Rename the 'acct' column to 'account_key' in daily_engagement table
for engagement_record in daily_engagement:
    engagement_record['account_key'] = engagement_record['acct']   #first create a new key with the name 'account_key' and copy all the values of the 'acct' key into it
    del[engagement_record['acct']]          #now delete all the values with 'acct' key

#print "Key renamed"
    

#print daily_engagement[0]
#print("Total number of rows in daily_engagement.csv: ")
#print len(daily_engagement)

#getting the number of unique rows in daily_engagement.csv
unique_engagement_students = get_unique_students(daily_engagement)
#print("Total number of Unique Rows in daily_engagement.csv: ")
#print len(unique_engagement_students)

for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])

#print project_submissions[0]
#print("Total number of rows in project_submissions.csv: ")
#print len(project_submissions)

#getting the number of unique rows in project_submissions.csv
unique_project_submitters = get_unique_students(project_submissions)
#print("Total number of Unique Rows in project_submissions.csv: ")
#print len(unique_project_submitters)


#Finding missing engagement records


num_problem_students = 0
for enrollment in enrollments:
    student = enrollment['account_key']
    if student not in unique_engagement_students and enrollment['join_date'] != enrollment['cancel_date']:
        #print enrollment
        num_problem_students+=1

#print num_problem_students


#create a set of the account keys for all Udacity test accounts
udacity_test_accounts = set()
for enrollment in enrollments:
    if enrollment['is_udacity']:
        udacity_test_accounts.add(enrollment['account_key'])
#print len(udacity_test_accounts)


#Given some data with an account_key field, removes any records corresponding to Udacity test accounts
def remove_udacity_accounts(data):
    non_udacity_data = []
    for data_point in data:
        if data_point['account_key'] not in udacity_test_accounts:
            non_udacity_data.append(data_point)
    return non_udacity_data

#remove udacity test accounts from all three tables
non_udacity_enrollments = remove_udacity_accounts(enrollments)
non_udacity_engagement = remove_udacity_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_accounts(project_submissions)

#print len(non_udacity_enrollments)
#print len(non_udacity_engagement)
#print len(non_udacity_submissions)


#creating a dictionary of the students who either :-
#*haven't cancelled yet
#*stated enrolled more than 7 days

paid_students = {}

for enrollment in non_udacity_enrollments:
    if(not enrollment['is_canceled'] or enrollment['days_to_cancel'] > 7):
        account_key = enrollment['account_key']
        enrollment_date = enrollment['join_date']
       
        if(account_key not in paid_students or enrollment_date > paid_students[account_key]):
            paid_students[account_key] = enrollment_date

#print len(paid_students)        #995


#Getting data from first week

# Takes a student's join date and the date of a specific engagement record,
# and returns True if that engagement record happened within one week
# of the student joining.

def within_one_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return time_delta.days < 7 and time_delta.days >= 0

#Remove the paid students who have canceled before paying i.e. after the trial period
def remove_free_trial_cancel(data):
    new_data = []
    for data_point in data:
        if data_point['account_key'] in paid_students:
            new_data.append(data_point)

    return new_data

# Remove canceled students accounts from all three tables
paid_enrollments = remove_free_trial_cancel(non_udacity_enrollments)
paid_engagement = remove_free_trial_cancel(non_udacity_engagement)
paid_submissions = remove_free_trial_cancel(non_udacity_submissions)

#Task to find Number of Visits in First Week
#from: ######################################
#                 10                 #

for engagement_record in paid_engagement:
    if engagement_record['num_courses_visited'] > 0:
        engagement_record['has_visited'] = 1
    else:
        engagement_record['has_visited'] = 0


#print len(paid_enrollments)     #1293
#print len(paid_engagement)      #134549
#print len(paid_submissions)     #3618

#####################################
#                 7                 #
#####################################

## Create a list of rows from the engagement table including only rows where
## the student is one of the paid students you just found, and the date is within
## one week of the student's join date.

paid_engagement_in_first_week = []

for engagement_record in paid_engagement:
    account_key = engagement_record['account_key']
    engagement_record_date = engagement_record['utc_date']
    join_date = paid_students[account_key]

    if within_one_week(join_date, engagement_record_date):
        paid_engagement_in_first_week.append(engagement_record)

#print len(paid_engagement_in_first_week)        #21508

##Exploring Student Engagement

# Create a dictionary of engagement grouped by student.
# The keys are account keys, and the values are lists of engagement records.
        
from collections import defaultdict

# Create a dictionary of engagement grouped by student.
# The keys are account keys, and the values are lists of engagement records.

def group_data(data, key_name):
    grouped_data = defaultdict(list)
    for data_point in data:
        key = data_point[key_name]
        grouped_data[key].append(data_point)
    return grouped_data    

engagement_by_account = group_data(paid_engagement_in_first_week, 'account_key')
# Create a dictionary with the total minutes each student spent in the classroom during the first week.
# The keys are account keys, and the values are numbers (total minutes)

def sum_grouped_items(grouped_data, field_name):
    summed_data = {}
    for key, data_points in grouped_data.items():
        total = 0
        for data_point in data_points:
            total += data_point[field_name]        
        summed_data[key] = total
        
    return summed_data

total_minutes_by_account = sum_grouped_items(engagement_by_account, 'total_minutes_visited')

# Summarize the data about minutes spent in the classroom

import numpy as np

def describe_data(data):        
    print 'Mean:', np.mean(data)
    print 'Standard deviation:', np.std(data)
    print 'Minimum:', np.min(data)
    print 'Maximum:', np.max(data)
    
    
total_minutes = total_minutes_by_account.values()
#print "Total minutes summary"
#describe_data(total_minutes)


#Lessons completed in first week

#####################################
#                 9                 #
#####################################

## Adapt the code above to find the mean, standard deviation, minimum, and maximum for
## the number of lessons completed by each student during the first week. Try creating
## one or more functions to re-use the code above.

#lessons_completed_by_account = sum_grouped_items(engagement_by_account, 'lessons_completed')
#print "Total lessons summary"
#describe_data(lessons_completed_by_account.values())


##Number of Visits in First Week
######################################
#                 10                 #
######################################

## Find the mean, standard deviation, minimum, and maximum for the number of
## days each student visits the classroom during the first week.

print "Total days any course visited in the first week summary"
days_visited_by_account = sum_grouped_items(engagement_by_account, 'has_visited')
describe_data(days_visited_by_account.values())


######################################
#                 11                 #
######################################

## Create two lists of engagement data for paid students in the first week.
## The first list should contain data for students who eventually pass the
## subway project, and the second list should contain data for students
## who do not.

subway_project_lesson_keys = ['746169184', '3176718735']

pass_subway_project = set()

for submission in paid_submissions:
    project = submission['lesson_key']
    rating = submission['assigned_rating']
    
    if project in subway_project_lesson_keys and \
        (rating == 'PASSED' or rating == 'DISTINCTION'):
            pass_subway_project.add(submission['account_key'])

passing_engagement = []
non_passing_engagement = []

for engagement_record in paid_engagement_in_first_week:
    if engagement_record['account_key'] in pass_subway_project:
        passing_engagement.append(engagement_record)
    else:
        non_passing_engagement.append(engagement_record)

print len(passing_engagement)
print len(non_passing_engagement)













