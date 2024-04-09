from flask import jsonify
from model.chains import ChainsDAO

class BaseChains:
    def build_map_dict(self, row):
        result = {}
        result['chid'] = row[0]
        result['cname'] = row[1]
        result['springmkup'] = row[2]
        result['summermkup'] = row[3]
        result['fallmkup'] = row[4]
        result['wintermkup'] = row[5]
        return result

    def build_attr_dict(self, chid, cname, springmkup, summermkup, fallmkup, wintermkup):
        result = {}
        result['chid'] = chid
        result['cname'] = cname
        result['springmkup'] = springmkup
        result['summermkup'] = summermkup
        result['fallmkup'] = fallmkup
        result['wintermkup'] = wintermkup
        return result
    
    def get_all_chains(self):
        dao = ChainsDAO()
        chains_list = dao.get_all_chains()
        result_list = []
        dao.close_connection()
        for row in chains_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def get_chains_by_id(self, chid):
        dao = ChainsDAO()
        chains_tuple = dao.get_chains_by_id(chid)
        dao.close_connection()
        if not chains_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(chains_tuple)
            return jsonify(result), 200

    def add_new_chains(self, json):
        cname = json['cname']
        springmkup = json['springmkup']
        summermkup = json['summermkup']
        fallmkup = json['fallmkup']
        wintermkup = json['wintermkup']
        dao = ChainsDAO()
        chid = dao.insert_chains(cname, springmkup, summermkup, fallmkup, wintermkup)
        dao.close_connection()
        result = self.build_attr_dict(chid, cname, springmkup, summermkup, fallmkup, wintermkup)
        return jsonify(result), 201

    def update_chains(self, json):
        cname = json['cname']
        springmkup = json['springmkup']
        summermkup = json['summermkup']
        fallmkup = json['fallmkup']
        wintermkup = json['wintermkup']
        chid = json['chid']
        dao = ChainsDAO()
        dao.update_chains(chid, cname, springmkup, summermkup, fallmkup, wintermkup)
        dao.close_connection()
        result = self.build_attr_dict(chid, cname, springmkup, summermkup, fallmkup, wintermkup)
        return jsonify(result), 200

    def delete_chains(self, chid):
        dao = ChainsDAO()
        result = dao.delete_chains(chid)
        dao.close_connection()
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404
    
    # Top 3 chains with the highest total revenue.    
    def top_3_chains_by_total_revenue(self):
        dao = ChainsDAO()
        result = dao.top_3_chains_by_total_revenue()
        result_list = []
        
        for row in result:
            result_list.append({
                'Chain' : row[0], 
                'Revenue' : row[1]
            })
        
        dao.close_connection()
        return jsonify(result_list)
    
    # Top 3 chains with the least rooms.
    def top_3_chains_with_least_rooms(self):
        dao = ChainsDAO()
        result = dao.top_3_chains_with_least_rooms()
        result_list = []
        
        for row in result:
            result_list.append({
                'Chain' : row[0], 
                'Rooms Available' : row[1]
            })
        
        dao.close_connection()
        return jsonify(result_list)