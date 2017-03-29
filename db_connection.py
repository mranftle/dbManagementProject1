'''
Connects to the Postgres DB and performs analysis/plots on graph

Download Secure Pipes

new local forward
server address: shell.cec.wustl.edu, port: 22
ssh username, ssh password
bind address *, port 80 (or w.e is open/set below)
host address 128.252.167.175 port 5432



'''
import psycopg2 as pgres
import pandas as pd

forward_port = 80
# create database connection
conn = pgres.connect(database="ranftleoser_project1", \
                     # user=USERNAME
                     #  password=PASSWORD, \
                     host="localhost", \
                     port=forward_port)
cur = conn.cursor()

# happiness vs number of terrorist attacks
# sql = "select * from cummulative_happiness"
# cur.execute(sql)
# cumm_happiness = pd.DataFrame(cur.fetchall(), columns = ['Country', 'Attacks', 'Happiness Rank', 'Happiness Score'])
# print cumm_happiness.sort(['Attacks', 'Happiness Rank'], ascending = False)
# print cumm_happiness[['Attacks', 'Happiness Rank', 'Happiness Score']].corr('pearson')

# attack type vs freedom / trust
sql = "select * from attack_targets_happiness " \
      "where targtype1 = 'Government (Diplomatic)'"
cur.execute(sql)
attack_targ_happiness= pd.DataFrame(cur.fetchall(), columns=['Country', 'Targ Type', 'Attacks', 'Trust', 'Freedom'])
print attack_targ_happiness[['Attacks','Trust', 'Freedom']].corr('pearson')
#
