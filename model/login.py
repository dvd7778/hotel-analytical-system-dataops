from config.dbconfig import pg_config
import psycopg2

class loginDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='cc3engiv0mo271.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com'" %(pg_config['database'], pg_config['username'],
                                                                  pg_config['pswrd'], pg_config['port_id'])
        print("conection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)
        self.cursor = self.conn.cursor()

    def get_All_logins(self):
        query = "select * from login;"
        self.cursor.execute(query)
        result = []
        for row in self.cursor:
            result.append(row)
        return result

    def get_login_By_Id(self, lid):
        query = "select * from login where lid = %s;"
        self.cursor.execute(query, (lid,))
        result = self.cursor.fetchone()
        return result

    def insert_login(self, eid, username, password):
        query = "insert into login (eid, username, password) values (%s,%s,%s) returning lid;"
        self.cursor.execute(query, (eid, username, password, ))
        lid = self.cursor.fetchone()[0]
        self.conn.commit()
        return lid

    def update_login(self, eid, username, password, lid):
        query= "update room set eid = %s, username =%s, password =%s where lid=%s;"
        self.cursor.execute(query, (eid, username, password, lid))
        self.conn.commit()
        return True

    def delete_login_by_Id(self, lid):
        query = "delete from login where lid=%s;"
        self.cursor.execute(query,(lid,))
        affected_rows = self.cursor.rowcount
        self.conn.commit()
        return affected_rows !=0
    
    def close_connection(self):
        self.cursor.close()
        self.conn.close()