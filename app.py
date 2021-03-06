from flask import Flask, render_template, url_for, request, redirect
from db_connector import connect_to_database, execute_query

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/book_ticket.html', methods=['POST', 'GET'])
def book_tickets():
    if request.method == 'GET':
        query = 'SELECT * FROM Customers'
        db_connection = connect_to_database()
        result = execute_query(db_connection, query).fetchall()
        print(f"All Customers in DB: {result}")
        query = 'SELECT * FROM Transport_Pods'
        db_connection = connect_to_database()
        result = execute_query(db_connection, query).fetchall()
        print(f"All Pods in DB: {result}")

    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        partySize = request.form['partySize']
        destination = request.form['destination']

        db_connection = connect_to_database()
        query = "SELECT * FROM Transport_Pods"
        results = execute_query(db_connection, query).fetchall()

        for result in results:
            if result[1] == True:
                if result[3] > int(partySize):
                    if result[4] == False:
                        if result[5] == 1:
                            currentPod = str(result[0])

                            location_query = "SELECT * FROM Locations"
                            location_results = execute_query(db_connection, location_query).fetchall()
                            for location in location_results:
                                if location[1] == destination:
                                    destination = str(location[0])

                                    customer_query = "INSERT INTO Customers (firstName, lastName, currentPod, destination) VALUES (%s, %s, %s, %s)"
                                    data = (firstName, lastName, currentPod, destination)
                                    execute_query(db_connection, customer_query, data)
                                    return redirect(url_for('ticket_response'))
        print("error - add more pods")
        
    else:
        return render_template('book_ticket.html')

@app.route('/customers.html')
def customers():
    db_connection = connect_to_database()
    query = "SELECT customerID, firstName, lastName, currentPod, destination FROM Customers;"
    result = execute_query(db_connection, query).fetchall()
    print(f"All Customers in DB: {result}")
    return render_template('customers.html', rows=result)

@app.route('/engineer_pods.html', methods=['POST', 'GET'])
def engineer_pods():
    if request.method == 'GET':
        db_connection = connect_to_database()
        query = "SELECT engineerID, podID FROM Engineer_Pods;"
        result = execute_query(db_connection, query).fetchall()
        print(f"All Engineer_Pods in DB: {result}")
        return render_template('engineer_pods.html', rows=result)
    
    if request.method == 'POST':
        engineerID = request.form['engineerID']
        podID = request.form['podID']

        db_connection = connect_to_database()
        query = "INSERT INTO Engineer_Pods (engineerID, podID) VALUES (%s, %s)"
        data = engineerID, podID
        execute_query(db_connection, query, data)
        return redirect(url_for('engineer_pods'))


@app.route('/engineers.html', methods=['POST', 'GET'])
def engineers():
    if request.method == 'GET':
        db_connection = connect_to_database()     
        query = "SELECT engineerID, firstName, lastName, available FROM Service_Engineers;"
        result = execute_query(db_connection, query).fetchall()
        print(f"All Engineers in DB: {result}")
        return render_template('engineers.html', rows=result)

    if request.method == 'POST' and 'firstName' in request.form:
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        available = request.form['available']
        db_connection = connect_to_database()
        query = "INSERT INTO Service_Engineers (firstName, lastName, available) VALUES (%s, %s, %s)"
        data = firstName, lastName, available
        execute_query(db_connection, query, data)
        return redirect(url_for('engineers'))
  
    if request.method == 'POST':
        lastName = request.form['lastName'] 
        db_connection = connect_to_database()   
        query = "SELECT engineerID, firstName, lastName, available FROM Service_Engineers WHERE lastName = '%s'" %(lastName)
        searchresult = execute_query(db_connection, query).fetchall()
        print(f"Search Result: {searchresult}")
        query = "SELECT engineerID, firstName, lastName, available FROM Service_Engineers;"
        result = execute_query(db_connection, query).fetchall()
        print(f"All Engineers in DB: {result}")
        return render_template('engineers.html', searchrows=searchresult, rows= result)
       
    else:
        return render_template('engineers.html')


        
@app.route('/locations.html', methods=['GET', 'POST'])
def locations():
    if request.method == 'GET':
        db_connection = connect_to_database()
        query = "SELECT locationID, description FROM Locations;"
        result = execute_query(db_connection, query).fetchall()
        print(f"All Locations in DB: {result}")
        return render_template('locations.html', rows=result)

    if request.method == 'POST': 
        description = request.form['description']

        db_connection = connect_to_database()
        query = "INSERT INTO Locations (description) VALUES (%s)"
        data = (description,)
        execute_query(db_connection, query, data)
        return redirect(url_for('locations'))
       
    else:
        return render_template('locations.html')

@app.route('/pods.html', methods=['GET', 'POST'])
def pods():
    if request.method == 'GET':
        db_connection = connect_to_database()
        query = "SELECT podID, operableStatus, seatCapacity, availableSeat, inTransition, currentLocation FROM Transport_Pods;"
        result = execute_query(db_connection, query).fetchall()
        print(f"All Pods in DB: {result}")
        return render_template('pods.html', rows=result)

    if request.method == 'POST' and 'operableStatus' in request.form:
        operableStatus = request.form['operableStatus']
        seatCapacity = '5'
        availableSeat = '5'
        inTransition = '0'
        currentLocation = request.form['currentLocation']

        db_connection = connect_to_database()
        query = "INSERT INTO Transport_Pods (operableStatus, seatCapacity, availableSeat, inTransition, currentLocation) VALUES (%s, %s, %s, %s, %s)"
        data = operableStatus, seatCapacity, availableSeat, inTransition, currentLocation
        execute_query(db_connection, query, data)
        return redirect(url_for('pods'))

    if request.method == 'POST':
        podID = request.form['podID'] 
        db_connection = connect_to_database()   
        query = "SELECT podID, operableStatus, seatCapacity, availableSeat, inTransition, currentLocation FROM Transport_Pods WHERE podID = '%s'" %(podID)
        searchresult = execute_query(db_connection, query).fetchall()
        print(f"Search Result: {searchresult}")
        query = "SELECT podID, operableStatus, seatCapacity, availableSeat, inTransition, currentLocation FROM Transport_Pods;"
        result = execute_query(db_connection, query).fetchall()
        print(f"All Pods in DB: {result}")
        return render_template('pods.html', searchrows=searchresult, rows= result)
       
       
    else:
        return render_template('pods.html')





@app.route('/review.html')
def review():
    return render_template('review.html')

@app.route('/ticket_response.html')
def ticket_response():
    return render_template('ticket_response.html')    

if __name__ == "__main__":
    app.run(debug=True)
