from config.dbconfig import pg_config
import psycopg2

class ChainsDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='cc3engiv0mo271.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com'" %(pg_config['database'], pg_config['username'],
                                                                  pg_config['pswrd'], pg_config['port_id'])
        print("conection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)
        self.cursor = self.conn.cursor()

    def get_all_chains(self):
        query = "select * from chains;"
        self.cursor.execute(query)
        result = []
        
        for row in self.cursor:
            result.append(row)
            
        return result
    
    def get_chains_by_id(self, chid):
        query = "select * from chains where chid = %s;"
        self.cursor.execute(query, (chid,))
        
        result = self.cursor.fetchone()
        
        return result
    
    def insert_chains(self, cname, springmkup, summermkup, fallmkup, wintermkup):
        query = "insert into chains (cname, springmkup, summermkup, fallmkup, wintermkup) values (%s,%s,%s,%s,%s) returning chid;"
        self.cursor.execute(query, (cname, springmkup, summermkup, fallmkup, wintermkup,))
        
        reid = self.cursor.fetchone()[0]
        self.conn.commit()
        
        return reid
    
    def update_chains(self, chid, cname, springmkup, summermkup, fallmkup, wintermkup):
        query= "update chains set cname=%s, springmkup = %s, summermkup=%s, fallmkup=%s, wintermkup=%s where chid=%s;"
        
        self.cursor.execute(query, (cname, springmkup, summermkup, fallmkup, wintermkup, chid))
        self.conn.commit()
        
        return True
    
    def delete_chains(self, chid):
        query = "delete from chains where chid=%s;"
        self.cursor.execute(query,(chid,))
        
        # determine affected rows
        affected_rows = self.cursor.rowcount
        self.conn.commit()
        
        # if affected rows == 0, the chain was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows !=0
    
    # Top 3 chains with the highest total revenue.
    def top_3_chains_by_total_revenue(self):
        query = """ SELECT  chid, cname, sum(total_cost) as revenue
                    FROM reserve NATURAL INNER JOIN roomunavailable NATURAL INNER JOIN room NATURAL INNER JOIN hotel NATURAL INNER JOIN chains
                    GROUP BY cname, chid
                    ORDER BY revenue DESC
                    limit 3 """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    # Top 3 chains with the least rooms.
    def top_3_chains_with_least_rooms(self):
        query = """ SELECT cname as "Chain", count(rid) as "rooms available"
                    FROM room NATURAL INNER JOIN hotel NATURAL INNER JOIN chains
                    GROUP BY cname
                    ORDER BY "rooms available" ASC
                    limit 3 """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    def close_connection(self):
        self.cursor.close()
        self.conn.close()