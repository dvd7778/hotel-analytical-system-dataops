from config.dbconfig import pg_config
import psycopg2

class RoomDescriptionDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='cc3engiv0mo271.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com'" %(pg_config['database'], pg_config['username'],
                                                                  pg_config['pswrd'], pg_config['port_id'])
        print("conection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)
        self.cursor = self.conn.cursor()

    def get_All_RoomDescription(self):
        query = "select * from roomdescription;"
        self.cursor.execute(query)
        result = []
        for row in self.cursor:
            result.append(row)
        return result

    def get_RoomDescription_By_Id(self, rdid):
        query = "select * from roomdescription where rdid = %s;"
        self.cursor.execute(query, (rdid,))
        result = self.cursor.fetchone()
        return result

    def insert_RoomDescription(self, rname, rtype, capacity, ishandicap):
        query = "insert into roomdescription ( rname, rtype, capacity, ishandicap) values (%s,%s,%s,%s) returning rdid;"
        self.cursor.execute(query, (rname, rtype, capacity, ishandicap, ))
        rdid = self.cursor.fetchone()[0]
        self.conn.commit()
        return rdid

    def update_RoomDescription(self, rname, rtype, capacity, ishandicap, rdid):
        query= "update roomdescription set rname = %s, rtype =%s, capacity =%s, ishandicap =%s where rdid=%s;"
        self.cursor.execute(query, (rname, rtype, capacity, ishandicap, rdid))
        self.conn.commit()
        return True

    def delete_RoomDescription_by_Id(self, rdid):
        query = "delete from roomdescription where rdid=%s;"
        self.cursor.execute(query,(rdid,))
        affected_rows = self.cursor.rowcount
        self.conn.commit()
        return affected_rows !=0
    
    def close_connection(self):
        self.cursor.close()
        self.conn.close()