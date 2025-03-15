# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from database.databaseConnection import DatabaseConnection  # Import your database connection class
# from database.databaseQueries import DatabaseQueries  # Import your query class

# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend communication

# # Establish database connection
# db = DatabaseConnection(
#     dbname='MoodMingle',
#     user='moodmingle_user',
#     password='team2',
#     host='104.198.30.234',
#     port=3306
# )
# db.connect()
# queries = DatabaseQueries(db.connection)

# # User login route
# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     username = data.get("username")
#     password = data.get("password")

#     if queries.user_exists(username, password):
#         return jsonify({"message": "Login successful", "status": "success"}), 200
#     else:
#         return jsonify({"message": "Invalid username or password", "status": "error"}), 401

# # User registration route
# @app.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     username = data.get("username")
#     email = data.get("email")
#     password = data.get("password")

#     if queries.add_user(username, email, password):
#         return jsonify({"message": "User registered successfully", "status": "success"}), 201
#     else:
#         return jsonify({"message": "User already exists or error occurred", "status": "error"}), 400

# # Close database connection on exit
# @app.teardown_appcontext
# def close_db_connection(exception=None):
#     db.disconnect()

# if __name__ == '__main__':
#     app.run(debug=True)





# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from database.databaseConnection import db  # Ensure this is set up to connect to MySQL
# from database.databaseQueries import DatabaseQueries as dq  # Import your query class

# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend-backend communication

# # User login
# @app.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     username = data.get("username")
#     password = data.get("password")

#     db.connect()
#     if dq.user_exists(username, password):  # Assuming this function checks credentials
#         user_data = dq.select_from_table("Users", columns=["username", "email", "displayName"], conditions=f"username='{username}'")[0]
#         db.disconnect()
#         return jsonify({"success": True, "user": dict(zip(["username", "email", "displayName"], user_data))})
#     else:
#         db.disconnect()
#         return jsonify({"success": False, "error": "Invalid username or password"}), 401

# # User signup
# @app.route("/signup", methods=["POST"])
# def signup():
#     data = request.json
#     username = data.get("username")
#     email = data.get("email")
#     password = data.get("password")

#     db.connect()
#     if dq.add_user(username, email, password):  # Assuming this function inserts into DB
#         db.disconnect()
#         return jsonify({"success": True, "user": {"username": username, "email": email}})
#     else:
#         db.disconnect()
#         return jsonify({"success": False, "error": "Signup failed"}), 400

# # Update user profile
# @app.route("/update-profile", methods=["PUT"])
# def update_profile():
#     data = request.json
#     username = data.get("username")
#     displayName = data.get("displayName")
#     location = data.get("location")

#     db.connect()
#     update_query = f"UPDATE Users SET displayName='{displayName}', location='{location}' WHERE username='{username}'"
#     try:
#         db.cursor.execute(update_query)
#         db.connection.commit()
#         db.disconnect()
#         return jsonify({"success": True})
#     except:
#         db.disconnect()
#         return jsonify({"success": False, "error": "Update failed"}), 400

# if __name__ == "__main__":
#     app.run(debug=True)





from flask import Flask, request, jsonify, session
from flask_cors import CORS
from database.databaseConnection import db  # Ensure this is set up to connect to MySQL
from database.databaseQueries import DatabaseQueries as dq  # Import your query class

app = Flask(__name__)
app.secret_key = 'kbo7c43w7898jbs'  # Required for session management
CORS(app, supports_credentials=True)  # Enable CORS for frontend-backend communication

# User login
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")
        print(f"Attempting login for {username}")

        db.connect()
        dq_query = dq(db.connection)
        
        # Retrieve user credentials from the database
        user_credentials = dq_query.user_exists_2(username, password)
        
        if user_credentials:
            stored_username, stored_password = user_credentials  # Unpack the username and password from the result
            
            # Check if the entered password matches the stored password (if using hashed passwords, use check_password_hash)
            if stored_username == username and stored_password == password:  # For plaintext passwords
                # For hashed passwords, you would use check_password_hash(stored_password, password)
                
                # Retrieve user data to store in session
                user_data = dq_query.select_from_table("Users", columns=["username", "email"], conditions=f"username='{username}'")[0]
                db.disconnect()
                
                # Store user in session after successful login
                session['user'] = dict(zip(["username", "email", "displayName"], user_data))
                
                print("Login Successful")            
                return jsonify({"success": True, "user": dict(zip(["username", "email"], user_data))})
            else:
                print("Password does not match")
                db.disconnect()
                return jsonify({"success": False, "error": "Invalid username or password"}), 401
        else:
            print("No matching user found")
            db.disconnect()
            return jsonify({"success": False, "error": "Invalid username or password"}), 401

    except Exception as e:
        print(f"Error during login: {str(e)}")
        db.disconnect()
        return jsonify({"success": False, "error": "An error occurred during login"}), 500

# User signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    db.connect()
    dq_query = dq(db.connection())
    if dq_query.add_user(username, email, password):  # Assuming this function inserts into DB
        db.disconnect()
        return jsonify({"success": True, "user": {"username": username, "email": email}})
    else:
        db.disconnect()
        return jsonify({"success": False, "error": "Signup failed"}), 400

# Update user profile
@app.route("/update-profile", methods=["PUT"])
def update_profile():
    data = request.json
    username = data.get("username")
    displayName = data.get("displayName")
    location = data.get("location")

    db.connect()
    dq_query = dq(db.connection())
    update_query = f"UPDATE Users SET displayName='{displayName}', location='{location}' WHERE username='{username}'"
    try:
        db.cursor.execute(update_query)
        db.connection.commit()
        db.disconnect()
        return jsonify({"success": True})
    except:
        db.disconnect()
        return jsonify({"success": False, "error": "Update failed"}), 400

# Get current logged-in user
@app.route("/current-user", methods=["GET"])
def current_user():
    if 'user' in session:
        return jsonify({"success": True, "user": session['user']})
    else:
         # If no user is logged in, return a default guest user
        guest_user = {
            "username": "Guest",
            "email": "",
            "displayName": "Guest User",
            "isGuest": True  # Flag to indicate this is a guest user
        }
        return jsonify({"success": True, "user": guest_user})

# Logout route to clear session
@app.route("/logout", methods=["POST"])
def logout():
    session.pop('user', None)  # Remove user from session
    print("Successfuly Logged Out")
    return jsonify({"success": True, "message": "Logged out successfully"})

if __name__ == "__main__":
    app.run(debug=True)
