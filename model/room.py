from config.dbconfig import pg_config
import psycopg2

class roomDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='cc3engiv0mo271.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com'" %(pg_config['database'], pg_config['username'],
                                                                  pg_config['pswrd'], pg_config['port_id'])
        print("conection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)
        self.cursor = self.conn.cursor()

    def get_All_Rooms(self):
        query = "select * from room;"
        self.cursor.execute(query)
        result = []
        for row in self.cursor:
            result.append(row)
        return result

    def get_Room_By_Id(self, rid):
        query = "select * from room where rid = %s;"
        self.cursor.execute(query, (rid,))
        result = self.cursor.fetchone()
        return result

    def insert_Room(self, hid, rdid, rprice):
        query = "insert into room (hid, rdid, rprice) values %s,%s,%s) returning rid;"
        self.cursor.execute(query, (hid, rdid, rprice, ))
        rid = self.cursor.fetchone()[0]
        self.conn.commit()
        return rid

    def update_Room(self, rid, hid, rdid, rprice):
        query= "update room set hid = %s, rdid =%s, rprice =%s where rid=%s;"
        self.cursor.execute(query, (hid, rdid, rprice, rid))
        self.conn.commit()
        return True

    def delete_Room_by_Id(self, rid):
        query = "delete from room where rid=%s;"
        self.cursor.execute(query,(rid,))
        affected_rows = self.cursor.rowcount
        self.conn.commit()
        return affected_rows !=0
    
    def close_connection(self):
        self.cursor.close()
        self.conn.close()