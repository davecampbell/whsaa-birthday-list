# this python script does the following:
# - accesses and logs into the MembershipWorks site
# - navigates to the Members admin area
# - goes to Export, then selects all fields
# - downloads the CSV to a local file
# - opens that CSV file and reads into a pandas dataframe
# - filters that file for the following:
# - remove deceased alumni entries
# - remove rows with empty birthday or month
# - replaces blank graduation year with a space
# - creates a json output file of just the required columns

from helium import *
import pandas as pd
import os
import glob
import time
from dotenv import load_dotenv

load_dotenv()
MW_USER = os.getenv("MW_USER")
MW_PASS = os.getenv("MW_PASS")

# login to MW and download all fields for all members
start_chrome('https://membershipworks.com/admin/#folder/Members', headless=True)
write(MW_USER, into='Email')
write(MW_PASS, into='Password')
click('Sign In')

click(Link('Export'))

click(Button('click here to select all fields'))
click(Button('Download'))

print("file is downloading...")

# wait about 10 seconds to be sure the file is saved prop
time.sleep(10)

# the file downloaded to the default download directory for the browser (~/Downloads)
# with a name of 'export.csv'.  if there was one there already, it makes a number
# like 'export (4).csv'

# find the most recent file in the ~/Downloads folder

def find_most_recent_file(folder_path):
    # Expand `~` to the user's home directory
    expanded_path = os.path.expanduser(folder_path)
    
    # Get all files in the folder
    files = glob.glob(os.path.join(expanded_path, "*"))
    
    if not files:
        print("No files found in the specified folder.")
        return None
    
    # Find the most recent file
    most_recent_file = max(files, key=os.path.getmtime)
    
    return most_recent_file

# Specify the Downloads folder
downloads_folder = "~/Downloads"

# Find and print the most recent file
most_recent_file = find_most_recent_file(downloads_folder)
if most_recent_file:
    print(f"The most recent file is: {most_recent_file}")

# open that file into a dataframe
file_path = most_recent_file
df = pd.read_csv(file_path)

# keep named columns
columns_to_keep = ['Account Name', 'Account ID', 'Deceased', 'Graduation Year', 'Birthday Month', 'Birthday Day']  # Replace with the column names to keep
df = df[columns_to_keep]

# Delete rows for deceased alumni
values_to_remove = ['Y']
df = df[~df['Deceased'].isin(values_to_remove)]

# Delete specific columns
columns_to_delete = ['Deceased']
df = df.drop(columns=columns_to_delete, errors='ignore')

# Keep rows where Birthday date info is not null
df = df[df['Birthday Month'].notnull()]
df = df[df['Birthday Day'].notnull()]

# fill the null / Nan in Graduation Year with a space
df['Graduation Year'] = df['Graduation Year'].fillna(' ')

# Rename specific columns
df = df.rename(columns={'Account Name': 'name', 'Account ID': 'id', 'Graduation Year': 'gradYear', 'Birthday Month': 'birthMonth', 'Birthday Day': 'birthDay'})

# save to a json file
save_file = downloads_folder + '/all-names-birthday-id.json'
df.to_json(save_file, orient='records', index=False, indent=4)

