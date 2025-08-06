import pymysql

try:
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='Hacker!@#123123',
        database='mobile_app_backend',
        port=3306
    )
    print("✅ Direct MySQL connection successful!")
    connection.close()
except Exception as e:
    print(f"❌ MySQL connection failed: {e}")