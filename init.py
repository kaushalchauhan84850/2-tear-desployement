import boto3
import os
import sys
import pymysql

client=boto3.client("ssm" , region_name="us-east-1")
def get_param(name):
    return client.get_parameters(
        name=f"/application/testing/{name}",
        WithDecryption=True)["Parameter"]["Value"]
    
    
try:
    conn=pymysql.connect(
        host=get_param("DB_HOST"),
        user=get_param("DB_USER"),
        password=get_param("DB_PASSWORD"),
        database=get_param("DB_NAME"),
        port=int(get_param("DB_PORT")),
        connect_timeout=10
    )
    
    cur=conn.cursor()
    
    Base_dir=os.path.dirname(os.abspath(__file__))
    sql_file=os.path.join(Base_dir,"init.py")
    
    with open(sql_file,"r",encoding="utf=8") as f:
        sql=f.read()
    
    
    for statment in sql.split(";"):
        statment=statment.strip()
        if statment:
            cur.execute(statment)
            
    conn.commit()
    print("✅ Database conneted successfull")
    
    
except Exception as e:
    print("Error :" , e)
finally:
    conn.close()