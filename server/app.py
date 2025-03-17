from flask import Flask, request, jsonify, session
from flask_cors import CORS
import mysql.connector
import traceback

app = Flask(__name__)
app.secret_key = 'kbo7c43w7898jbs'  # Required for session management
CORS(app, supports_credentials=True)  # Enable CORS with credentials support

# Database connection configuration
DB_CONFIG = {
    'host': '104.198.30.234',
    'port': 3306,
    'user': 'moodmingle_user',
    'password': 'team2',
    'database': 'MoodMingle',
}

# Helper function to get database connection
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Test database connection
@app.route("/test-db", methods=["GET"])
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Users")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({
            "success": True, 
            "message": "Database connection successful", 
            "user_count": count
        })
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": str(e),
            "traceback": traceback.format_exc()
        })

# Check if specific user exists
@app.route("/check-user/<username>", methods=["GET"])
def check_user(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, name, email FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            return jsonify({
                "exists": True, 
                "user": {
                    "username": user[0],
                    "name": user[1],
                    "email": user[2]
                }
            })
        else:
            return jsonify({"exists": False})
    except Exception as e:
        return jsonify({"error": str(e)})

# Create test user
@app.route("/create-test-user", methods=["GET"])
def create_test_user():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Users (username, name, email, password) VALUES (%s, %s, %s, %s)",
            ("testuser", "Test User", "test@example.com", "password123")
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "Test user created"})
    except Exception as e:
        return jsonify({"error": str(e)})

# User login
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")
        print(f"Login attempt for username: {username}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query to get user by username - only use columns that actually exist
        query = "SELECT username, password, email FROM Users WHERE username = %s"
        print(f"Executing query: {query} with username={username}")
        cursor.execute(query, (username,))
        user_data = cursor.fetchone()
        
        print(f"Query result: {user_data}")
        
        # Check if user exists and password matches
        if user_data and user_data[1] == password:  # Plain text comparison for now
            user_obj = {
                "username": user_data[0],
                "displayName": user_data[0],  # Use username as displayName since name column doesn't exist
                "email": user_data[2]
            }
            
            # Store in session
            session['user'] = user_obj
            
            print(f"Login successful for user: {username}")
            cursor.close()
            conn.close()
            return jsonify({"success": True, "user": user_obj})
        else:
            if not user_data:
                print(f"User not found: {username}")
                cursor.close()
                conn.close()
                return jsonify({"success": False, "error": "User not found"}), 401
            else:
                print(f"Invalid password for user: {username}")
                cursor.close()
                conn.close()
                return jsonify({"success": False, "error": "Invalid password"}), 401
            
    except Exception as e:
        print(f"Login error: {str(e)}")
        traceback.print_exc()
        return jsonify({"success": False, "error": f"An error occurred during login: {str(e)}"}), 500
# User signup
@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user already exists
        check_query = "SELECT COUNT(*) FROM Users WHERE username = %s OR email = %s"
        cursor.execute(check_query, (username, email))
        if cursor.fetchone()[0] > 0:
            cursor.close()
            conn.close()
            return jsonify({"success": False, "error": "Username or email already exists"}), 400
        
        # Insert new user - only use fields that exist in your table
        insert_query = """
        INSERT INTO Users (username, email, password)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (username, email, password))
        conn.commit()
        
        # Create user object for response
        user_obj = {
            "username": username,
            "displayName": username,  # Use username as display name
            "email": email
        }
        
        # Store in session
        session['user'] = user_obj
        
        cursor.close()
        conn.close()
        return jsonify({"success": True, "user": user_obj})
        
    except Exception as e:
        print(f"Signup error: {str(e)}")
        traceback.print_exc()
        return jsonify({"success": False, "error": f"An error occurred during signup: {str(e)}"}), 500

# Update user profile
@app.route("/update-profile", methods=["PUT"])
def update_profile():
    try:
        if 'user' not in session:
            return jsonify({"success": False, "error": "Not authenticated"}), 401
            
        data = request.json
        username = data.get("username")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Your database doesn't have a 'name' column, so we can only update other fields if needed
        # For now, let's just return success
        
        cursor.close()
        conn.close()
        return jsonify({"success": True})
        
    except Exception as e:
        print(f"Profile update error: {str(e)}")
        traceback.print_exc()
        return jsonify({"success": False, "error": f"An error occurred updating profile: {str(e)}"}), 500
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
            "isGuest": True
        }
        return jsonify({"success": True, "user": guest_user})

# Logout route to clear session
@app.route("/logout", methods=["POST"])
def logout():
    session.pop('user', None)
    return jsonify({"success": True, "message": "Logged out successfully"})

# Update user interests
@app.route("/user/interests", methods=["PUT"])
def update_interests():
    try:
        if 'user' not in session:
            return jsonify({"success": False, "error": "Not authenticated"}), 401
            
        data = request.json
        username = data.get("username")
        interests = data.get("interests", [])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get user ID
        id_query = "SELECT userID FROM Users WHERE username = %s"
        cursor.execute(id_query, (username,))
        user_result = cursor.fetchone()
        
        if not user_result:
            cursor.close()
            conn.close()
            return jsonify({"success": False, "error": "User not found"}), 404
            
        user_id = user_result[0]
            
        # Delete existing preferences
        delete_query = "DELETE FROM Preferences WHERE userID = %s"
        cursor.execute(delete_query, (user_id,))
        
        # Insert new preferences
        for interest in interests:
            insert_query = "INSERT INTO Preferences (userID, keyword) VALUES (%s, %s)"
            cursor.execute(insert_query, (user_id, interest))
            
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True})
        
    except Exception as e:
        print(f"Interests update error: {str(e)}")
        traceback.print_exc()
        return jsonify({"success": False, "error": f"An error occurred updating interests: {str(e)}"}), 500

# Execute SQL directly for debugging - ONLY FOR DEVELOPMENT!
@app.route("/execute-sql", methods=["POST"])
def execute_sql():
    try:
        data = request.json
        query = data.get("query")
        
        if not query:
            return jsonify({"success": False, "error": "No query provided"}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(query)
        
        # If select query
        if query.strip().lower().startswith("select"):
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            cursor.close()
            conn.close()
            return jsonify({"success": True, "results": results})
        
        # If insert/update/delete
        else:
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()
            return jsonify({"success": True, "affected_rows": affected_rows})
            
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)