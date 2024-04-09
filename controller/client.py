from flask import jsonify
from model.client import ClientDAO

class BaseClient:
    def build_map_dict(self, row):
        result = {}
        result['clid'] = row[0]
        result['fname'] = row[1]
        result['lname'] = row[2]
        result['age'] = row[3]
        result['memberyear'] = row[4]
        return result

    def build_attr_dict(self, clid, fname, lname, age, memberyear):
        result = {}
        result['clid'] = clid
        result['fname'] = fname
        result['lname'] = lname
        result['age'] = age
        result['memberyear'] = memberyear
        return result
    
    def get_all_clients(self):
        dao = ClientDAO()
        client_list = dao.get_all_clients()
        result_list = []
        for row in client_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        dao.close_connection()
        return jsonify(result_list)

    def get_client_by_id(self, clid):
        dao = ClientDAO()
        client_tuple = dao.get_client_by_id(clid)
        dao.close_connection()
        if not client_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(client_tuple)
            return jsonify(result), 200

    def add_new_client(self, json):
        fname = json['fname']
        lname = json['lname']
        age = json['age']
        memberyear = json['memberyear']
        dao = ClientDAO()
        clid = dao.insert_client(fname, lname, age, memberyear)
        result = self.build_attr_dict(clid, fname, lname, age, memberyear)
        dao.close_connection()
        return jsonify(result), 201

    def update_client(self, json):
        fname = json['fname']
        lname = json['lname']
        age = json['age']
        memberyear = json['memberyear']
        clid = json['clid']
        dao = ClientDAO()
        dao.update_client(clid, fname, lname, age, memberyear)
        result = self.build_attr_dict(clid, fname, lname, age, memberyear)
        dao.close_connection()
        return jsonify(result), 200

    def delete_client(self, clid):
        dao = ClientDAO()
        result = dao.delete_client(clid)
        dao.close_connection()
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404
    
    # Top 5 clients under 30 years old that made the most reservation with a credit card.    
    def top_5_most_creditcard_under_30(self, hid):
        dao = ClientDAO()
        result = dao.top_5_most_creditcard_under_30(hid)
        result_list = []
        
        for row in result:
            result_list.append({
                'Full Name' : row[0], 
                'Credit Card Reservations' : row[1]
            })
        
        dao.close_connection()
        return jsonify(result_list)