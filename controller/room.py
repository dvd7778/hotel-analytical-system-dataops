from flask import jsonify
from model.room import roomDAO

class BaseRoom:

    def build_map_dict(self, row):
        result = {}
        result['rid'] = row[0]
        result['hid'] = row[1]
        result['rdid'] = row[2]
        result['rprice'] = row[3]
        return result

    def build_attr_dict(self, rid, hid, rdid, rprice):
        result = {}
        result['rid'] = rid
        result['hid'] = hid
        result['rdid'] = rdid
        result['rprice'] = rprice
        return result

    def get_all_rooms(self):
        dao = roomDAO()
        room_list = dao.get_All_Rooms()
        result_list = []
        dao.close_connection()
        for row in room_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def get_room_by_id(self, rid):
        dao = roomDAO()
        room_tuple = dao.get_Room_By_Id(rid)
        dao.close_connection()
        if not room_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(room_tuple)
            return jsonify(result), 200

    def add_new_room(self, json):
        rid = json['rid']
        hid = json['hid']
        rdid = json['rdid']
        rprice = json['rprice']
       
        dao = roomDAO()
        rid = dao.insert_Room(hid, rdid, rprice)
        result = self.build_attr_dict(rid, hid, rdid, rprice)
        dao.close_connection()
        return jsonify(result), 201

    def update_room(self, json):
        rid = result['rid']
        hid = result['hid']
        rdid = result['rdid']
        rprice = result['rprice']
        dao = roomDAO()
        dao.update_Room(rid, hid, rdid, rprice)
        result = self.build_attr_dict(rid, hid, rdid, rprice)
        dao.close_connection()
        return jsonify(result), 200

    def delete_room(self, rid):
        dao = roomDAO()
        result = dao.delete_Room_by_Id(rid)
        dao.close_connection()
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404