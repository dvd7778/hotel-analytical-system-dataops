from config.dbconfig import pg_config
import psycopg2

class HotelDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='cc3engiv0mo271.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com'" %(pg_config['database'], pg_config['username'],
                                                                  pg_config['pswrd'], pg_config['port_id'])
        print("conection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)
        self.cursor = self.conn.cursor()

    def get_All_Hotels(self):
        query = "select * from hotel;"
        self.cursor.execute(query)
        result = []
        for row in self.cursor:
            result.append(row)
        return result

    def get_Hotel_By_Id(self, hid):
        query = "select * from hotel where hid = %s;"
        self.cursor.execute(query, (hid,))
        result = self.cursor.fetchone()
        return result

    def insert_Hotel(self, chid, hname, hcity):
        query = "insert into hotel (chid, hname, hcity) values (%s,%s,%s) returning hid;"
        self.cursor.execute(query, (chid, hname, hcity, ))
        hid = self.cursor.fetchone()[0]
        self.conn.commit()
        return hid

    def update_Hotel(self, hid, chid, hname, hcity):
        query= "update hotel set chid = %s, hname =%s, hcity =%s where hid=%s;"
        self.cursor.execute(query, (chid, hname, hcity, hid))
        self.conn.commit()
        return True

    def delete_Hotel_by_Id(self, hid):
        query = "delete from hotel where hid=%s;"
        self.cursor.execute(query,(hid,))
        affected_rows = self.cursor.rowcount
        self.conn.commit()
        return affected_rows !=0
    
    # Top 5 hotels with the most client capacity. 
    def top_5_hotels_most_capacity(self):
        query = """ SELECT hname as "Hotel", sum(capacity) as "hotel capacity"
                    FROM room NATURAL INNER JOIN hotel NATURAL INNER JOIN roomdescription
                    GROUP BY hname
                    ORDER BY "hotel capacity" DESC
                    limit 5 """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    # Top 10% of the hotels that had the most reservations.
    def top_10_percent_most_reservations(self):
        query = """ SELECT hname as "Hotel", sum(reid) as "Reservations"
                    FROM reserve NATURAL INNER JOIN roomunavailable NATURAL INNER JOIN room NATURAL INNER JOIN hotel NATURAL INNER JOIN roomdescription
                    GROUP BY hname
                    ORDER BY "Reservations" DESC
                    limit (SELECT count(hname) *.10 FROM hotel)"""
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    # Top 5 handicap rooms that were reserved the most.
    def top_5_most_handicap_reservations(self, hid):
        query = """ SELECT rid, COUNT(reid) as Reservations
                    FROM room NATURAL INNER JOIN roomdescription NATURAL INNER JOIN hotel NATURAL INNER JOIN roomunavailable NATURAL INNER JOIN reserve
                    WHERE ishandicap = TRUE AND hid = %s
                    GROUP BY rid
                    ORDER BY Reservations DESC
                    LIMIT 5"""
        self.cursor.execute(query, (hid))
        result = self.cursor.fetchall()
        return result
    
    def close_connection(self):
        self.cursor.close()
        self.conn.close()