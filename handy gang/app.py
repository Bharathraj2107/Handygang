# follow the python coding standard and naming conventions.
#name: <Your name>
#Date: <Date when you started the program >
#describtion: <Signup page>

from flask import Flask,request,render_template, session #from flask package we are importing these things
import mysql.connector
app=Flask(__name__) #we are creating a obj called app for class flask from that only we are calling routes

app.secret_key = '\xf0?a\x9a\\\xff\xd4;\x0c\xcbHi'#to find  the session  we use the session key to identify which session we are using if we hv multiple database

@app.route('/')#it loads index page when we start if the index.html is not used it may go to some other page so it is used
def index():
    return render_template('index.html')

@app.route('/signup',methods=['GET','POST'])#when signup button is clicked and the http is passed on the server  then the signup method is called and define the available methods
def signup():
    if request.method=="POST":#we use request for post method and see if method==post.
        name=request.form["name"]#here name is variable and it stores the value entered by the user in the form where name="name"
        password=request.form["password"]
        phone=request.form["phone"]
        print(name,password,phone)
        try:
            connection = mysql.connector.connect(#connection is variable used to connect the mysql server so connection is server
            host="localhost",
            user="root",
            password="",
            database="final",
            ) 
            cursor=connection.cursor()#we use the cursor to identify for which database we are writing the query
            cursor.execute("insert into users (name,password,phone) values('"+name+"','"+password+"','"+phone+"')")#insert into the users table in the database name,password,phone
            connection.commit()#to save what we hv inserted,deleted,updated in server we use commit and connection is just variable for server connection
            cursor.close()#close the cursor
            connection.close()#close the connection
            return render_template('index.html')#for try block
        except Exception as e :
            print("error in connecting to the server"+str(e))#in e the reason for the error is stored and concat it with the other string
            return render_template('index.html')#for exception block
    return render_template('index.html')#if signup fails then this block

@app.route('/signin',methods=['GET','POST'])
def signin():
    if request.method=="POST":
        name=request.form["name"]
        password=request.form["Password"]
        print(name,password)
        try:
            connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="final",
            ) 
            cursor=connection.cursor()
            cursor.execute("select * from users where name='"+name+"'and password='"+password+"'")#if the entered  name and password match then it allows to the main page here name and password are columns in database both should match at a time
            result=cursor.fetchall()
            print(result)
            if result:
                return render_template('mainindex.html')
            else:
                return render_template('index.html')
        except Exception as e :
            print("error in connecting to the server"+str(e))
            return render_template('index.html')
    return render_template('index.html')

@app.route('/search', methods=["GET","POST"])
def search():
    if request.method=="POST":
        place=request.form["locations"]#the place selected by the user so we use request bcoz it is inside the form of post method
        try:
            connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="final",
            ) 
            cursor=connection.cursor()
            print(session['tab'])
            if session['tab'] == 'carpenter':#the session is set in  the carpenter,plumbing,electrical,painting-- method if it matches with this session then the location of  all the selected one will be displayed
                cursor.execute("select * from carpenter where location='"+place+"'")#it matches the  element that has same location in the database with the entered place all possible locations
                result=cursor.fetchall()
                title="carpenter"
            if session['tab'] == 'electrical':
                cursor.execute("select * from electrical where location='"+place+"'")
                result=cursor.fetchall()
                title="electrical"
            if session['tab'] == 'painting':
                cursor.execute("select * from painting where location='"+place+"'")
                result=cursor.fetchall()
                title="painting"
            if session['tab'] == 'plumbing':
                cursor.execute("select * from plumbing where location='"+place+"'")
                result=cursor.fetchall()
                title="plumbing"
            if session['tab'] == 'maintenance':
                cursor.execute("select * from maintenance where location='"+place+"'")
                result=cursor.fetchall()
                title="maintenance"

            return render_template('carpenter.html', result=result, title=title)
        except Exception as e:
            print(e)
            return render_template('carpenter.html')
    return render_template('carpenter.html')


@app.route('/carpenter')
def carpenter():
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="final",
        ) 
        cursor=connection.cursor()
        cursor.execute("select * from carpenter")
        result=cursor.fetchall()
        session['tab'] = 'carpenter'#it is set in all the table if this session matches the above session then it displays all the matched locations

        cursor.execute("select location from carpenter")
        locations=cursor.fetchall()#here we are fetching all the locations and storing in locations

        locs = []#here we create a list called locs
        for loc in locations:#here each location is stored in loc and appended to the list called loc
            locs.append(loc[0])
        
        print(locs)
        locs = set(locs)#since there are duplicates allowed in list we will convert it to set were there is no duplicate allowed and then sent back to the same locations
        print(locs)
        locations = list(locs)
        return render_template('carpenter.html', result=result, title="Carpentar", locations=locations)
    except Exception as e:
        print(e)
        return render_template('carpenter.html')

@app.route("/plumbing")
def plumbing():
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="final",
        ) 
        cursor=connection.cursor()
        cursor.execute("select * from plumbing")
        result=cursor.fetchall()
        session['tab'] = 'plumbing'

        cursor.execute("select location from plumbing")
        locations=cursor.fetchall()

        locs = []
        for loc in locations:
            locs.append(loc[0])
        
        print(locs)
        locs = set(locs)
        print(locs)
        locations = list(locs)

        return render_template('carpenter.html', result=result,title="plumbing", locations=locations)
    except Exception as e:
        print(e)
        return render_template('carpenter.html')
    
@app.route("/electrical")
def electrical():
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="final",
        ) 
        cursor=connection.cursor()
        cursor.execute("select * from electrical")
        result=cursor.fetchall()
        session['tab'] = 'electrical'
        cursor.execute("select location from electrical")
        locations=cursor.fetchall()
        locs = []
        for loc in locations:
            locs.append(loc[0])
        print(locs)
        locs = set(locs)
        print(locs)
        locations = list(locs)
        return render_template('carpenter.html', result=result,title="electrical",locations=locations)
    except Exception as e:
        print(e)
        return render_template('carpenter.html')
    
@app.route("/painting")
def painting():
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="final",
        ) 
        cursor=connection.cursor()
        cursor.execute("select * from painting")
        result=cursor.fetchall()
        session['tab'] = 'painting'
        cursor.execute("select location from painting")
        locations=cursor.fetchall()
        locs = []
        for loc in locations:
            locs.append(loc[0])
        print(locs)
        locs = set(locs)
        print(locs)
        locations = list(locs)
        return render_template('carpenter.html', result=result,title="painting", locations=locations)
    except Exception as e:
        print(e)
        return render_template('carpenter.html')
    
@app.route("/maintenance")
def maintenance():
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="final",
        ) 
        cursor=connection.cursor()
        cursor.execute("select * from maintenance")
        result=cursor.fetchall()
        session['tab'] = 'maintenance'
        cursor.execute("select location from maintenance")
        locations=cursor.fetchall()
        locs = []
        for loc in locations:
            locs.append(loc[0])
        print(locs)
        locs = set(locs)
        print(locs)
        locations = list(locs)
        return render_template('carpenter.html', result=result,title="maintenance",locations=locations)
    except Exception as e:
        print(e)
        return render_template('carpenter.html')
    
@app.route('/update',methods=['GET','POST'])
def update():
    if request.method=="POST":
        name=request.form["name"]
        password=request.form["password"]
        confirmpassword=request.form["confirmpassword"]
        print(name,password,confirmpassword)
        try:
            connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="final",
            ) 
            cursor=connection.cursor()
            cursor.execute("update users set password='"+password+"'where name='"+name+"'" )
            connection.commit()
            return render_template('index.html',m="updated successfully")
        except Exception as e :
            return render_template('index.html',m="not updated")
        

@app.route('/ADD',methods=['GET','POST'])
def ADD():
    if request.method=="POST":
        map=request.form["map"]
        address=request.form["address"]
        shopname=request.form["shopname"]
        service=request.form["service"]
        phone=request.form["phone"]
        timing=request.form["timing"]
        ownername=request.form["ownername"]
        location=request.form["location"]
        Type=request.form["serviceavailable"]
        print(ownername,map,address,phone,shopname,location,timing,service)
        try:
            connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="final",
            ) 
            cursor=connection.cursor()
            if Type == 'carpentry':
                cursor.execute("insert into carpenter (ownername,map,phone,address,shopname,location,timing,services) values('"+ownername+"','"+map+"','"+phone+"','"+address+"','"+shopname+"','"+location+"','"+timing+"','"+service+"')")
                connection.commit()
            if Type == 'plumbing':
                cursor.execute("insert into plumbing (ownername,map,phone,address,shopname,location,timing,services) values('"+ownername+"','"+map+"','"+phone+"','"+address+"','"+shopname+"','"+location+"','"+timing+"','"+service+"')")
                connection.commit()
            if Type == 'painting':
                cursor.execute("insert into painting (ownername,map,phone,address,shopname,location,timing,services) values('"+ownername+"','"+map+"','"+phone+"','"+address+"','"+shopname+"','"+location+"','"+timing+"','"+service+"')")
                connection.commit()
            
            if Type == 'maintenance':
                cursor.execute("insert into maintenance (ownername,map,phone,address,shopname,location,timing,services) values('"+ownername+"','"+map+"','"+phone+"','"+address+"','"+shopname+"','"+location+"','"+timing+"','"+service+"')")
                connection.commit()
            
            if Type == 'electrical':
                cursor.execute("insert into electrical (ownername,map,phone,address,shopname,location,timing,services) values('"+ownername+"','"+map+"','"+phone+"','"+address+"','"+shopname+"','"+location+"','"+timing+"','"+service+"')")
                connection.commit()
            
            cursor.close()
            connection.close()
            return render_template('mainindex.html')
        except Exception as e :
            print("error in connecting to the server"+str(e))
            return render_template('mainindex.html')
    return render_template('mainindex.html')

@app.route('/home')
def home():
    return render_template('mainindex.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
