
# coding: utf-8
# # Prepare Flood Events data for DB
# In[1]:

import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

#from db_scripts.main_db_script import data_dir, db_filename
import pandas as pd

#import sqlite3
# ### Read in the data


def Main(in_file,out_file,out_dir):

	cds = pd.read_csv(in_file)

	# ### Index by location name and subset to just columns we want

	cds = cds[['location', 'event', 'eventType', 'dt']]
	cds
	event_dates = cds.event.str.extract(r'(\d*/\d*/\d*)', expand=False)
	event_names = cds.event.str.replace(r'(\(\d*/\d*/\d*)\)', '')
	cds['event_name'] = event_names
	cds['event_date'] = pd.to_datetime(event_dates)
	event_date_str = cds['event_date'].dt.strftime('%Y-%m-%d').str.replace('/', '-')
	cds['dt'] = pd.to_datetime(cds['dt'])
	cds['dates'] = cds['dt'].dt.strftime('%Y-%m-%d')
	cds['event_name'] = event_names.str.strip()+ '-' + event_date_str
	del cds['event']
	cds

	# In[14]:
	# con = sqlite3.connect(db_filename)
	# cds.to_sql(con=con, name="flood_events", if_exists="replace")

	cds.to_csv(os.path.join(out_dir, out_file))
	cds.set_index('event_name')

if __name__=='__main__':


    import argparse
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-I", "--in_file",
                        required=True,
                        default=None,
                        help="Path to target CSV file")
                        
    parser.add_argument("-O", "--out_file",
                        required=False,
                        default='flood_events.csv',
                        help="out_file")

    parser.add_argument("-d", "--Path_to_out_Dir",
                        required=False,
                        default=os.getcwd(),
                        help="out file directory")
                       
    args = parser.parse_args()


    Main(args.in_file,args.out_file,args.Path_to_out_Dir)

