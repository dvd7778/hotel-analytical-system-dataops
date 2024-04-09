from flask import jsonify
from model.login import loginDAO

class BaseLogin:

    def build_map_dict(self, row):
        result = {}
        result['lid'] = row[0]
        result['eid'] = row[1]
        result['username'] = row[2]
        result['password'] = row[3]
        return result

    def build_attr_dict(self, lid, eid, username, password):
        result = {}
        result['lid'] = lid
        result['eid'] = eid
        result['username'] = username
        result['password'] = password
        return result

    def get_all_logins(self):
        dao = loginDAO()
        login_list = dao.get_All_logins()
        result_list = []
        for row in login_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        dao.close_connection()
        return jsonify(result_list)

    def get_login_by_id(self, lid):
        dao = loginDAO()
        login_tuple = dao.get_login_By_Id(lid)
        dao.close_connection()
        if not login_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(login_tuple)
            return jsonify(result), 200

    def add_new_login(self, json):
        lid = json['lid']
        eid = json['eid'] 
        username = json['username'] 
        password = json['password'] 
        dao = loginDAO()
        lid = dao.insert_login(eid, username, password)
        result = self.build_attr_dict(lid, eid, username, password)
        dao.close_connection()
        return jsonify(result), 201

    def update_login(self, json):
        lid = json['lid']
        eid = json['eid'] 
        username = json['username'] 
        password = json['password'] 
        dao = loginDAO()
        dao.update_login(lid, eid, username, password)
        result = self.build_attr_dict(lid, eid, username, password)
        dao.close_connection()
        return jsonify(result), 200

    def delete_login(self, lid):
        dao = loginDAO()
        result = dao.delete_login_by_Id(lid)
        dao.close_connection()
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404