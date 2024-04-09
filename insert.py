import dataextract
import psycopg2

# Test Database Credentials

hostname = "cc3engiv0mo271.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com"
database = "d8uea7h8p65mvj"
username = "ufbb5r769p4qkt"
port_id = 5432
pswrd = "p182c562d39073627fa01820090f0519f04fc3c136c27f287dcb5f070084f5b56"


# Production Database Credentials
'''
hostname = "cbbirn8v9855bl.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com"
database = "d2ghqj593h4e8t"
username = "u44qctnupemhd1"
port_id = 5432
pswrd = "p70ecec794926ab5abdee6ba81e18ef74aeafda0aedef0acc48cd91f6068b0405"
'''

def create_cursor():
    # Initialize connection and cursor as None
    connection = None
    cursor = None
    
    # Uses the database's credentials to connect to the database
    connection = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pswrd,
        port = port_id
    )
    
    # Creates a database cursor using the established connection
    cursor = connection.cursor()
    return cursor, connection

# Inserts client data to the client table
def insert_client_data(cursor):
    insert_client = ''' INSERT INTO client (clid, fname, lname, age, memberyear)
                        VALUES (%s, %s, %s, %s, %s)'''
    clients = dataextract.get_client_data()
    for client in clients:
        cursor.execute(insert_client, client)

# Inserts hotel data to the hotel table
def insert_hotel_data(cursor):
    insert_hotel = ''' INSERT INTO hotel (hid, chid, hname, hcity)
                        VALUES (%s, %s, %s, %s)'''
    hotels = dataextract.get_hotel_data()
    for hotel in hotels:
        cursor.execute(insert_hotel, hotel) 

# Inserts room unavailable data to the roomunavailable table    
def insert_room_unavailable_data(cursor):
    insert_room_unavailable = ''' INSERT INTO roomunavailable (ruid, rid, startdate, enddate)
                        VALUES (%s, %s, %s, %s)'''
    rooms = dataextract.get_room_unavailable_data()
    for room in rooms:
        cursor.execute(insert_room_unavailable, room)

# Inserts reservation data to the reserve table    
def insert_reserve_data(cursor):
    insert_reserve = ''' INSERT INTO reserve (reid, ruid, clid, total_cost, payment, guests)
                        VALUES (%s, %s, %s, %s, %s, %s)'''
    reservations = dataextract.get_reservations_data()
    for reservation in reservations:
        cursor.execute(insert_reserve, reservation)

# Inserts room data to the room table    
def insert_room_data(cursor):
    insert_room = ''' INSERT INTO room (rid, hid, rdid, rprice)
                        VALUES (%s, %s, %s, %s)'''
    rooms = dataextract.get_rooms_data()
    for room in rooms:
        cursor.execute(insert_room, room)

# Inserts employee data to the employee table    
def insert_employee_data(cursor):
    insert_employee = ''' INSERT INTO employee (eid, hid, fname, lname, age, salary, position)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    employees = dataextract.get_employee_data()
    for employee in employees:
        cursor.execute(insert_employee, employee)

# Inserts room description data to the roomdescription table
def insert_room_description_data(cursor):
    insert_room_description = ''' INSERT INTO roomdescription (rdid, rname, rtype, capacity, ishandicap)
                        VALUES (%s, %s, %s, %s, %s)'''
    room_descriptions = dataextract.get_room_details_data()
    for description in room_descriptions:
        cursor.execute(insert_room_description, description)

# Inserts chain data to the chains table
def insert_chain_data(cursor):
    insert_chain = ''' INSERT INTO chains (chid, cname, springmkup, summermkup, fallmkup, wintermkup)
                        VALUES (%s, %s, %s, %s, %s, %s)'''
    chains = dataextract.get_chain_data()
    for chain in chains:
        cursor.execute(insert_chain, chain)

# Inserts login data to the login table    
def insert_login_data(cursor):
    insert_login = ''' INSERT INTO login (lid, eid, username, password)
                        VALUES (%s, %s, %s, %s)'''
    logins = dataextract.get_login_data()
    for login in logins:
        cursor.execute(insert_login, login)


cursor = None 
connection = None 

try:
    # Creates database connection and cursor
    cursor, connection = create_cursor()
    
    print("Inserting clients")
    insert_client_data(cursor)
    
    print("Inserting chains")
    insert_chain_data(cursor)
    
    print("Inserting hotels")
    insert_hotel_data(cursor)
    
    print("Inserting room details")
    insert_room_description_data(cursor)
    
    print("Inserting employees")
    insert_employee_data(cursor)
    
    print("Inserting logins")
    insert_login_data(cursor)
    
    print("Inserting rooms")
    insert_room_data(cursor)
    
    print("Inserting unavailables rooms")
    insert_room_unavailable_data(cursor)
    
    print("Inserting reservations")
    insert_reserve_data(cursor)

    
    connection.commit()
    
# Catches an exception if the database cursor or connection cannot be created, and prints the exception  
except Exception as error:
    print(error)
    
# Closes the connection and cursor objects if created
finally:
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()
    
    