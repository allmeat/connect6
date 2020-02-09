import pymysql

db = pymysql.connect(
    host="35.233.179.226",
    port=3306,
    user="root",
    passwd="allmeat",
    db="playground_log",
    charset="utf8",
)

cursor = db.cursor()

query = "INSERT INTO `playground_log`.`TESTTABLE` (`name`, `age`) VALUES ('walter', 34);"
cursor.execute(query)

db.commit()
db.close()

print("insert done")
