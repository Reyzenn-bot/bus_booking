import pymysql
def connectDB():
    return pymysql.connect(
        host='localhost',
        user='root',
        database='bus_booking_db',
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )

connect=connectDB()
if connect:
    print("Database connected successfully")