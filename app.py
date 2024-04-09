from flask import Flask, request, jsonify
from flask_cors import CORS
from controller.chains import BaseChains
from controller.client import BaseClient
from controller.employee import BaseEmployee
from controller.hotel import BaseHotel
from controller.login import BaseLogin
from controller.reserve import BaseReserve
from controller.room import BaseRoom
from controller.roomdescription import BaseRoomDescription
from controller.roomunavailable import BaseRoomunavailable

app = Flask(__name__)
#apply CORS
CORS(app)

@app.route('/')
def home():
    return 'Hello World!'


################################################ CRUD #####################################################

# Chains
@app.route('/dataops/chains', methods=['GET', 'POST'])
def handle_chains():
    if request.method == 'POST':
        return BaseChains().add_new_chains(request.json)
    else:
        return BaseChains().get_all_chains()

@app.route('/dataops/chains/<int:chid>', methods=['GET', 'PUT', 'DELETE'])
def handle_chain_by_id(chid):
    if request.method == 'GET':
        return BaseChains().get_chains_by_id(chid)
    elif request.method == 'PUT':
        return BaseChains().update_chains(request.json)
    elif request.method == 'DELETE':
        return BaseChains().delete_chains(chid)
    else:
        return jsonify("Method Not Allowed"), 405

# Client
@app.route('/dataops/client', methods=['GET', 'POST'])
def handle_client():
    if request.method == 'POST':
        return BaseClient().add_new_client(request.json)
    else:
        return BaseClient().get_all_clients()

@app.route('/dataops/client/<int:cid>', methods=['GET', 'PUT', 'DELETE'])
def handle_client_by_id(cid):
    if request.method == 'GET':
        return BaseClient().get_client_by_id(cid)
    elif  request.method == 'PUT':
        return BaseClient().update_client(request.json)
    elif request.method == 'DELETE':
        return BaseClient().delete_client(cid)
    else:
        return jsonify("Method Not Allowed"), 405
    
# Employee
@app.route('/dataops/employee', methods=['GET', 'POST'])
def handle_employee():
    if request.method == 'POST':
        return BaseEmployee().add_new_employee(request.json)
    else:
        return BaseEmployee().get_all_employee()

@app.route('/dataops/employee/<int:eid>', methods=['GET', 'PUT', 'DELETE'])
def handle_employee_by_id(eid):
    if request.method == 'GET':
        return BaseEmployee().get_employee_by_id(eid)
    elif  request.method == 'PUT':
        return BaseEmployee().update_employee(request.json)
    elif request.method == 'DELETE':
        return BaseEmployee().delete_employee(eid)
    else:
        return jsonify("Method Not Allowed"), 405   
    
# Reserve
@app.route('/dataops/reserve', methods=['GET', 'POST'])
def handle_reserve():
    if request.method == 'POST':
        return BaseReserve().add_new_reserve(request.json)
    else:
        return BaseReserve().get_all_reserve()

@app.route('/dataops/reserve/<int:reid>', methods=['GET', 'PUT', 'DELETE'])
def handle_reserve_by_id(reid):
    if request.method == 'GET':
        return BaseReserve().get_reserve_by_id(reid)
    elif  request.method == 'PUT':
        return BaseReserve().update_reserve(request.json)
    elif request.method == 'DELETE':
        return BaseReserve().delete_reserve(reid)
    else:
        return jsonify("Method Not Allowed"), 405  
    
# Roomunavailable
@app.route('/dataops/roomunavailable', methods=['GET', 'POST'])
def handle_roomunavailable():
    if request.method == 'POST':
        return BaseRoomunavailable().add_new_roomunavailable(request.json)
    else:
        return BaseRoomunavailable().get_all_roomunavailable()

@app.route('/dataops/roomunavailable/<int:ruid>', methods=['GET', 'PUT', 'DELETE'])
def handle_roomunavailable_by_id(ruid):
    if request.method == 'GET':
        return BaseRoomunavailable().get_roomunavailable_by_id(ruid)
    elif  request.method == 'PUT':
        return BaseRoomunavailable().update_roomunavailable(request.json)
    elif request.method == 'DELETE':
        return BaseRoomunavailable().delete_roomunavailable(ruid)
    else:
        return jsonify("Method Not Allowed"), 405    
    
# Hotel 
@app.route('/dataops/hotel', methods=['GET', 'POST'])
def handle_hotel():
    if request.method == 'POST':
        return BaseHotel().add_new_hotel(request.json)
    else:
        return BaseHotel().get_all_hotels()

@app.route('/dataops/hotel/<int:hid>', methods=['GET', 'PUT', 'DELETE'])
def handle_hotel_by_id(hid):
    if request.method == 'GET':
        return BaseHotel().get_hotel_by_id(hid)
    elif  request.method == 'PUT':
        return BaseHotel().update_hotel(request.json)
    elif request.method == 'DELETE':
        return BaseHotel().delete_hotel(hid)
    else:
        return jsonify("Method Not Allowed"), 405  
  
# Login 
@app.route('/dataops/login', methods=['GET', 'POST'])
def handle_login():
    if request.method == 'POST':
        return BaseLogin().add_new_login(request.json)
    else:
        return BaseLogin().get_all_logins()

@app.route('/dataops/login/<int:lid>', methods=['GET', 'PUT', 'DELETE'])
def handle_login_by_id(lid):
    if request.method == 'GET':
        return BaseLogin().get_login_by_id(lid)
    elif  request.method == 'PUT':
        return BaseLogin().update_login(request.json)
    elif request.method == 'DELETE':
        return BaseLogin().delete_login(lid)
    else:
        return jsonify("Method Not Allowed"), 405


################################################# GLOBAL STATISTICS #####################################################
# Top 3 chains with the highest total revenue.
@app.route('/dataops/most/revenue', methods=['POST']) # 9
def most_revenue_chains(eid):
    if request.method == 'POST':
        return BaseChains().top_3_chains_by_total_revenue()
    else:
        return jsonify("Method Not Allowed"), 405

# Total reservation percentage by payment method.
@app.route('/dataops/paymentmethod', methods=['POST']) # 10
def payment_method_reservations(eid):
    if request.method == 'POST':
        return BaseReserve().total_reservations_by_payment()
    else:
        return jsonify("Method Not Allowed"), 405

# Top 3 chains with the least rooms.    
@app.route('/dataops/least/rooms', methods=['POST']) # 11
def least_rooms_chains(eid):
    if request.method == 'POST':
        return BaseChains().top_3_chains_with_least_rooms()
    else:
        return jsonify("Method Not Allowed"), 405

# Top 5 hotels with the most client capacity.    
@app.route('/dataops/most/capacity', methods=['POST']) # 12
def most_capacity_hotels(eid):
    if request.method == 'POST':
        return BaseHotel().top_5_hotels_most_capacity()
    else:
        return jsonify("Method Not Allowed"), 405

# Top 10% of the hotels that had the most reservations.    
@app.route('/dataops/most/reservation', methods=['POST']) # 13
def most_reservations_hotels(eid):
    if request.method == 'POST':
        return BaseHotel().top_10_percent_most_reservations()
    else:
        return jsonify("Method Not Allowed"), 405

################################################# LOCAL STATISTICS #####################################################

# Top 5 handicap rooms that were reserved the most.
@app.route('/dataops/<int:hid>/handicaproom', methods=['POST']) # 2
def most_reserved_handicap_rooms(hid):
    if request.method == 'POST':
        return BaseHotel().top_10_percent_most_reservations(hid)
    else:
        return jsonify("Method Not Allowed"), 405
    
# Top 5 clients under 30 years old that made the most reservation with a credit card.
@app.route('/dataops/<int:hid>/mostcreditcard', methods=['POST']) # 4
def most_creditcard_clients(hid):
    if request.method == 'POST':
        return BaseClient().top_5_most_creditcard_under_30(hid)
    else:
        return jsonify("Method Not Allowed"), 405

# Top 3 highest paid regular employees.
@app.route('/dataops/<int:hid>/highestpaid', methods=['POST']) # 5
def highest_paid_regular_employes(hid):
    if request.method == 'POST':
        return BaseEmployee().highest_paid_regular_employees(hid)
    else:
        return jsonify("Method Not Allowed"), 405
    

if __name__ == '__main__':
    app.run(DEBUG=True)