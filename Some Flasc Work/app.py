# app.py
from flask import Flask, request, render_template
# Import the functions you built in database.py
from database import init_db, add_user, get_all_users

app = Flask(__name__)

# Run table setup automatically when the server turns on
init_db()

@app.route('/register', methods=['POST'])
def register():
    # 1. Get the values submitted by the Frontend guy's HTML form
    user_name = request.form['username']
    user_email = request.form['email']
    
    # 2. Call your database function to save it
    add_user(user_name, user_email)
    
    # 3. Fetch updated list of users to show on screen
    all_users = get_all_users()
    
    # 4. Render the page with live database records
    return render_template('dashboard.html', users=all_users)

if __name__ == '__main__':
    app.run(debug=True)