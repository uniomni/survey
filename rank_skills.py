"""Read CSV file from 2021 Digital Science Maturity and Skills Survey and rank skills by importance.

Example:
python rank_skills.py "Digital Science Maturity and Skills Deep Dive.csv"

Ole Nielsen - 2021
"""

import csv, sys, pandas, numpy
from skills_analysis_helpers import extract_data, SFIA_skills, SFIA_abbreviations, response_values, sort_dictionary_by_value

   
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
            
            # Record number of responses
            if number_of_responses == -1:
                number_of_responses = len(d['NEED'])
            else:
                msg = 'Number of responses were not the same across this data'
                assert number_of_responses == len(d['NEED']), msg



# Convert responses to numerical values
responses = {}
for skill in SFIA_abbreviations:
    #print()
    #print(skill)
    responses[skill] = {}  # Create new entry for this skill
    skill_response = skills_dict[skill]  # Responses for this skill
    for key in skill_response:
        responses[skill][key] = numpy.zeros(number_of_responses)    
        for i, response in enumerate(skill_response[key]):

            val = response_values[str(response)]  # Turn e.g. nan into a string to index structure.
            responses[skill][key][i] = val
        #print(' ', key, ': ', responses[skill][key])
        

# Calculate skills gaps (G) using the formula
#
# G = avg(N - min(A, S))
# 
# where 
# G is the skills gap
# N is how much it is needed
# A is how much access we have
# S is how sustainable the access is
#

skills_gap = {}
needs = {}
for skill in SFIA_abbreviations:
    response = responses[skill]
    N = response['NEED']
    A = response['ACCESS']
    S = response['SUSTAIN']        

    # We treat the Don't know (-1) and N/A (nan) as follows
    #
    # Don't know (-1) should count as follows
    # N: 3 (Same as neither agree nor disagree in regards to whether we need the skill)
    # A: 3 (If we don't know if we have access to a skill we set it to 3 as well)
    # S: 0 (It is really bad if we don't know if something we need is sustainable).
    #
    # N/A (nan) should count as 
    # N: 0 (i.e. skill not important to this respondent)
    # A: 3 (we really mind either way)
    # S: 3 (we don't care if it sustainable so again set it to 3)
       
    # Replace Don't Know with appropriate numerical values:
    N[N==-1] = 3  # 0 -> 3
    A[A==-1] = 3  # 0 -> 3
    S[S==-1] = 0  # 0 -> 0
    
    # Replace N/A with appropriate numerical values:
    N[numpy.isnan(N)] = 0  # nan -> 0        
    A[numpy.isnan(A)] = 3  # nan -> 3
    S[numpy.isnan(S)] = 3  # nan -> 3    
                
    # Round negative numbers to 0 (We don't care about access and sustainability of skills we don't need)
    G = (N - numpy.minimum(A, S))  #.clip(min=0)  # Can round to 0 if needed using this command.
     
    # Take the averages and save
    skills_gap[skill] = numpy.mean(G)
    needs[skill] = numpy.mean(N)



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



    

    
