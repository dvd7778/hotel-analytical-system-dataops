from config.dbconfig import pg_config
import psycopg2

class ReserveDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='cc3engiv0mo271.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com'" %(pg_config['database'], pg_config['username'],
                                                                  pg_config['pswrd'], pg_config['port_id'])
        print("conection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)
        self.cursor = self.conn.cursor()

    def get_all_reserves(self):
        query = "select * from reserve;"
        self.cursor.execute(query)
        result = []
        
        for row in self.cursor:
            result.append(row)
            
        return result
    
    def get_reserve_by_id(self, reid):
        query = "select * from reserve where reid = %s;"
        self.cursor.execute(query, (reid,))
        
        result = self.cursor.fetchone()
        
        return result
    
    def insert_reserve(self, ruid, clid, total_cost, payment, guests):
        query = "insert into reserve (ruid, clid, total_cost, payment, guests) values (%s,%s,%s,%s,%s) returning reid;"
        self.cursor.execute(query, (ruid, clid, total_cost, payment, guests,))
        
        reid = self.cursor.fetchone()[0]
        self.conn.commit()
        
        return reid
    
    def update_reserve(self, reid, ruid, clid, total_cost, payment, guests):
        query= "update reserve set ruid=%s, clid = %s, total_cost=%s, payment=%s, guests=%s where reid=%s;"
        
        self.cursor.execute(query, (ruid, clid, total_cost, payment, guests, reid))
        self.conn.commit()
        
        return True
    
    def delete_reserve(self, reid):
        query = "delete from reserve where reid=%s;"
        self.cursor.execute(query,(reid,))
        
        # determine affected rows
        affected_rows = self.cursor.rowcount
        self.conn.commit()
        
        # if affected rows == 0, the reserve was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows !=0
    
    # Total reservation percentage by payment method.
    def total_reservations_by_payment(self):
        query = """ SELECT payment AS "Payment Method", (COUNT(payment) * 100.0) / (SELECT COUNT(*) FROM reserve) AS "Reservation Percentage"
                    FROM reserve
                    GROUP BY payment; """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    def close_connection(self):
        self.cursor.close()
        self.conn.close()