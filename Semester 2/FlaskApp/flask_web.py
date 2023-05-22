from flask import Flask, redirect, render_template, request, url_for, send_file 
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
from login import Login
from register import Register
import Database as db
import mkdir
import encryption as encr

# Create a flask instance
app = Flask(__name__)


# Create route decorator
@app.route('/registerPage', methods=['GET', 'POST'])
def registerPage():

    # Create globals variable that will store classes
    global r

    # Check the request method
    if request.method == 'GET':
        return render_template("register.html")

    else:
        # Register data
        r = Register(reg_firstname=request.form['first_name'], reg_lastname = request.form['last_name'], reg_username = request.form['username'],
        reg_password = request.form['password'], reg_emailaddress = request.form['email_address'], reg_phone= request.form['phone_number'])
        
        # Check if register button is clicked
        if 'register-btn' in request.form:
                       
            # Check if the informaion is correct
            if r.reg_firstname == "" or r.reg_lastname == "" or r.reg_username == "" or r.reg_password == "" or r.reg_emailaddress == "" or r.reg_phone == "" or 'checkbox' not in request.form:
                return render_template("register.html", message = "The information is not completed or the terms and conditions are checked! Please try again.") 
            
            else:
                try:
                    # Hashing the password
                    hash_value = generate_password_hash(r.reg_password)
                    r.reg_password = hash_value

                    # Method to check if the user has already account
                    if db.check_account(r.reg_username) == False:

                        # Create nessary folders where user's file will be stored
                        mkdir.check_dir(r.reg_username) 

                        # Create user's account
                        if db.register(r.reg_firstname, r.reg_lastname, r.reg_username, r.reg_password, r.reg_emailaddress, r.reg_phone, mkdir.folder_dic[0], mkdir.folder_dic[1]) == False:
                            return render_template("register.html", message = db.register_message)

                        else:
                            # Check the path of the user's data folder    
                            if db.data_path(r.reg_username) == True:
                                
                                # Configure the upload folder
                                UPLOAD_FOLDER = db.path
                                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

                            return redirect("userPage")

                    else:
                        return render_template("register.html", message = db.check_message)

                except:
                    return render_template("register.html", message = db.check_message)
                

# Create route decorator
@app.route('/', methods=['GET', 'POST'])
def loginPage():

    # Create globals variable that will store classes
    global l

    # Check the request method
    if request.method == 'GET':
        return render_template("index.html")

    else:
        # Login creadentials
        l = Login(log_username=request.form['log_username'], log_password = request.form['log_password'])       

        # Check if login button is clicked and the credentials are correct
        if 'submit-btn' in request.form and db.check_user_pass(l.log_username, l.log_password) == True:
            
            # Check the path to the user's data folder
            if db.data_path(l.log_username) == True:
            
                # Configure the upload folder
                UPLOAD_FOLDER = db.path
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            return redirect("userPage")

        else:            
            error_message = "The password is wrong or the user does not exist"
            return render_template("index.html", message = error_message)


# Allowed extentions of the files that could be uploaded to the server 
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mov', 'mp4', 'webm', 'docx', 'xlsx', 'py', 'html', 'pptx'}


# Create a method to check what is the extention of the file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Create route decorator
@app.route('/userPage', methods=['GET', 'POST'], endpoint="user")
def user():

    # Declare error message variable
    error_message = "No file selected. Click on 'Choose File' to select data and then click 'Submit' to uploaded it to your folder"

    # Checks the request method
    if request.method == 'GET':
        files = os.listdir(app.config['UPLOAD_FOLDER'])

        return render_template("user.html", files=files)
    
    elif request.method == 'POST':
        
        # Checks if the post request has the file part
        if 'file' not in request.files:
            return render_template('user.html', error_message = error_message)
        
        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            return render_template('user.html', error_message = error_message)
        
        if file and allowed_file(file.filename):
            
            # Formats the filename into a secure string
            filename = secure_filename(file.filename)
            
            # Moves the file into the declared folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Encrypt the file
            os.chdir(db.path)
            encr.encrypt(file.filename, encr.load_key())
            print("yes")

            # Fetch the type of the file that is uploaded
            type = os.path.splitext(filename)
            
            # Insert file's details into the database
            db.insert_file_data(l.log_username or r.reg_username, filename, type[1], db.path)

            return redirect(url_for('user'))


    return render_template("user.html")

    
# Create route decorator
@app.route('/userPage/<filename>', methods=['GET', 'POST'], endpoint="user1")
def download(filename):
    
    os.chdir(db.path)
    
    # Searches for files location
    file = db.path + '\\' + filename
 
    return send_file(file, as_attachment=True)
    


# Create route decorator
@app.route('/userPage/delete/<path:filename>', methods=['GET','POST'])
def delete(filename):
    
    # Delete certain fail from the user's folder
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))

    # Delete file's details from the database
    db.delete_file_date(l.log_username or r.reg_username, filename)
    return redirect(url_for('user'))


# Create route decorator
@app.route('/accountPage', methods=['GET', 'POST'])
def accountPage():

    # Check the user's credentials
    if db.account_info(l.log_username or r.reg_username) == True:
        return render_template("account.html", username = db.data[2], first_name = db.data[0], last_name = db.data[1], email_address = db.data[4], phone_number = db.data[5])


# Create debugger
if __name__ == "__main__":
    app.run(debug=True)