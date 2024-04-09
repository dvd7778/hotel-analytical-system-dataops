from config.dbconfig import pg_config
import psycopg2

class RoomunavailableDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='cc3engiv0mo271.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com'" %(pg_config['database'], pg_config['username'],
                                                                  pg_config['pswrd'], pg_config['port_id'])
        print("conection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)
        self.cursor = self.conn.cursor()

    def get_all_roomunavailables(self):
        query = "select * from roomunavailable;"
        self.cursor.execute(query)
        result = []
        
        for row in self.cursor:
            result.append(row)
            
        return result
    
    def get_roomunavailable_by_id(self, clid):
        query = "select * from roomunavailable where ruid = %s;"
        self.cursor.execute(query, (clid,))
        
        result = self.cursor.fetchone()
        
        return result
    
    def insert_roomunavailable(self, rid, startdate, enddate):
        query = "insert into client (rid, startdate, enddate) values (%s,%s,%s) returning ruid;"
        self.cursor.execute(query, (rid, startdate, enddate,))
        
        clid = self.cursor.fetchone()[0]
        self.conn.commit()
        
        return clid
    
    def update_roomunavailable(self, ruid, rid, startdate, enddate):
        query= "update client set rid=%s, startdate = %s, enddate=%s where ruid=%s;"
        
        self.cursor.execute(query, (rid, startdate, enddate, ruid))
        self.conn.commit()
        
        return True
    
    def delete_roomunavailable(self, ruid):
        query = "delete from roomunavailable where ruid=%s;"
        self.cursor.execute(query,(ruid,))
        
        # determine affected rows
        affected_rows = self.cursor.rowcount
        self.conn.commit()
        
        # if affected rows == 0, the roomunavailable was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows !=0
    
    def close_connection(self):
        self.cursor.close()
        self.conn.close()