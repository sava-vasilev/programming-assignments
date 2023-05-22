from werkzeug.security import check_password_hash
import pypyodbc as odbc


# Connect to the database server
conn = odbc.connect('DRIVER={SQL Server};'
                    'SERVER=localhost;'
                    'DATABASE=Flask_App;'
                    'Trusted_Connection=yes' 
                    )

c = conn.cursor()


# Create table 'user_creds'
def create_table1():
    c.execute('''
        CREATE TABLE user_creds (
            first_name nvarchar(MAX) NOT NULL,
            last_name nvarchar(MAX) NOT NULL,
            username nvarchar(MAX) NOT NULL,
            password nvarchar(MAX) NOT NULL,
            email_address nvarchar(MAX) Not NULL,
            phone nvarchar(MAX) NULL, 
            user_data_dir nvarchar(MAX) NOT NULL,
            user_sync_dir nvarchar(MAX) NOT NULL
            )
            ''')

    conn.commit()


# Create table 'user_files'
def create_table2():
    c.execute('''
        CREATE TABLE user_files (
            id int NOT NULL IDENTITY (1, 1) PRIMARY KEY,
            username nvarchar(MAX) NOT NULL,
            file_name nvarchar(MAX) NOT NULL,
            type nvarchar(MAX) NOT NULL,
            location nvarchar(MAX) NOT NULL
            )
            ''')

    conn.commit()


# Create method that will insert file and its details to the database 
def insert_file_data(username, file_name, type, location):

    query = "INSERT INTO user_files (username, file_name, type, location) VALUES (?, ?, ?, ?)"
    value = (username, file_name, type, location)

    try:
        c.execute(query, value)
        conn.commit()
        return True

    except Exception as e:
        print(e)
        conn.rollback()
        return False


# Create method to delete user file's details from the database
def delete_file_date(username, file_name):

    query = "DELETE FROM user_files WHERE username = ? and file_name = ?"
    value = (username, file_name)

    c.execute(query, value)
    conn.commit()


# Create method that checks if account with the same username already exists 
def check_account(username):
    
    # Create global variable that will store messages
    global check_message

    query = "SELECT username FROM user_creds WHERE username = ?"
    c.execute(query, [username])

    # Fetch username
    username = c.fetchone()

    # If there is no user with the same username, create the following account
    if username == None:
        return False

    else:
        check_message = "Username already exists. Please choose another one!"
        return True


# Create method that will will create accounts to new users
def register(first_name, last_name, username, password, email_address, phone, user_data_dir, user_sync_dir):

    # Create global variable that will store messages
    global register_message

    query1 = "INSERT INTO user_creds (first_name, last_name, username, password, email_address, phone, user_data_dir, user_sync_dir) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    value = (first_name, last_name, username, password, email_address, phone, user_data_dir, user_sync_dir)

    try:
        c.execute(query1, value)
        conn.commit()
        return True

    except:
        register_message = "Something went wrong! Please try again later."
        conn.rollback()
        return False


# Create method that checks if username and password of certain user are correct
def check_user_pass(username, password):

    # Query that checks if there is a record in the databese with the following username
    query = "SELECT password FROM user_creds WHERE username = ?"

    c.execute(query, [username])

    # Fetch password of the user
    user_password = c.fetchone()

    if user_password != None:

        # Compare the entered password with the one save in the database 
        if check_password_hash(user_password[0], password):
            return True

        else: 
            return False

    else:
        return False


# Create function insert
def insert(filename, username):
    with conn:

        query="INSERT INTO user_files (filename, username) VALUES (?, ?)"        
        val=(filename, username)

        try: 
            c.execute(query, val)
            print("record is inserted")
            conn.commit()

        except Exception as e:
            conn.rollback()
            print(e)


def delete(username):
    with conn:
        query = "DELETE FROM user_files WHERE username = ?"

        c.execute(query, [username])
        conn.commit()


# Create method that fetches the path of the data folder of the selected user
def data_path(username):
    
    # Create global that will store the fetch data
    global path
    
    query = "SELECT user_data_dir FROM user_creds WHERE username = ?"
    c.execute(query, [username])

    # Fetcheed the path
    path = c.fetchone()
    path = path[0]

    if path == None:
        return False
    
    else:
        return True


# Create method that will fetch user's datail
def account_info(username):

    # Create global to store user's details
    global data

    query = "SELECT * FROM user_creds WHERE username = ?"
    c.execute(query, [username])
    
    # Fetch user's details
    data = c.fetchone()

    if data != None :
        return True
    
    else:
        return False
