import re

# ------------
# phone_number
# ------------

def phone_number (s) :
    return not re.search('^\d\d\d-\d\d\d\d$', s) is None
