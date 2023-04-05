# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 21:55:14 2023

@author: weste
"""

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
from flask_login import LoginManager, UserMixin, login_user, \
    logout_user, current_user, login_required


app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = "secret"

USER = 'ESSWebsite2023'
PASSWORD = 'ConergyDonation'
HOST = 'ESSWebsite2023.mysql.pythonanywhere-services.com'
DATABASE = 'ESSWebsite2023$EES'

'''
db = MySQLdb.connect(user=USER, db=DATABASE, passwd=PASSWORD, host=HOST)
'''

try:
    connection = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Wrong name/password", flush=True)
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist", flush=True)
    else:
        print(err)
else:
    print("connected: connection successful", flush=True)
    #connection.close()


class Module:
    id = 0
    donor = ""
    serialNumber = 0
    ratedWatts = 0
    moduleManu = ""
    model = ""
    weight = 0.0
    panelDimensionL= 0
    panelDimensionW=0
    panelDimensionD=0
    vmp = 0
    imp = 0
    voc = 0
    isc = 0
    pmpTemp = 0
    year = ""
    loaction = ""
    legacyVoc = 0
    legacyExpectedVoc = 0
    legacyIsc = 0
    legacyExpectedIsc = 0
    Irradiance = 0
    cellTemp = 0
    measuredpmp = 0
    expectedpmp = 0
    newpmp = 0
    measuredVocIsc = 0
    expectedVocIsc = 0
    newVocIsc = 0
    legacyInfrared = ""
    corrosion = 0
    cellCracks = 0
    evaBrowning = ""
    patternBrowning = ""
    frameDamage = ""
    frameSeal = ""
    jboxDamage = ""
    jboxloose = ""
    nameplate = ""
    backsideCracks = ""
    backsideBubbles = ""
    backsideTears = ""
    backsideChalking = ""
    frontsideBurn = ""
    backsideBurn = ""
    frontsideGlass = ""
    delamination = ""
    milkyDiscolor = ""
    residualMetal = ""
    snailTracks = ""
    snailTracksRes = ""
    futureDefect = ""
    futureDefectTwo = ""
    futureDefectThree = ""
    infrared = ""
    ultraviolet = ""
    finalDisposition = ""

def queryall():
    global connection
    module = Module()
    cursor = connection.cursor()
    query = "SELECT * FROM solar_module_tracking"
    cursor.execute(query)
    units=cursor.fetchall()
    #close the cursor after you grab your data
    cursor.close()
    print(units)
    modules=[]
    for row in units:
        module.donor = row[0]
        module.serialNumber = row[1]
        module.ratedWatts = row[2]
        module.moduleManu = row[3]
        module.model = row[4]
        module.weight = row[5]
        module.panelDimensionL = row[6]
        module.panelDimensionW = row[7]
        module.panelDimensionD = row [8]
        module.vmp = row[9]
        module.imp = row[10]
        module.voc = row[11]
        module.isc = row[12]
        module.pmpTemp = row[13]
        module.year = row[14]
        module.location = row[15]
        module.Irradiance = row[16]
        module.cellTemp = row[17]
        module.measuredpmp = row[18]
        module.expectedpmp = row[19]
        module.newpmp = row [20]
        module.id = row[21]
        id = row[21]

        #add legacy data associated with same module
        print(id)
        cursor = connection.cursor()
        query = "SELECT * FROM legacy_data WHERE Id = %s"
        cursor.execute(query, (id,))
        legacy=cursor.fetchall()
        #close the cursor after you grab your data
        cursor.close()
        print(legacy)
        for l in legacy:
            module.legacyVoc = l[0]
            module.legacyExpectedVoc = l[1]
            module.legacyIsc = l[2]
            module.legacyExpectedIsc = l[3]
            module.measuredVocIsc = l[4]
            module.expectedVocIsc = l[5]
            module.newVocIsc = l[6]
            module.legacyInfrared = l[7]

        #add the defect modes for the same module
        cursor = connection.cursor()
        query = "SELECT * FROM defect_modes WHERE Id = %s"
        cursor.execute(query, (id,))
        defects=cursor.fetchall()
        #close the cursor after you grab your data
        cursor.close()
        for defect in defects:
            module.corrosion = defect[0]
            module.cellCracks = defect[1]
            module.evaBrowning = defect[2]
            module.patternBrowning = defect[3]
            module.frameDamage = defect[4]
            module.frameSeal = defect[5]
            module.jboxDamage = defect[6]
            module.jboxloose = defect[7]
            module.nameplate = defect[8]
            module.backsideCracks = defect[9]
            module.backsideBubble = defect[10]
            module.backsideTears = defect[11]
            module.backsideChalking = defect[12]
            module.frontsideBurn = defect[13]
            module.backsideBurn = defect[14]
            module.frontsideGlass = defect[15]
            module.delamination = defect[16]
            module.milkyDiscolor = defect[17]
            module.residualMetal = defect[18]
            module.snailTracks = defect[19]
            module.snailTracksRes = defect[20]
            module.futureDefect = defect[21]
            module.futureDefectTwo = defect[22]
            module.futureDefectThree = defect[23]
            module.infrared = defect[24]
            module.ultraviolet = defect[25]

            #add final disposition for the same module
            cursor = connection.cursor()
            query = "SELECT * FROM final_disposition WHERE Id = %s"
            cursor.execute(query, (id,))
            disposition=cursor.fetchall()
            #close the cursor after you grab your data
            cursor.close()
            for d in disposition:
                module.disposition = d[3]
        modules.append(module)
        return modules

'''
login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(uid):
    print("in load_user")
    global connection
    cursor = connection.cursor()
    query = "SELECT Pass FROM user_login WHERE id = %s"
    cursor.execute(query, (uid,))
    user=cursor.fetchone()
    cursor.close()
    print(user)
    return user
    '''


@app.route('/')
def home():
    a= False
    #a = current_user.is_authenticated
    return render_template("home.html", a=a)


@app.route('/login', methods=['GET','POST'])
def login():
    #a = current_user.is_authenticated
    a= False
    global connection
    if request.method =="POST":
        print("hey")
        username = request.form['username']
        password = request.form['password']
        try:
            #open a cursor to the database
            cursor = connection.cursor()
            query = "SELECT Pass FROM user_login WHERE Username = %s"
            cursor.execute(query, (username,))
            user=cursor.fetchall()
            #close the cursor after you grab your data
            cursor.close()
            print("user:")
            print(len(user))
            if len(user) != 0:
                for row in user:
                    userpass = row[0]
                if password == userpass:
                    print("ugh I made it here")
                    cursor = connection.cursor()
                    query = "SELECT id FROM user_login WHERE Username = %s AND Pass = %s"
                    cursor.execute(query, (username, userpass))
                    user=cursor.fetchone()
                    cursor.close()
                    print(user[0])
                    print("hey there")
                    login_user(user[0])
                    print("done")
                    return render_template("home.html", a=a)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
    return render_template("login.html", a=a)

@app.route("/create")
#@login_required
def create():
    #a = current_user.is_authenticated
    a= False
    return render_template("create.html", a=a)

@app.route("/update")
def update():
    #a = current_user.is_authenticated
    a= False
    global connection
    module = Module()
    cursor = connection.cursor()
    query = "SELECT * FROM solar_module_tracking"
    cursor.execute(query)
    units=cursor.fetchall()
    #close the cursor after you grab your data
    cursor.close()
    print(units)
    modules=[]
    for row in units:
        module.donor = row[0]
        module.serialNumber = row[1]
        module.ratedWatts = row[2]
        module.moduleManu = row[3]
        module.model = row[4]
        module.weight = row[5]
        module.panelDimensionL = row[6]
        module.panelDimensionW = row[7]
        module.panelDimensionD = row [8]
        module.vmp = row[9]
        module.imp = row[10]
        module.voc = row[11]
        module.isc = row[12]
        module.pmpTemp = row[13]
        module.year = row[14]
        module.location = row[15]
        module.Irradiance = row[16]
        module.cellTemp = row[17]
        module.measuredpmp = row[18]
        module.expectedpmp = row[19]
        module.newpmp = row [20]
        module.id = row[21]
        id = row[21]

        #add legacy data associated with same module
        print(id)
        cursor = connection.cursor()
        query = "SELECT * FROM legacy_data WHERE Id = %s"
        cursor.execute(query, (id,))
        legacy=cursor.fetchall()
        #close the cursor after you grab your data
        cursor.close()
        print(legacy)
        for l in legacy:
            module.legacyVoc = l[0]
            module.legacyExpectedVoc = l[1]
            module.legacyIsc = l[2]
            module.legacyExpectedIsc = l[3]
            module.measuredVocIsc = l[4]
            module.expectedVocIsc = l[5]
            module.newVocIsc = l[6]
            module.legacyInfrared = l[7]

        #add the defect modes for the same module
        cursor = connection.cursor()
        query = "SELECT * FROM defect_modes WHERE Id = %s"
        cursor.execute(query, (id,))
        defects=cursor.fetchall()
        #close the cursor after you grab your data
        cursor.close()
        for defect in defects:
            module.corrosion = defect[0]
            module.cellCracks = defect[1]
            module.evaBrowning = defect[2]
            module.patternBrowning = defect[3]
            module.frameDamage = defect[4]
            module.frameSeal = defect[5]
            module.jboxDamage = defect[6]
            module.jboxloose = defect[7]
            module.nameplate = defect[8]
            module.backsideCracks = defect[9]
            module.backsideBubble = defect[10]
            module.backsideTears = defect[11]
            module.backsideChalking = defect[12]
            module.frontsideBurn = defect[13]
            module.backsideBurn = defect[14]
            module.frontsideGlass = defect[15]
            module.delamination = defect[16]
            module.milkyDiscolor = defect[17]
            module.residualMetal = defect[18]
            module.snailTracks = defect[19]
            module.snailTracksRes = defect[20]
            module.futureDefect = defect[21]
            module.futureDefectTwo = defect[22]
            module.futureDefectThree = defect[23]
            module.infrared = defect[24]
            module.ultraviolet = defect[25]

            #add final disposition for the same module
            cursor = connection.cursor()
            query = "SELECT * FROM final_disposition WHERE Id = %s"
            cursor.execute(query, (id,))
            disposition=cursor.fetchall()
            #close the cursor after you grab your data
            cursor.close()
            for d in disposition:
                module.disposition = d[3]
        modules.append(module)
    return render_template("update.html", a=a, modules=modules)

@app.route("/delete")
def delete():
    #a = current_user.is_authenticated
    a= False
    '''
    global connection
    module = Module()
    cursor = connection.cursor()
    query = "SELECT * FROM solar_module_tracking"
    cursor.execute(query)
    units=cursor.fetchall()
    #close the cursor after you grab your data
    cursor.close()
    print(units)
    modules=[]
    for row in units:
        module.donor = row[0]
        module.serialNumber = row[1]
        module.ratedWatts = row[2]
        module.moduleManu = row[3]
        module.model = row[4]
        module.weight = row[5]
        module.panelDimensionL = row[6]
        module.panelDimensionW = row[7]
        module.panelDimensionD = row [8]
        module.vmp = row[9]
        module.imp = row[10]
        module.voc = row[11]
        module.isc = row[12]
        module.pmpTemp = row[13]
        module.year = row[14]
        module.location = row[15]
        module.Irradiance = row[16]
        module.cellTemp = row[17]
        module.measuredpmp = row[18]
        module.expectedpmp = row[19]
        module.newpmp = row [20]
        module.id = row[21]
        id = row[21]

        #add legacy data associated with same module
        print(id)
        cursor = connection.cursor()
        query = "SELECT * FROM legacy_data WHERE Id = %s"
        cursor.execute(query, (id,))
        legacy=cursor.fetchall()
        #close the cursor after you grab your data
        cursor.close()
        print(legacy)
        for l in legacy:
            module.legacyVoc = l[0]
            module.legacyExpectedVoc = l[1]
            module.legacyIsc = l[2]
            module.legacyExpectedIsc = l[3]
            module.measuredVocIsc = l[4]
            module.expectedVocIsc = l[5]
            module.newVocIsc = l[6]
            module.legacyInfrared = l[7]

        #add the defect modes for the same module
        cursor = connection.cursor()
        query = "SELECT * FROM defect_modes WHERE Id = %s"
        cursor.execute(query, (id,))
        defects=cursor.fetchall()
        #close the cursor after you grab your data
        cursor.close()
        for defect in defects:
            module.corrosion = defect[0]
            module.cellCracks = defect[1]
            module.evaBrowning = defect[2]
            module.patternBrowning = defect[3]
            module.frameDamage = defect[4]
            module.frameSeal = defect[5]
            module.jboxDamage = defect[6]
            module.jboxloose = defect[7]
            module.nameplate = defect[8]
            module.backsideCracks = defect[9]
            module.backsideBubble = defect[10]
            module.backsideTears = defect[11]
            module.backsideChalking = defect[12]
            module.frontsideBurn = defect[13]
            module.backsideBurn = defect[14]
            module.frontsideGlass = defect[15]
            module.delamination = defect[16]
            module.milkyDiscolor = defect[17]
            module.residualMetal = defect[18]
            module.snailTracks = defect[19]
            module.snailTracksRes = defect[20]
            module.futureDefect = defect[21]
            module.futureDefectTwo = defect[22]
            module.futureDefectThree = defect[23]
            module.infrared = defect[24]
            module.ultraviolet = defect[25]

            #add final disposition for the same module
            cursor = connection.cursor()
            query = "SELECT * FROM final_disposition WHERE Id = %s"
            cursor.execute(query, (id,))
            disposition=cursor.fetchall()
            #close the cursor after you grab your data
            cursor.close()
            for d in disposition:
                module.disposition = d[3]
        modules.append(module)
    print(modules)
    '''
    modules = queryall()
    return render_template("delete.html", a=a,modules=modules)


@app.route("/view", methods=['GET','POST'])
def view():
    a= False
    #a = current_user.is_authenticated
    if request.method =="POST":
        searchParameter = request.form['search']
        print(searchParameter)
        if searchParameter == "all":
            modules = queryall()
            return render_template("view.html", a=a, modules=modules)
    return render_template("view.html", a=a)

@app.route('/logout', methods=['GET','POST'])
def logout():
    a= False
    #a = current_user.is_authenticated
    if request.method == "POST":
        logout_user()
        print("successfully logged out")
    return render_template("logout.html", a=a)

if __name__ == '__main__':
    app.run(port=5050)