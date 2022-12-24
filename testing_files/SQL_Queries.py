# Importing the engine
import pandas as pd
from sqlalchemy import create_engine
import pymysql
# Dialect for the Url
import sql_connector_key.key as key

# connector Url to the MySQL database
k = key.Key()

engine = create_engine(k.this_is_key())
conn = engine.connect()


d = {'day_id': ['2022-12-21', '2022-12-22', '2022-12-23', '2022-12-24'], 'money': [965, 1927, 1876, 1849]}
df = pd.DataFrame(data=d)
df.to_sql('budget', con=conn, if_exists='append', index= False)
pt = engine.execute("SELECT * FROM budget").fetchall()

print(pt)