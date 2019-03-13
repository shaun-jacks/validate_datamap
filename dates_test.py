#### Create a test to check if dates are YYYY-MM-DD ####
import pandas as pd 
import numpy as np 

#### create helper functions ####
## HasTwoDashes ##
def HasTwoDashes(mydate):
    return(mydate.str.count('-') == 2)

## HasTwoSlashes ##
def HasTwoSlashes(mydate):
    return(mydate.str.count('/') == 2)


## IsCharNumber ##
# Checks if my_char could be a number 
def IsCharNumber(my_char):
    assert(my_char.dtype == 'object'), 'my_char must be an object dtype'
    return(my_char.str.contains('[-0123456789\\.]', regex = True))

## character_clean ##
# Cleans characters by blanks to nas and coercing into string dtypes 
# and trimming whitespace
def character_clean(mydate):
    mydate = mydate.replace(r'', np.nan, regex=True)
    mydate = mydate.str.strip()
    return(mydate)

#### Is_YMD_Date ####
def Is_YMD_Date(mydate):
    assert(mydate.dtype == 'object'), 'dtype of mydate must be object'
    mydate = character_clean(mydate)
    # save all missing dates in bool
    missing_dates = mydate.isnull()
    has_two_slashes_dashes = HasTwoDashes(mydate) | HasTwoSlashes(mydate)

    year = mydate.str.replace('^(.*)[-/]{1}(.*)[-/]{1}(.*)$', '\\1', \
         regex = True)
    month = mydate.str.replace('^(.*)[-/]{1}(.*)[-/]{1}(.*)$', '\\2', \
         regex = True)
    day = mydate.str.replace('^(.*)[-/]{1}(.*)[-/]{1}(.*)$', '\\3', \
         regex = True)
    
    has_numbers = IsCharNumber(year) & IsCharNumber(month) & \
        IsCharNumber(day) & has_two_slashes_dashes
    
    string_len_matches = ((year.str.len() == 4) & (month.str.len() == 2) & \
        (day.str.len() == 2))
    
    year = pd.to_numeric(year)
    month = pd.to_numeric(month)
    day = pd.to_numeric(day)

    days_range_match = ((day > 0) & (day < 32))
    months_range_match = ((month > 0) & (month < 13))
    years_range_match = ((year > 0) & (year < 2100))

    val_ranges_match = days_range_match & months_range_match & \
         years_range_match
    
    is_ymd = ((missing_dates) | (has_two_slashes_dashes & has_numbers & \
        string_len_matches & val_ranges_match))
    
    return(is_ymd)





