from flask import jsonify
from model.reserve import ReserveDAO

class BaseReserve:
    def build_map_dict(self, row):
        result = {}
        result['reid'] = row[0]
        result['ruid'] = row[1]
        result['clid'] = row[2]
        result['total_cost'] = row[3]
        result['payment'] = row[4]
        result['guests'] = row[5]
        return result

    def build_attr_dict(self, reid, ruid, clid, total_cost, payment, guests):
        result = {}
        result['reid'] = reid
        result['ruid'] = ruid
        result['clid'] = clid
        result['total_cost'] = total_cost
        result['payment'] = payment
        result['guests'] = guests
        return result
    
    def get_all_reserve(self):
        dao = ReserveDAO()
        reserve_list = dao.get_all_reserves()
        result_list = []
        for row in reserve_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        dao.close_connection()
        return jsonify(result_list)

    def get_reserve_by_id(self, reid):
        dao = ReserveDAO()
        reserve_tuple = dao.get_reserve_by_id(reid)
        dao.close_connection()
        if not reserve_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(reserve_tuple)
            return jsonify(result), 200

    def add_new_reserve(self, json):
        ruid = json['ruid']
        clid = json['clid']
        total_cost = json['total_cost']
        payment = json['payment']
        guests = json['guests']
        dao = ReserveDAO()
        reid = dao.insert_reserve(ruid, clid, total_cost, payment, guests)
        result = self.build_attr_dict(reid, ruid, clid, total_cost, payment, guests)
        dao.close_connection()
        return jsonify(result), 201

    def update_reserve(self, json):
        ruid = json['ruid']
        clid = json['clid']
        total_cost = json['total_cost']
        payment = json['payment']
        guests = json['guests']
        reid = json['reid']
        dao = ReserveDAO()
        dao.update_reserve(reid, ruid, clid, total_cost, payment, guests)
        result = self.build_attr_dict(reid, ruid, clid, total_cost, payment, guests)
        dao.close_connection()
        return jsonify(result), 200

    def delete_reserve(self, reid):
        dao = ReserveDAO()
        result = dao.delete_reserve(reid)
        dao.close_connection()
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404
    
    # Total reservation percentage by payment method.
    def total_reservations_by_payment(self):
        dao = ReserveDAO()
        result = dao.total_reservations_by_payment()
        result_list = []
        
        for row in result:
            result_list.append({
                'Payment Method' : row[0], 
                'Reservation Percentage' : row[1]
            })
        
        dao.close_connection()
        return jsonify(result_list)