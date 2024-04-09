from config.dbconfig import pg_config
import psycopg2

class ClientDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='cc3engiv0mo271.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com'" %(pg_config['database'], pg_config['username'],
                                                                  pg_config['pswrd'], pg_config['port_id'])
        print("conection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)
        self.cursor = self.conn.cursor()

    def get_all_clients(self):
        query = "select * from client;"
        self.cursor.execute(query)
        result = []
        
        for row in self.cursor:
            result.append(row)
            
        return result
    
    def get_client_by_id(self, clid):
        query = "select * from client where clid = %s;"
        self.cursor.execute(query, (clid,))
        
        result = self.cursor.fetchone()
        
        return result
    
    def insert_client(self, fname, lname, age, memberyear):
        query = "insert into client (fname, lname, age, memberyear) values (%s,%s,%s,%s) returning clid;"
        self.cursor.execute(query, (fname, lname, age, memberyear,))
        
        clid = self.cursor.fetchone()[0]
        self.conn.commit()
        
        return clid
    
    def update_client(self, clid, fname, lname, age, memberyear):
        query= "update client set fname=%s, lname = %s, age=%s, memberyear =%s where clid=%s;"
        
        self.cursor.execute(query, (fname, lname, age, memberyear, clid))
        self.conn.commit()
        
        return True
    
    def delete_client(self, clid):
        query = "delete from client where clid=%s;"
        self.cursor.execute(query,(clid,))
        
        # determine affected rows
        affected_rows = self.cursor.rowcount
        self.conn.commit()
        
        # if affected rows == 0, the client was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows !=0
    
    # Top 5 clients under 30 years old that made the most reservation with a credit card.
    def top_5_most_creditcard_under_30(self, hid):
        query = """ SELECT CONCAT(fname, ' ', lname) AS "full name", count(clid) as "Reservations"
                    FROM client NATURAL INNER JOIN reserve NATURAL INNER JOIN roomunavailable NATURAL INNER JOIN room
                    WHERE age < 30 AND payment = 'credit card' AND hid = %s
                    GROUP BY "full name"
                    order by "Reservations" DESC
                    limit 5 """
        self.cursor.execute(query, (hid))
        result = self.cursor.fetchall()
        return result
    
    def close_connection(self):
        self.cursor.close()
        self.conn.close()