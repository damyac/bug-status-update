# Author: Da'Mya Campbell (damycamp@cisco.com) 
# File: testcounts.py
# Date: June 2018 (c) Cisco Systems
# Description: Compares lists of bug ids and determines if some have been added or deleted then emails owner about the changes.

import re
import smtplib
#from settings import SENDER_EMAIL, SENDER_PASSWORD

name = "Da'Mya"

# email template for bugs added
ADDED_MSG = """
Hi {},

New bugs have been discovered. Below are the ids of said bugs.
Added: {}

Thanks,
UnifiedPerformance
"""
# email template for bugs deleted
DELETED_MSG = """
Hi {},

Bugs have been removed. Below are the ids of said bugs.
Deleted: {}

Thanks,
UnifiedPerformance
"""

# email template for no bugs present
NOID_MSG = """
Hi {},

There were no bug ids found. Please look into it.

Thanks,
UnifiedPerformance
"""
def create_email_msg(SENDER_EMAIL, SENDER_PASSWORD):
    file = open('bugids.txt')
    list_one = []
    for line in file:
        line = line.rstrip()
        # check to see if id resembles a CDETS
        match = re.search(r'CSC[a-z][a-z]\d+', line)
        if match:
            list_one.append(match.group())
        baseline = set(list_one)

    file_two = open('bugids2.txt') # bug ids were deleted
    list_two = []
    for line in file_two:
        line = line.rstrip()
        # check to see if id resembles a CDETS
        match = re.search(r'CSC[a-z][a-z]\d+', line)
        if match:
            list_two.append(match.group())
    day_two = set(list_two)

    # compare the two sets and determine what email needs to be sent out
    if baseline.difference(day_two):
        subject = 'CDETS Status - Delete Bug Ids' 
        ids = baseline.difference(day_two)
        msg = DELETED_MSG.format(name, ids)
    elif day_two.difference(baseline):
            subject = 'CDETS Status - Added Bug Ids'
            ids = day_two.difference(baseline)
            msg = ADDED_MSG.format(name, ids)
    else:
            subject = 'CDETS Status - No Bug Ids'
            msg = NOID_MSG.format(name)
    email_msg = "Subject: {} \n\n{}".format(subject, msg)
    return email_msg

if __name__ == '__main__':
    SENDER_EMAIL = input('Email address: ')
    SENDER_PASSWORD = input('Password: ')
    email_to = ['damycamp@cisco.com']
    email_msg = create_email_msg(SENDER_EMAIL, SENDER_PASSWORD)

    with smtplib.SMTP('outbound.cisco.com') as smtp:
        smtp.ehlo()
        # put smtp in TLS mode to encrypt following commands
        smtp.starttls()
        smtp.ehlo() 
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.sendmail(SENDER_EMAIL, email_to, email_msg)
        smtp.quit()
    print('Email has been sent successfully')