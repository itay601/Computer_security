from flask import Flask , render_template, request, flash, redirect, url_for, make_response,Response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from login import connect_to_db
from req_db import *
from send_pass_to_email import reset_password_and_send_email



app = Flask(__name__)


app.config['JWT_SECRET_KEY'] = '7$*&?>fhd3433@#4227'  # Change this to a secure random key in production
jwt = JWTManager(app)

'''
                                                                
                                                                   
888888888888  ,ad8888ba,    88888888ba,      ,ad8888ba,            
     88      d8"'    `"8b   88      `"8b    d8"'    `"8b           
     88     d8'        `8b  88        `8b  d8'        `8b          
     88     88          88  88         88  88          88     888  
     88     88          88  88         88  88          88     888  
     88     Y8,        ,8P  88         8P  Y8,        ,8P          
     88      Y8a.    .a8P   88      .a8P    Y8a.    .a8P      888  
     88       `"Y8888Y"'    88888888Y"'      `"Y8888Y"'       888  
                                                                   
                                                                                      

    * Finish mail password restore page, run below code, redirect to "authenticated password change" page 
   
                        if validate_mail_code(username, mail_code):
                            if compare_pass_history(username, password_new):                           
                                sqlSelect = "SELECT password FROM users WHERE username=%s"
                                cursor.execute(sqlSelect, (username , ))
                                password_old = cursor.fetchone()
                                if change_password(username, password_new, password_old):
                                    print("Successs")


    *** Return proper error messages such as duplicate email, duplicate phone number etc
    
   

    

'''




#need system_screen only with token in headers (not working)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('login.html')   

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_password(username, password):
            access_token = create_access_token(identity=username)
            # Render the template
            return render_template('system_screen.html')    

@app.route('/register.html', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        username = request.form['username'] 
        email = request.form['email']

        if request.form['user_type'] == 'user':          
            password = request.form['password']
            register_new_user(username , email , password)
            return render_template('login.html')

        elif request.form['user_type'] == 'client':
            phoneNum = request.form['clientPhone']
            register_new_client(username , email , phoneNum) 
            return redirect("/show.html") 

@app.route('/change_password.html', methods=['GET','POST'])
def change_password_():
    if request.method == 'GET':
        return render_template('change_password.html')

    elif request.method == 'POST':
        username     = request.form['username']
        password_old = request.form['currentPassword']
        password_new = request.form['newPassword']
        if validate_password(username, password_old):
            if compare_pass_history(username, password_new):
                if change_password(username, password_new, password_old):
                    return render_template('login.html') 
        return render_template('change_password.html') #Redirect nowhere, render error onto page here
    
@app.route('/forgot_password.html', methods=['GET','POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')
    elif request.method == 'POST':
        mail =request.form['email']
        reset_password_and_send_email(mail)
        return render_template('login.html')





@app.route('/system_screen.html', methods=['GET','POST'])
@jwt_required()
def system_screen():
    if request.method == 'GET':
        current_user = get_jwt_identity()
        print(current_user)
        if current_user==None:
            return render_template('login.html')  
        

#Skeleton method, needs to be tailored to our needs
@app.route('/show.html', methods=['GET'])
@jwt_required()
def show():
    if request.method == 'GET':
        # Connect to the database
        connection = connect_to_db()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM clients;" # Change statement accordingly
                cursor.execute(sql)
                result = cursor.fetchall()
        except:
            print("something failed")

        finally:
            connection.close()
        return render_template('table_display.html', headings= ("uName", "email", "pass"), data = result)   # (("Jeff","j@mail.com","asd123"),("don","d@mail.com","ads321"))




if __name__ == '__main__':
    app.run(debug=True)
    
  






