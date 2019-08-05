import psycopg2
conn = None
try:
    # self.conn = psycopg2.connect("dbname='dblp' user='postgres' host='localhost' password='Codechef'")
    conn = psycopg2.connect("dbname='library' user='root' host='localhost' password='abcd'")
    # self.conn = psycopg2.connect("dbname='db_b130974cs' user='postgres' host='localhost' password='Codechef'")
except:
    print ("I am unable to connect to the database")


with open("load_salaries.sql", "r+") as f:
    lines = f.readlines()
