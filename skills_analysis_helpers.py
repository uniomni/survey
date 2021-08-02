"""Auxiliary functions and definitions for extracting and analysing skills from 
GA Digital Science Maturity and Skills Deep Dive 2021
"""

from numpy import nan

SFIA_skills = ['IRMG', 'SCTY', 'INAN', 'VISL', 'BPRE', 'ARCH', 'DATM', 'BUAN', 'DLMG', 'DESN', 'SWDN', 'PROG', 'RESD', 'ADEV', 'DTAN', 'DBDS', 'TEST', 'HCEV', 'SCMD', 'NUMA', 'HPCC', 'DATS']
        
response_values = {"Strongly Disagree": 0,
                   "Disagree": 1, 
                   "Neither agree nor disagree": 2,
                   "Agree": 3,
                   "Strongly Agree": 4,
                   "Don't Know": nan,
                   "nan": nan}
                
        
def extract_data(field, item):
    """Helper function to extract pandas data
    """
    
    data = item[1:][0]  # Pull out data from tuple
    assert(field.lower() in data[0]) # Check that the right keyword is in the header             
    return(list(data[1:]))  # Return data as a list

    
