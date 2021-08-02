"""Auxiliary functions and definitions for extracting and analysing skills from 
GA Digital Science Maturity and Skills Deep Dive 2021
"""

from numpy import nan



SFIA_skills = {'IRMG': 'Information governance', 
               'SCTY': 'Information security',
               'INAN': 'Analytics',
               'VISL': 'Data visualisation',
               'BPRE': 'Business process improvement',
               'ARCH': 'Solution architecture',
               'DATM': 'Data management',
               'BUAN': 'Business analysis',
               'DLMG': 'Systems development management',
               'DESN': 'Systems design',
               'SWDN': 'Software design',
               'PROG': 'Programming/software development',
               'RESD': 'Real-time/embedded systems development',
               'ADEV': 'Animation development',
               'DTAN': 'Data modelling and design',
               'DBDS': 'Database design',
               'TEST': 'Testing',
               'HCEV': 'User experience design',
               'SCMD': 'Scientific Modelling',
               'NUMA': 'Numerical Analysis',
               'HPCC': 'High Performance Computing',
               'DATS': 'Machine Learning and Data Science'}
               
SFIA_abbreviations = SFIA_skills.keys()               
        
response_values = {"Strongly Disagree": 1,
                   "Disagree": 2, 
                   "Neither agree nor disagree": 3,
                   "Agree": 4,
                   "Strongly Agree": 5,
                   "Don't Know": -1,
                   "nan": nan}  # IEEE value for Not A Number
                
        
def extract_data(field, item):
    """Helper function to extract pandas data
    """
    
    data = item[1:][0]  # Pull out data from tuple
    assert(field.lower() in data[0]) # Check that the right keyword is in the header             
    return(list(data[1:]))  # Return data as a list

def sort_dictionary_by_value(D):
    """Sort dictionary of the form key: value
    """
    
    # Sort skills by gap (Schwarzian Transform)
    L = [(x[1], x) for x in D.items()]
    L.sort()
    return([(x[1][0], x[1][1]) for x in L])
    

    
