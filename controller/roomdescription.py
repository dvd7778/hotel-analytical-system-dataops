from flask import jsonify
from model.roomdescription import RoomDescriptionDAO

class BaseRoomDescription:
    def build_map_dict(self, row):
        result = {}
        result['rdid'] = row[0]
        result['rname'] = row[1]
        result['rtype'] = row[2]
        result['capacity'] = row[3]
        result['ishandicap'] = row[4]
        return result

    def build_attr_dict(self, rdid, rname, rtype, capacity, ishandicap):
        result = {}
        result['rdid'] = rdid
        result['rname'] = rname
        result['rtype'] = rtype
        result['capacity'] = capacity
        result['ishandicap'] = ishandicap
        return result
    
    def get_all_RoomDescription(self):
        dao = RoomDescriptionDAO()
        RoomDescription_list = dao.get_All_RoomDescription()
        result_list = []
        dao.close_connection()
        for row in RoomDescription_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def get_RoomDescription_by_id(self, rdid):
        dao = RoomDescriptionDAO()
        RoomDescription_tuple = dao.get_RoomDescription_By_Id(rdid)
        dao.close_connection()
        if not RoomDescription_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(RoomDescription_tuple)
            return jsonify(result), 200

    def add_new_RoomDescription(self, json):
        rname = json['rname']
        rtype = json['rtype']
        capacity = json['capacity']
        ishandicap = json['ishandicap']
        dao = RoomDescriptionDAO()
        rdid = dao.insert_RoomDescription(rname, rtype, capacity, ishandicap)
        result = self.build_attr_dict(rdid, rname, rtype, capacity, ishandicap)
        dao.close_connection()
        return jsonify(result), 201

    def update_RoomDescription(self, json):
        rname = json['rname']
        rtype = json['rtype']
        capacity = json['capacity']
        ishandicap = json['ishandicap']
        rdid = json['rdid']
        dao = RoomDescriptionDAO()
        dao.update_RoomDescription(rdid, rname, rtype, capacity, ishandicap)
        result = self.build_attr_dict(rdid, rname, rtype, capacity, ishandicap)
        dao.close_connection()
        return jsonify(result), 200

    def delete_RoomDescription(self, rdid):
        dao = RoomDescriptionDAO()
        result = dao.delete_RoomDescription_by_Id(rdid)
        dao.close_connection()
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404
