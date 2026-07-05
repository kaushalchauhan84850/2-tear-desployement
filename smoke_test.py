import boto3,os,sys
import pymysql 
client=boto3.client("ssm",region_name="us-east-1")
params=(
    os.path.basename(p["Name"],p["value"])
    for p in client.get_parameters_by_path(
        path="/application/testing",
        WithDecryption=True)["parameters"]
)
required=["DB_NAME","DB_USER","DB_HOST","DB_PASSWORD","DB_PORT"]
missing=[k for k in required if k not in params]

for k in required:
    print(f"{k} : {"✅" if k in params else '❌'}")
    
    
if missing:
    print(f"Failed : {missing}")
    sys.exit(1)    
    
    
# TO Finf the banking db and show all the tables in it 

try:
    connection=pymysql.connect(
        host=params["DB_HOST"],
        user=params["DB_USER"],
        password=params["DB_PASSWORD"],
        database=params["DB_NAME"],
        port=int(params["DB_PORT"]),
        connect_timeout=10
    )    
    
    cur=connection.cursor()
    cur.execute("SHOW TABLES")
    tables=[row[0] for row in cur.fetchall()]
    connection.close()
    print(f"{params["DB_NAME"]}")
    print(f"table : {tables}")
    
    
except Exception as e:
    print("DB ERROR❌ :" , e)
    sys.exit(1)
    
print("✅ Smoke test Done")    
          
    