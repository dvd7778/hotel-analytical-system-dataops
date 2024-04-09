from config.dbconfig import pg_config
import psycopg2

class EmployeeDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='cc3engiv0mo271.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com'" %(pg_config['database'], pg_config['username'],
                                                                  pg_config['pswrd'], pg_config['port_id'])
        print("conection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)
        self.cursor = self.conn.cursor()

    def get_all_employees(self):
        query = "select * from employee;"
        self.cursor.execute(query)
        result = []
        
        for row in self.cursor:
            result.append(row)
            
        return result
    
    def get_employee_by_id(self, eid):
        query = "select * from employee where eid = %s;"
        self.cursor.execute(query, (eid,))
        
        result = self.cursor.fetchone()
        
        return result
    
    def insert_employee(self, hid, fname, lname, age, salary, position):
        query = "insert into employee (hid, fname, lname, age, salary, position) values (%s,%s,%s,%s,%s,%s) returning eid;"
        self.cursor.execute(query, (hid, fname, lname, age, salary, position,))
        
        eid = self.cursor.fetchone()[0]
        self.conn.commit()
        
        return eid
    
    def update_employee(self, eid, hid, fname, lname, age, salary, position):
        query= "update employee set hid=%s, fname = %s, lname=%s, age =%s salary=%s, position=%s where eid=%s;"
        
        self.cursor.execute(query, (hid, fname, lname, age, salary, position, eid))
        self.conn.commit()
        
        return True
    
    def delete_employee(self, eid):
        query = "delete from employee where eid=%s;"
        self.cursor.execute(query,(eid,))
        
        # determine affected rows
        affected_rows = self.cursor.rowcount
        self.conn.commit()
        
        # if affected rows == 0, the employee was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows !=0
    
    # Validates that the employee is a supervisor
    def supervisor_validation(self, eid):
        query = """SELECT eid FROM employee WHERE eid = %s AND position = 'Supervisor';"""
        self.cursor.execute(query, (eid))
        result = self.cursor.rowcount
        return result
    
    # Validates that the employee is an administrator
    def admin_validation(self, eid):
        query = """SELECT eid FROM employee WHERE eid = %s AND position = 'Administrator';"""
        self.cursor.execute(query, (eid))
        result = self.cursor.rowcount
        return result
    
    # Top 3 highest paid regular employees.
    def highest_paid_regular_employees(self, hid):
        query = """ SELECT CONCAT(fname, ' ', lname) AS "full name", salary
                    FROM employee
                    WHERE position = 'Regular' AND hid = %s
                    GROUP BY eid
                    ORDER BY salary DESC
                    limit 3 """
        self.cursor.execute(query, (hid))
        result = self.cursor.fetchall()
        return result
    
    def close_connection(self):
        self.cursor.close()
        self.conn.close()