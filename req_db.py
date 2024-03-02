import pymysql.cursors
import random
import string
import argon2
from argon2 import PasswordHasher, exceptions


###########################################################################
#chack common passwords  /// ilustrate large library of common passwords
passwords111= {"passwords":{"12345678910" , "Password" ,"P@ssw0rd",
                          "Pass@123" , "Aa@123456","1q2w3e4r5t"}}

def common_passwords(password,passwords111):
    for x in passwords111["passwords"]:
        if x == password:
            print("chahnge password")
        
    print("not common password")    




#common_passwords("assword",passwords111)
##########################################################################
import hashlib
import random
import string

def hash1_password(password):
    sha1_hash = hashlib.sha1(random_password.encode()).hexdigest()
    return sha1_hash

#####################################################################
#itay
ph = PasswordHasher()
name = ph.hash("itay")
print(name)


def compare_pass_history(username, pWord):
    ph = PasswordHasher()
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:           
            # Get current and 2 passwords back and compare the new one to all 3. 
            sqlSelect = "SELECT password FROM user WHERE username=%s"
            cursor.execute(sqlSelect, (username , ))
            pass1 = cursor.fetchone()

            sqlUpdate = "SELECT passwordsecond FROM userpass WHERE uname=%s"
            cursor.execute(sqlUpdate, (username, ))
            pass2 = cursor.fetchone()

            sqlUpdate = "SELECT passwordthird FROM userpass WHERE uname=%s"
            cursor.execute(sqlUpdate, (username, ))
            pass3 = cursor.fetchone()

            #If we fail validating against all 3, so it means its a new one
            allowedToProceed = False;
            try:
                ph.verify(pass1['password'], pWord)
                return 0
            except exceptions.VerifyMismatchError:
                try:
                    ph.verify(pass2['passwordsecond'], pWord)
                    return 0
                except exceptions.VerifyMismatchError:
                    try:
                        ph.verify(pass3['passwordthird'], pWord)
                        return 0
                    except exceptions.VerifyMismatchError:
                        return 1


    except pymysql.Error as e:
        print(f"Database error: {e}")
        return 0

    finally:
        if connection:
            connection.close()






def connect_to_db():
    host = "127.0.0.1"
    user = "root"
    password = "my-secret-pw"
    dbname = "USERS"

    # Connect to the database
    db_connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=dbname,
        port=3456,
        cursorclass=pymysql.cursors.DictCursor,
    )

    return db_connection


def validate_password(username, pWord):
    # Connect to the database
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            # Check if the username and password match a user in the database
            sql = "SELECT password FROM user WHERE username=%s"
            cursor.execute(sql, (username,))
            pass_hash = cursor.fetchone()
            ph = PasswordHasher()

            # On success return 1
            if pass_hash:
                    if ph.verify(pass_hash["password"], pWord):
                        return 1
                    else:
                        print("Invalid username or password")
                        return None
            else:
                return None

    except pymysql.Error as e:
        print(f"Database error: {e}")
    except argon2.exceptions.InvalidHashError:
        return None   
    except argon2.exceptions.VerifyMismatchError:
        return None   


    finally:
        if connection:
            connection.close()





def change_password(username, pWord, oldpHash): # Assumed authenticated, we authenticate in the line before in /register
    # Connect to the database
    ph = PasswordHasher()
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:           
            # Check if the username and password match a user in the database
            pHash = ph.hash(pWord)

            sqlSelect = "SELECT passwordsecond, passwordthird FROM userpass WHERE uname=%s"
            cursor.execute(sqlSelect, (username , ))
            passwordSecond, passwordThird = cursor.fetchone()

            #We discard the 3rd, put the 2nd there.
            passwordThird = passwordSecond
            sqlUpdate = "UPDATE userpass SET passwordthird =%s WHERE uname =%s"
            cursor.execute(sqlUpdate, (ph.hash(passwordThird), username, ))

            #Put current one (pre change) into 2nd.
            passwordSecond = oldpHash
            sqlUpdate = "UPDATE userpass SET passwordsecond =%s WHERE uname =%s"
            cursor.execute(sqlUpdate, (ph.hash(passwordSecond), username, ))

            #Update current password with the new password
            sql = "UPDATE user SET password =%s WHERE username =%s"
            if ph.verify(pHash, pWord):
                cursor.execute(sql, (pHash, username, ))
                connection.commit()
                print("commited update")
                return 1
            else:
                raise pymysql.Error
    except pymysql.Error as e:
        print(f"Database error: {e}")
        return 0
    finally:
        if connection:
            connection.close()




def register_new_user(username, email, pWord):
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            ph = PasswordHasher()
            passHash = ph.hash(pWord)
            sqlInsert = "INSERT INTO user (username, email, password) VALUES (%s, %s, %s)"
            values = (username, email, passHash)
            cursor.execute(sqlInsert, values)

            sqlCreatePassTable = "INSERT INTO userpass (uname, passwordtemp, passwordsecond, passwordthird) VALUES (%s, %s, %s, %s)"
            dummyHash = ph.hash(generate_random_password()) 
            values = (username, dummyHash, dummyHash, dummyHash)
            cursor.execute(sqlCreatePassTable, values)
        # Commit the changes to the database
        connection.commit()
        print("User registered successfully!")

    except pymysql.Error as e:
        print(f"Error: {e}")


    finally:
        if connection:
            connection.close()

def register_new_client(username, email, phoneNum):
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            sql = "INSERT INTO clients (name, email, phone) VALUES (%s, %s, %s)"
            values = (username, email, phoneNum)
            cursor.execute(sql, values)
        # Commit the changes to the database
        connection.commit()
        print("Client registered successfully!")

    except pymysql.Error as e:
        print(f"Error: {e}")

    finally:
        if connection:
            connection.close()

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for _ in range(length))
    return password


def show_user_db():
    # Connect to the database
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM user;"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                print(row)

    except:
        print("something failed")

    finally:
        if connection:
            connection.close()


###working and checked
def show_clientent_db():
    # Connect to the database
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM clients;"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                print(row)

    except:
        print("something failed")

    finally:
        if connection:
            connection.close()





def validate_mail_code(username, pWord):
    # Connect to the database
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:           
            # Check if the username and password match a user in the database
            sql = "SELECT passwordtemp FROM userpass WHERE uname=%s"
            cursor.execute(sql, (username , ))
            mail_hash = cursor.fetchone()
            ph = PasswordHasher()

            #On success return 1
            if ph.verify(mail_hash['passwordtemp'], pWord):
                return 1
            else:
                print("Invalid username or password")
                return 0

    except pymysql.Error as e:
        print(f"Database error: {e}")

    finally:
        if connection:
            connection.close()