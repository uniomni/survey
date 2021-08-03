"""Auxiliary functions and definitions for extracting and analysing skills
   from GA Digital Science Maturity and Skills Deep Dive 2021
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

response_values = {"Strongly Disagree": -2,
                   "Disagree": -1,
                   "Neither agree nor disagree": 0,
                   "Agree": 1,
                   "Strongly Agree": 2,
                   "Don't Know": nan,
                   "nan": nan}  # IEEE value for Not A Number


def extract_data(field, item):
    """Helper function to extract pandas data
    """

    data = item[1:][0]  # Pull out data from tuple

    # Check that the right keyword is in the header
    msg = 'Did not find expected keyword %s in %s' % (field, data[0])
    assert field.lower() in data[0], msg

    return(list(data[1:]))  # Return data as a list


def sort_dictionary_by_value(D):
    """Sort dictionary of the form key: value
    """

    # Sort skills by gap (Schwarzian Transform)
    L = [(x[1], x) for x in D.items()]
    L.sort()
    return([(x[1][0], x[1][1]) for x in L])


def print_sorted_skills(data, label='value'):
    """Print out the skills sorted by the processed values
    """

    header = 'Skills sorted by average %s:' % label
    line = '-'*len(header)

    print()
    print(line)
    print(header)
    print(line)

    L = sort_dictionary_by_value(data)
    for item in L[::-1]:  # Reverse order
        skill = item[0]
        weight = item[1]
        print('%.2f: %s (%s)' % (weight, SFIA_skills[skill], skill))
