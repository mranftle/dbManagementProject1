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

forward_port = 80
# create database connection
conn = pgres.connect(database="ranftleoser_project1", \
                     user="matthew.ranftle", \
                     # password=PASSWORD, \
                     host="localhost", \
                     port=forward_port)
cur = conn.cursor()

sql = "select * from cummulative_happiness"
cur.execute(sql)
res = cur.fetchall()

print res

