"""Read CSV file from 2021 Digital Science Maturity and Skills Survey
   and rank skills by importance.

Example:
python rank_skills.py DSMS_Survey_20210803.csv

The file argument is as downloaded (All Responses Data) from the 
GA Digital Science Maturity and Skills Deep Dive on Survey Monkey.

The script is specific to this survey only.

Ole Nielsen - 2021
"""

import csv
import sys
import pandas
import numpy

from skills_analysis_helpers import extract_data, SFIA_skills,\
    SFIA_abbreviations, response_values, sort_dictionary_by_value

# Get filename
if len(sys.argv) != 2:
    msg = 'Filename with survey data must be supplied as command line argument'
    raise Exception(msg)
filename = sys.argv[1]


# Read data from CSV file
# There are three responses for each skill:
# - How much it is needed,
# - How well we can access it and
# - How sustainable is it.
# Therefore we read three columns for each skill.

skills_dict = {}
dataframe = pandas.read_csv(filename)

number_of_responses = -1  # Flag keeping track of columns
for skill in SFIA_abbreviations:
    # Collect responses for each skill

    # Find columns with responses for this skill.
    # This is done through linear searching, but data is small
    # so it doesn't pose a performance issue.

    additional_columns_to_collect = 0
    for item in dataframe.items():
        if additional_columns_to_collect > 0:
            # Collect remaining responses for current skill

            if additional_columns_to_collect == 2:
                d['ACCESS'] = extract_data('ACCESS', item)

            if additional_columns_to_collect == 1:
                d['SUSTAIN'] = extract_data('SUSTAIN', item)

            additional_columns_to_collect -= 1

        if skill in item[0]:
            # Collect first response for this skill
            additional_columns_to_collect = 2

            d = skills_dict[skill] = {}   # Create new entry
            d['NEED'] = extract_data('NEED', item)

            # Record number of responses and test that it is the same across
            # all columns.
            if number_of_responses == -1:
                number_of_responses = len(d['NEED'])
            else:
                msg = 'Number of responses were not the same across this data'
                assert number_of_responses == len(d['NEED']), msg


# Convert responses to numerical values
responses = {}
for skill in SFIA_abbreviations:
    responses[skill] = {}  # Create new entry for this skill
    skill_response = skills_dict[skill]  # Responses for this skill
    for key in skill_response:
        responses[skill][key] = numpy.zeros(number_of_responses)
        for i, response in enumerate(skill_response[key]):

            # Make sure all indices are strings and get value
            # from response values
            val = response_values[str(response)]
            responses[skill][key][i] = val


# Calculate skills gaps (G) using the formula
#
# G = avg(N - min(A, S))
#
# where
# G is the skills gap
# N is how much it is needed
# A is how much access we have
# S is how sustainable the access is


skills_gap = {}
needs = {}
for skill in SFIA_abbreviations:
    response = responses[skill]
    N = response['NEED']
    A = response['ACCESS']
    S = response['SUSTAIN']

    # Remove "N/A" and Don't Know
    N = N[~numpy.isnan(N)]
    A = A[~numpy.isnan(A)]
    S = S[~numpy.isnan(S)]

    # Find the mean values of each metric
    N = numpy.mean(N)
    A = numpy.mean(A)
    S = numpy.mean(S)

    # Calculate Gap
    G = N - min(A, S)

    # Save the values
    skills_gap[skill] = G
    needs[skill] = N

# Print out skills sorted by need only
L = sort_dictionary_by_value(needs)
print()
print('------------------------------')
print('Skills sorted by average need:')
print('------------------------------')
for item in L[::-1]:  # Reverse order
    skill = item[0]
    weight = item[1]
    print('%.2f: %s (%s)' % (weight, SFIA_skills[skill], skill))

# Print out skills sorted by gap
L = sort_dictionary_by_value(skills_gap)
print()
print('-----------------------------')
print('Skills sorted by average gap:')
print('-----------------------------')
for item in L[::-1]:  # Reverse order
    skill = item[0]
    weight = item[1]
    print('%.2f: %s (%s)' % (weight, SFIA_skills[skill], skill))
