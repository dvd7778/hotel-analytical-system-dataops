from flask import jsonify
from model.hotel import HotelDAO

class BaseHotel:

    def build_map_dict(self, row):
        result = {}
        result['hid'] = row[0]
        result['chid'] = row[1]
        result['hname'] = row[2]
        result['hcity'] = row[3]
        return result

    def build_attr_dict(self, hid, chid, hname, hcity):
        result = {}
        result['hid'] = hid
        result['chid'] = chid
        result['hname'] = hname
        result['hcity'] = hcity
        return result

    def get_all_hotels(self):
        dao = HotelDAO()
        hotel_list = dao.get_All_Hotels()
        result_list = []
        for row in hotel_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        dao.close_connection()
        return jsonify(result_list)

    def get_hotel_by_id(self, hid):
        dao = HotelDAO()
        hotel_tuple = dao.get_Hotel_By_Id(hid)
        dao.close_connection()
        if not hotel_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(hotel_tuple)
            return jsonify(result), 200

    def add_new_hotel(self, json):
        hid = json['hid']
        chid = json['chid'] 
        hname = json['hname']
        hcity = json['hcity']
        dao = HotelDAO()
        hid = dao.insert_Hotel(chid, hname, hcity)
        result = self.build_attr_dict(hid, chid, hname, hcity)
        dao.close_connection()
        return jsonify(result), 201

    def update_hotel(self, json):
        hid = json['hid']
        chid = json['chid'] 
        hname = json['hname']
        hcity = json['hcity'] 
        dao = HotelDAO()
        dao.update_Hotel(hid, chid, hname, hcity)
        result = self.build_attr_dict(hid, chid, hname, hcity)
        dao.close_connection()
        return jsonify(result), 200

    def delete_hotel(self, hid):
        dao = HotelDAO()
        result = dao.delete_Hotel_by_Id(hid)
        dao.close_connection()
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404
    
    # Top 5 hotels with the most client capacity.     
    def top_5_hotels_most_capacity(self):
        dao = HotelDAO()
        result = dao.top_5_hotels_most_capacity()
        result_list = []
        
        for row in result:
            result_list.append({
                'Hotel' : row[0], 
                'Capacity' : row[1]
            })
        
        dao.close_connection()
        return jsonify(result_list)
    
    # Top 10% of the hotels that had the most reservations.
    def top_10_percent_most_reservations(self):
        dao = HotelDAO()
        result = dao.top_10_percent_most_reservations()
        result_list = []
        
        for row in result:
            result_list.append({
                'Hotel' : row[0], 
                'Reservations' : row[1]
            })
        
        dao.close_connection()
        return jsonify(result_list)
    
    # Top 5 handicap rooms that were reserved the most.
    def top_5_most_handicap_reservations(self, hid):
        dao = HotelDAO()
        result = dao.top_5_most_handicap_reservations(hid)
        result_list = []
        
        for row in result:
            result_list.append({
                'Room ID' : row[0], 
                'Reservations' : row[1]
            })
        
        dao.close_connection()
        return jsonify(result_list)
    
    