from flask import jsonify
from model.roomunavailable import RoomunavailableDAO

class BaseRoomunavailable:
    def build_map_dict(self, row):
        result = {}
        result['ruid'] = row[0]
        result['rid'] = row[1]
        result['startdate'] = row[2]
        result['enddate'] = row[3]
        return result

    def build_attr_dict(self, ruid, rid, startdate, enddate):
        result = {}
        result['ruid'] = ruid
        result['rid'] = rid
        result['startdate'] = startdate
        result['enddate'] = enddate
        return result
    
    def get_all_roomunavailable(self):
        dao = RoomunavailableDAO()
        roomunavailable_list = dao.get_all_roomunavailables()
        result_list = []
        dao.close_connection()
        for row in roomunavailable_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def get_roomunavailable_by_id(self, ruid):
        dao = RoomunavailableDAO()
        roomunavailable_tuple = dao.get_roomunavailable_by_id(ruid)
        dao.close_connection()
        if not roomunavailable_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(roomunavailable_tuple)
            return jsonify(result), 200

    def add_new_roomunavailable(self, json):
        rid = json['rid']
        startdate = json['startdate']
        enddate = json['enddate']
        dao = RoomunavailableDAO()
        ruid = dao.insert_roomunavailable(rid, startdate, enddate)
        result = self.build_attr_dict(ruid, rid, startdate, enddate)
        dao.close_connection()
        return jsonify(result), 201

    def update_roomunavailable(self, json):
        rid = json['rid']
        startdate = json['startdate']
        enddate = json['enddate']
        ruid = json['ruid']
        dao = RoomunavailableDAO()
        dao.update_roomunavailable(ruid, rid, startdate, enddate)
        result = self.build_attr_dict(ruid, rid, startdate, enddate)
        dao.close_connection()
        return jsonify(result), 200

    def delete_roomunavailable(self, ruid):
        dao = RoomunavailableDAO()
        result = dao.delete_roomunavailable(ruid)
        dao.close_connection()
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404