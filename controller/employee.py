from flask import jsonify
from model.employee import EmployeeDAO

class BaseEmployee:
    def build_map_dict(self, row):
        result = {}
        result['eid'] = row[0]
        result['hid'] = row[1]
        result['fname'] = row[2]
        result['lname'] = row[3]
        result['age'] = row[4]
        result['salary'] = row[5]
        result['position'] = row[6]
        return result

    def build_attr_dict(self, eid, hid, fname, lname, age, salary, position):
        result = {}
        result['eid'] = eid
        result['hid'] = hid
        result['fname'] = fname
        result['lname'] = lname
        result['age'] = age
        result['salary'] = salary
        result['position'] = position
        return result
    
    def get_all_employee(self):
        dao = EmployeeDAO()
        employee_list = dao.get_all_employees()
        result_list = []
        for row in employee_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        dao.close_connection()
        return jsonify(result_list)

    def get_employee_by_id(self, eid):
        dao = EmployeeDAO()
        employee_tuple = dao.get_employee_by_id(eid)
        dao.close_connection()
        if not employee_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(employee_tuple)
            return jsonify(result), 200

    def add_new_employee(self, json):
        hid = json['hid']
        fname = json['fname']
        lname = json['lname']
        age = json['age']
        salary = json['salary']
        position = json['position']
        dao = EmployeeDAO()
        eid = dao.insert_employee(hid, fname, lname, age, salary, position)
        result = self.build_attr_dict(eid, hid, fname, lname, age, salary, position)
        dao.close_connection()
        return jsonify(result), 201

    def update_employee(self, json):
        hid = json['hid']
        fname = json['fname']
        lname = json['lname']
        age = json['age']
        salary = json['salary']
        eid = json['eid']
        position = json['position']
        dao = EmployeeDAO()
        dao.update_employee(eid, hid, fname, lname, age, salary, position)
        result = self.build_attr_dict(eid, hid, fname, lname, age, salary, position)
        dao.close_connection()
        return jsonify(result), 200

    def delete_employee(self, eid):
        dao = EmployeeDAO()
        result = dao.delete_employee(eid)
        dao.close_connection()
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404

    # Validates that the employee is a supervisor
    def supervisor_validation(self, eid):
        dao = EmployeeDAO()
        result = dao.supervisor_validation(eid)
        dao.close_connection()
        if result:
            return True
        else:
            return False
    
    # Validates that the employee is an administrator
    def admin_validation(self, eid):
        dao = EmployeeDAO()
        result = dao.supervisor_validation(eid)
        dao.close_connection()
        if result:
            return True
        else:
            return False
    
    # Top 3 highest paid regular employees.    
    def highest_paid_regular_employees(self, hid):
        dao = EmployeeDAO()
        result = dao.highest_paid_regular_employees(hid)
        result_list = []
        
        for row in result:
            result_list.append({
                'Employee Name' : row[0], 
                'Salary' : row[1]
            })
        
        dao.close_connection()
        return jsonify(result_list)