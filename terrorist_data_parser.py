import pandas as pd

''' script for parsing, cleaning and organizing terrorist attack data into .csv files
    Matthew Ranftle, Alex Oser
    CSE 530 Project 1
'''
terr_data = pd.read_csv('data/terrorist_data.csv', dtype={'eventid':object})

attack_cols = ['eventid', \
               'iyear', 'imonth', 'iday', \
               'country_txt', 'region_txt', 'city',\
               'gname', 'gsubname', 'claimed', 'nperps', \
               'weaptype1_txt', 'attacktype1_txt', 'motive']

outcome_cols= ['eventid', \
                'success', 'suicide', \
                'nkill','nwound', 'propvalue']

victim_cols = ['eventid', \
                'targtype1_txt', 'targsubtype1_txt', \
                'corp1', 'target1', 'natlty1_txt']

attacks = terr_data[attack_cols].copy().fillna(0)
outcomes = terr_data[outcome_cols].copy().fillna(0)
victims = terr_data[victim_cols].copy()

attacks[['claimed', 'nperps']] = attacks[['claimed', 'nperps']].astype(int)
outcomes[['nkill', 'nwound', 'propvalue']] = outcomes[['nkill', 'nwound', 'propvalue']].astype(int)

attacks.to_csv('data/attacks.csv', index=False, sep='\t')
victims.to_csv('data/victims.csv', index=False, sep='\t')
outcomes.to_csv('data/outcomes.csv', index=False, sep='\t')
