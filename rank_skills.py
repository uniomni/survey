"""Read CSV file from 2021 Digital Science Maturity and Skills Survey and rank skills by importance.

Example

python rank_skills.py CSV/Digital Science Maturity and Skills Deep Dive.csv

Ole Nielsen - 2021
"""

import csv, sys, pandas, numpy
from skills_analysis_helpers import extract_data, SFIA_skills, response_values

   
# Get filename
if len(sys.argv) != 2:
    msg = 'Filename with survey data must be supplied as command line argument'
    raise Exception(msg)
filename = sys.argv[1]


# Read data from CSV file
# There are three responses for each skill: How much it is needed, 
# How well we can access it and how sustainable it is. Therefore we read
# three columns for each skill.

skills_dict = {}
dataframe = pandas.read_csv(filename)

number_of_responses = -1 # Collect number of responses and check that it is the same across all columns.
for skill in SFIA_skills:
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
            
            # Record number of responses
            if number_of_responses == -1:
                number_of_responses = len(d['NEED'])
            else:
                msg = 'Number of responses were not the same across this data'
                assert number_of_responses == len(d['NEED']), msg



# Convert responses to numerical values
responses = {}
for skill in SFIA_skills:
    print()
    print(skill)
    responses[skill] = {}  # Create new entry for this skill
    skill_response = skills_dict[skill]  # Responses for this skill
    for key in skill_response:
        responses[skill][key] = numpy.zeros(number_of_responses)    
        for i, response in enumerate(skill_response[key]):

            val = response_values[str(response)]  # Turn e.g. nan into a string to index structure.
            responses[skill][key][i] = val
        print(' ', key, ': ', responses[skill][key])
        

# Calculate skills gaps (G) using the formula
#
# G = N - min(A, S)
# 
# where 
# G is the skills gap
# N is how much it is needed
# A is how much access we have
# S is how sustainable the access is
#
# Don't know and not applicable are treated is NaN values for the purpose of this computation.
#          

skills_gap = {}
for skill in SFIA_skills:
    response = responses[skill]
    N = response['NEED']
    A = response['ACCESS']
    S = response['SUSTAIN']        


    
#print(responses)            
    
