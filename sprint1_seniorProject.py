# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 21:55:14 2023

@author: weste
"""

from flask import Flask, render_template, request, redirect, url_for,session
import mysql.connector
from mysql.connector import errorcode
from flask_login import LoginManager, UserMixin, login_user, \
    logout_user, current_user, login_required
import config
import csv
import time


app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY']=config.SECRETKEY

USER = config.USER
PASSWORD = config.PASSWORD
HOST = config.HOST
DATABASE = config.DATABASE

def createConnection():
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
        return connection


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
    location = ""
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
    comments = ""

class User(UserMixin):
    def __init__(self, username, password):
        self.Username = username
        self.Pass = password
        self._authenticated = False

    def is_authenticated(self):
        return self._authenticated

    def is_active(self):
        return True

    def is_annonymous(self):
        return False

    def get_id(self):
        connection = createConnection()
        cursor = connection.cursor()
        query = "SELECT * FROM user_login WHERE Username = %s"
        cursor.execute(query, (self.Username,))
        users=cursor.fetchall()
        #close the cursor after you grab your data
        cursor.close()
        self._authenticated = True
        for row in users:
            uname = row[0]
            u_pass = row[1]
            u_id = row[2]
        user = User(uname,u_pass)
        return user



def queryall():
    connection = createConnection()
    module = Module()
    cursor = connection.cursor(buffered=True)
    query = "SELECT * FROM solar_module"
    cursor.execute(query)
    connection.commit()
    units=cursor.fetchall()
    #close the cursor after you grab your data
    cursor.close()
    #print("units:")
    #print(units)
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
        #print(id)
        cursor = connection.cursor(buffered=True)
        query = "SELECT * FROM legacyData WHERE Id = %s"
        cursor.execute(query, (id,))
        connection.commit()
        legacy=cursor.fetchall()
        #close the cursor after you grab your data
        cursor.close()
        #print(legacy)
        for l in legacy:
            module.legacyVoc = l[0]
            module.legacyExpectedVoc = l[1]
            module.legacyIsc = l[2]
            module.legacyExpectedIsc = l[3]
            module.measuredVocIsc = l[4]
            module.expectedVocIsc = l[5]
            module.newVocIsc = l[9]
            module.legacyInfrared = l[6]

        #add the defect modes for the same module
        cursor = connection.cursor()
        query = "SELECT * FROM defectModes WHERE Id = %s"
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
            query = "SELECT * FROM finalDisposition WHERE Id = %s"
            cursor.execute(query, (id,))
            disposition=cursor.fetchall()
            #close the cursor after you grab your data
            cursor.close()
            for d in disposition:
                module.disposition = d[1]
                module.comments = d[2]
        copyModule = Module()
        copyModule = module
        modules.append(copyModule)
        module = Module()
    connection.close()
    return modules

def queryByObject(name, searchObject):
    connection = createConnection()
    module = Module()
    cursor = connection.cursor()
    query = ""
    if (name == "donor"):
        query = "SELECT * FROM solar_module WHERE donor=%s"
    if (name == "serial"):
        query = "SELECT * FROM solar_module WHERE serial=%s"
    if (name == "manufacturer"):
        query = "SELECT * FROM solar_module WHERE Module_manufacturer=%s"
    if (name == "model"):
        query = "SELECT * FROM solar_module WHERE Module=%s"
    if (name == "id"):
        query = "SELECT * FROM solar_module WHERE Id=%s"
    if (name == "location"):
        query = "SELECT * FROM solar_module WHERE Location=%s"
    cursor.execute(query,(searchObject,))
    units=cursor.fetchall()
    #close the cursor after you grab your data
    cursor.close()
    #print(units)
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
        query = "SELECT * FROM legacyData WHERE Id = %s"
        cursor.execute(query, (id,))
        legacy=cursor.fetchall()
        #close the cursor after you grab your data
        cursor.close()
        #print(legacy)
        for l in legacy:
            module.legacyVoc = l[0]
            module.legacyExpectedVoc = l[1]
            module.legacyIsc = l[2]
            module.legacyExpectedIsc = l[3]
            module.measuredVocIsc = l[4]
            module.expectedVocIsc = l[5]
            module.newVocIsc = l[9]
            module.legacyInfrared = l[6]

        #add the defect modes for the same module
        cursor = connection.cursor()
        query = "SELECT * FROM defectModes WHERE Id = %s"
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
            query = "SELECT * FROM finalDisposition WHERE Id = %s"
            cursor.execute(query, (id,))
            disposition=cursor.fetchall()
            #close the cursor after you grab your data
            cursor.close()
            for d in disposition:
                module.disposition = d[1]
                module.comments = d[2]
        copyModule = Module()
        copyModule = module
        modules.append(copyModule)
        module = Module()
    connection.close()
    return modules


'''
login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(uid):
    print("in load_user")
    return uid
'''


@app.route('/')
def home():
    #global loggedin
    #a = loggedin
    if 'loggedin' in session:
        a = True
    else:
        a= False
    #a = current_user.is_authenticated
    return render_template("home.html", a=a)


@app.route('/login', methods=['GET','POST'])
def login():
    #a = current_user.is_authenticated
    #global loggedin
    #a = loggedin
    if 'loggedin' in session:
        a = True
    else:
        a =False
    if(a == True):
        return redirect(url_for("home"))
    connection = createConnection()
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
                    session['loggedin'] = True
                    return redirect(url_for('home'))
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
    return render_template("login.html", a=a)

@app.route("/create", methods=['GET','POST'])
#@login_required
def create():
    #a = current_user.is_authenticated
    #a= False
    if 'loggedin' in session:
        a = True
        donor = ""
        model = ""
        panelManufacturer = ""
    else:
        return redirect(url_for("login"))
    connection = createConnection()
    if request.method == "POST":
        donor = request.form['donor']
        serial = request.form['serialNumber']
        ratedWatts = request.form['ratedWatts']
        panelManufacturer = request.form['panelManufacturer']
        model = request.form['model']
        weight = request.form['weight']
        length = request.form['length']
        width = request.form['width']
        depth = request.form['depth']
        vmp = request.form['vmp']
        imp = request.form['imp']
        voc = request.form['voc']
        isc = request.form['isc']
        pmpTemp = request.form['pmpTemp']
        year = request.form['year']
        location = request.form['location']
        irradiance = request.form['irradiance']
        cellTemp= request.form['cellTempC']
        measuredPmp = request.form['pmp']
        PmpExpected = (irradiance/1000)*ratedWatts+(ratedWatts*pmpTemp*(irradiance/1000)*(cellTemp-25))

        cursor = connection.cursor()
        query = 'INSERT INTO solar_module\
                    (donor, serial, Rated_watts, Module_manufacturer, Module,\
                    Weight_kg, Panel_Dimensions_L, Panel_Dimensions_W, Panel_Dimensions_D,\
                    VMP, IMP, Voc, Isc,pmpTemp, Year_of_Manufacture, Location,\
                    Irradiance, Cell_Temp_C, Measured_Pmp_watts,Pmp_Watts_Expected)\
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(query, (donor,serial,ratedWatts,panelManufacturer,model,weight,length,width,depth,vmp,imp,voc,isc,pmpTemp,year,location,irradiance,cellTemp,measuredPmp,PmpExpected))
        connection.commit()
        cursor.close()

        corrosion = request.form['corrosion']
        cracks = request.form['cracks']
        evaBrowning = request.form['evaBrowning']
        patternBrowning = request.form['patternBrowning']
        frameDamage = request.form['frameDamage']
        frameSeal = request.form['frameSeal']
        jBoxDamage = request.form['jBoxDamage']
        jBoxLoose = request.form['jBoxLoose']
        nameplate = request.form['nameplate']
        backsideCracks = request.form['backsideCracks']
        backsideBubbles = request.form['backsideBubbles']
        backsideTears = request.form['backsideTears']
        backsideChalking = request.form['backsideChalking']
        frontsideBurn = request.form['frontsideBurn']
        backsideBurn = request.form['backsideBurn']
        frontsideGlass = request.form['frontsideGlass']
        delamination = request.form['delamination']
        milky = request.form['milky']
        residualMetal = request.form['residualMetal']
        snailTracks = request.form['snailTracks']
        snailTracksRes = request.form['snailTracksRes']
        defectOne = request.form['defectOne']
        defectTwo = request.form['defectTwo']
        defectThree = request.form['defectThree']
        infrared = request.form['infrared']
        ultraviolet = request.form['ultraviolet']

        #scarch-chip-crack
        cursor = connection.cursor()
        query = 'INSERT INTO defectModes\
                    (Corrosion_cells, Cell_Cracks, EVA_Browning, Pattern_of_Browning, Frame_Damage,\
                    Frame_Seal, Jbox_Damage, Jbox_Loose, Nameplate_Faded_Missing, Backside_Cracks,\
                    Backside_Bubbles, Backside_Tears_Scratches,Backside_Chalking,Frontside_Burn_Mark,Backside_Burn_Mark,\
                    Frontside_Glass, Delamination, Milky_Discoloration, Residual_Metal,Snail_Tracks, Snail_Tracks_Resid, Future_Defect_1,\
                    Future_Defect_2, Future_Defect_3, Infrared, Ultraviolet,id)\
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,(SELECT MAX(Id)FROM solar_module))'
        cursor.execute(query, (corrosion,cracks,evaBrowning,patternBrowning,frameDamage,frameSeal,jBoxDamage,jBoxLoose,nameplate,backsideCracks,backsideBubbles,backsideTears,backsideChalking,frontsideBurn,backsideBurn,frontsideGlass,delamination,milky,residualMetal,snailTracks,snailTracksRes,defectOne,defectTwo,defectThree,infrared,ultraviolet))
        connection.commit()
        cursor.close()

        finalDisposition = request.form['disposition']
        comments = request.form['comments']

        #add in final disposition when we iron that out
        cursor = connection.cursor()
        query = 'INSERT INTO finalDisposition\
            (Final_Disposition,Comments,id)\
            VALUES (%s,%s,(SELECT MAX(Id)FROM solar_module))'
        cursor.execute(query,(finalDisposition, comments))
        connection.commit()
        cursor.close()

        connection.close()

        repeat = request.form['continue']
        if (repeat == "no"):
            donor = ""
            model = ""
            panelManufacturer = ""
    return render_template("create.html", a=a, donor=donor, model=model,panelManufacturer=panelManufacturer)

@app.route("/update", methods=['GET','POST'])
def update():
    #a = current_user.is_authenticated
    #a= False
    if 'loggedin' in session:
        a = True
    else:
        return redirect(url_for("login"))
    if request.method =="POST":
        searchParameter = request.form['search']
        print(searchParameter)
        if searchParameter == "all":
            modules = queryall()
            return render_template("update.html", a=a, modules=modules)
        if searchParameter == "donor":
            donor = request.form['searchValue']
            modules = queryByObject("donor", donor)
            return render_template("update.html", a=a, modules=modules)
        if searchParameter == "serial":
            serial = request.form['searchValue']
            modules = queryByObject("serial", serial)
            return render_template("update.html", a=a, modules=modules)
        if searchParameter == "manufacturer":
            manufacturer = request.form['searchValue']
            modules = queryByObject("manufacturer", manufacturer)
            return render_template("update.html", a=a, modules=modules)
        if searchParameter == "Model":
            model = request.form['searchValue']
            modules = queryByObject("model", model)
            return render_template("update.html", a=a, modules=modules)
        if searchParameter == "location":
            model = request.form['searchValue']
            modules = queryByObject("location",model)
            return render_template("update.html", a=a, modules=modules)
    return render_template("update.html", a=a)

@app.route('/update/<id>', methods=['GET','POST'])
def updateEntry(id):
    #a = current_user.is_authenticated
    #a= False
    if 'loggedin' in session:
        a = True
    else:
        return redirect(url_for("login"))
    connection = createConnection()
    print(id)
    if request.method == "GET":
        modules = queryByObject("id",id)
        return render_template("updateForm.html",a=a,modules=modules)
    if request.method == "POST":
        cursor = connection.cursor()
        #add serial after the column name fixed
        #add Pmp_Watts_Expected = %s, %_of_New_Pmp = %s calculations later
        donor = request.form['donor']
        serial = request.form['serialNumber']
        ratedWatts = request.form['ratedWatts']
        panelManufacturer = request.form['panelManufacturer']
        model = request.form['model']
        weight = request.form['weight']
        length = request.form['length']
        width = request.form['width']
        depth = request.form['depth']
        vmp = request.form['vmp']
        imp = request.form['imp']
        voc = request.form['voc']
        isc = request.form['isc']
        pmpTemp = request.form['pmpTemp']
        year = request.form['year']
        location = request.form['location']
        irradiance = request.form['irradiance']
        cellTemp= request.form['cellTempC']
        measuredPmp = request.form['pmp']
        PmpExpected = (irradiance/1000)*ratedWatts+(ratedWatts*pmpTemp*(irradiance/1000)*(cellTemp-25))

        print("voc: " + str(voc))
        print("vmp: " + str(vmp))
        print("id: " + str(id))
        #update table one
        query = "UPDATE solar_module\
                    SET donor = %s, serial = %s, Rated_watts = %s, Module_manufacturer = %s, Module = %s,\
                    Weight_kg = %s, Panel_Dimensions_L = %s, Panel_Dimensions_W = %s, Panel_Dimensions_D = %s,\
                    VMP = %s, IMP = %s, Voc = %s, Isc = %s,pmpTemp = %s, Year_of_Manufacture = %s, Location=%s,\
                    Irradiance = %s, Cell_Temp_C = %s, Measured_Pmp_watts = %s, Pmp_Watts_Expected=%s\
                    WHERE Id = %s"
        cursor.execute(query, (donor,serial,ratedWatts,panelManufacturer,model,weight,length,width,depth,vmp,imp,voc,isc,pmpTemp,year,location,irradiance,cellTemp,measuredPmp,PmpExpected,id))
        connection.commit()
        cursor.close()

        #update defect modes
        corrosion = request.form['corrosion']
        cracks = request.form['cracks']
        evaBrowning = request.form['evaBrowning']
        patternBrowning = request.form['patternBrowning']
        frameDamage = request.form['frameDamage']
        frameSeal = request.form['frameSeal']
        jBoxDamage = request.form['jBoxDamage']
        jBoxLoose = request.form['jBoxLoose']
        nameplate = request.form['nameplate']
        backsideCracks = request.form['backsideCracks']
        backsideBubbles = request.form['backsideBubbles']
        backsideTears = request.form['backsideTears']
        backsideChalking = request.form['backsideChalking']
        frontsideBurn = request.form['frontsideBurn']
        backsideBurn = request.form['backsideBurn']
        frontsideGlass = request.form['frontsideGlass']
        delamination = request.form['delamination']
        milky = request.form['milky']
        residualMetal = request.form['residualMetal']
        snailTracks = request.form['snailTracks']
        snailTracksRes = request.form['snailTracksRes']
        defectOne = request.form['defectOne']
        defectTwo = request.form['defectTwo']
        defectThree = request.form['defectThree']
        infrared = request.form['infrared']
        ultraviolet = request.form['ultraviolet']

        #scarch-chip-crack
        cursor = connection.cursor()
        query = "UPDATE defectModes\
                    SET Corrosion_cells = %s, Cell_Cracks = %s, EVA_Browning = %s, Pattern_of_Browning = %s, Frame_Damage= %s,\
                    Frame_Seal = %s, Jbox_Damage = %s, Jbox_Loose = %s, Nameplate_Faded_Missing = %s, Backside_Cracks = %s,\
                    Backside_Bubbles = %s, Backside_Tears_Scratches = %s,Backside_Chalking  = %s,Frontside_Burn_Mark = %s,Backside_Burn_Mark = %s, Frontside_Burn_Mark = %s,\
                    Frontside_Glass = %s, Delamination = %s, Milky_Discoloration = %s, Residual_Metal = %s,Snail_Tracks=%s, Snail_Tracks_Resid=%s, Future_Defect_1=%s,\
                    Future_Defect_2=%s, Future_Defect_3=%s, Infrared=%s, Ultraviolet=%s\
                    WHERE Id = %s"
        cursor.execute(query, (corrosion,cracks,evaBrowning,patternBrowning,frameDamage,frameSeal,jBoxDamage,jBoxLoose,nameplate,backsideCracks,backsideBubbles,backsideTears,backsideChalking,\
                                frontsideBurn,backsideBurn,frontsideBurn,frontsideGlass,delamination,milky,residualMetal,snailTracks,snailTracksRes,defectOne,defectTwo,defectThree,infrared,ultraviolet,id))
        connection.commit()
        cursor.close()

        #add final disposition
        finalDisposition = request.form['disposition']
        comments = request.form['comments']

        cursor = connection.cursor()
        query = "UPDATE finalDisposition\
                    SET Final_Disposition = %s, Comments = %s\
                    WHERE Id = %s"
        cursor.execute(query,(finalDisposition, comments,id))
        connection.commit()
        cursor.close()
        connection.close()
    return redirect(url_for("view"))

@app.route("/delete", methods=['GET','POST'])
def delete():
    #a = current_user.is_authenticated
    #a= False
    if 'loggedin' in session:
        a = True
    else:
        return redirect(url_for("login"))
    if request.method =="POST":
        searchParameter = request.form['search']
        print(searchParameter)
        if searchParameter == "all":
            modules = queryall()
            return render_template("delete.html", a=a, modules=modules)
        if searchParameter == "donor":
            donor = request.form['searchValue']
            modules = queryByObject("donor", donor)
            return render_template("delete.html", a=a, modules=modules)
        if searchParameter == "serial":
            serial = request.form['searchValue']
            modules = queryByObject("serial", serial)
            return render_template("delete.html", a=a, modules=modules)
        if searchParameter == "manufacturer":
            manufacturer = request.form['searchValue']
            modules = queryByObject("manufacturer", manufacturer)
            return render_template("delete.html", a=a, modules=modules)
        if searchParameter == "Model":
            model = request.form['searchValue']
            modules = queryByObject("model", model)
            return render_template("delete.html", a=a, modules=modules)
        if searchParameter == "location":
            model = request.form['searchValue']
            modules = queryByObject("location",model)
            return render_template("delete.html", a=a, modules=modules)
    return render_template("delete.html", a=a)

@app.route('/delete/<id>')
def deleteEntry(id):
    print(id)
    print("In the /delete/id")
    connection = createConnection()

    #remove that row from legacy data
    cursor = connection.cursor()
    query = "DELETE FROM legacyData WHERE Id = %s"
    cursor.execute(query, (id,))
    connection.commit()
    cursor.close()

    #remove that row from defect modes
    cursor = connection.cursor()
    query = "DELETE FROM defectModes WHERE Id = %s"
    cursor.execute(query, (id,))
    connection.commit()
    cursor.close()

    #remove from final dispostion once that is sorted out!
    cursor = connection.cursor()
    query = "DELETE FROM finalDisposition WHERE Id = %s"
    cursor.execute(query, (id,))
    connection.commit()
    cursor.close()

    #remove that row from solar_module table
    cursor = connection.cursor()
    query = "DELETE FROM solar_module WHERE Id = %s"
    cursor.execute(query, (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("view"))


@app.route("/view", methods=['GET','POST'])
def view():
    #a= False
    #a = current_user.is_authenticated
    if 'loggedin' in session:
        a = True
    else:
        return redirect(url_for("login"))
    if request.method =="POST":
        searchParameter = request.form['search']
        print(searchParameter)
        action = request.form['type']
        print(action)
        if searchParameter == "all":
            modules = queryall()
            if action == "csv":
                timestr = time.strftime("%Y_%m_%d-%I_%M_%S_%p")
                filename = timestr + ".csv"
                with open(filename,'w',newline='')as f:
                    writer = csv.writer(f)
                    writer.writerow(['Donor','Serial number','Rated Watts', 'Module Manufacturer','Model','Weight kg','panel Dimension L', 'panel Dimension W', 'panel Dimension D',\
                    'Vmp','Imp','Voc','Isc','Pmp temp coeff %','year of manufacture','location/intended project', 'Voc','Expected','Isc','Expected','Irradiance','Cell Temp c','Measured Pmp',\
                    'Pmp watts Expected', '% of New Pmp','Measured Voc x Isc Watts','Expected Voc x Isc', '% of new Voc x Isc', 'infrared', 'corrosion # of cells', 'cell cracks # of cells',\
                    'Eva Browning', 'Pattern of Browning', 'Frame Damage', 'Frame seal','Jbox damage','Jbox Loose','Nameplate faded/mising','Backside crakcs', 'Backside Bubbles', 'Backside Tears',\
                    'Backside Chalking','Frontside Burn','Backside burn','Frontside glass-scratch/chip/crack','Delamination','Milky disoloration','residual metal','snail tracks-no resid', 'snail tracks -metal resid',\
                    'Future defect', 'future defect 2', 'future defect 3', 'infrared','ultraviolet','final disposition','Comments'])
                    for m in modules:
                        writer.writerow([m.donor,m.serialNumber,m.ratedWatts,m.moduleManu,m.model,m.weight,m.panelDimensionL,m.panelDimensionW,m.panelDimensionD,m.vmp,m.imp,m.voc,m.isc,\
                        m.pmpTemp,m.year,m.location,m.legacyVoc,m.legacyExpectedVoc,m.legacyIsc,m.legacyExpectedIsc,m.Irradiance,m.cellTemp,m.measuredpmp,m.expectedpmp,m.newpmp,m.measuredVocIsc,\
                        m.expectedVocIsc,m.newVocIsc,m.legacyInfrared,m.corrosion,m.cellCracks,m.evaBrowning,m.patternBrowning,m.frameDamage,m.frameSeal,m.jboxDamage,m.jboxloose,m.nameplate,\
                        m.backsideCracks,m.backsideBubbles,m.backsideTears,m.backsideChalking,m.frontsideBurn,m.backsideBurn,m.frontsideGlass,m.delamination,m.milkyDiscolor,m.residualMetal,\
                        m.snailTracks,m.snailTracksRes,m.futureDefect,m.futureDefectTwo,m.futureDefectThree,m.infrared,m.ultraviolet,m.finalDisposition,m.comments])
            return render_template("view.html", a=a, modules=modules)
        if searchParameter == "donor":
            donor = request.form['searchValue']
            modules = queryByObject("donor", donor)
            return render_template("view.html", a=a, modules=modules)
        if searchParameter == "serial":
            serial = request.form['searchValue']
            modules = queryByObject("serial", serial)
            return render_template("view.html", a=a, modules=modules)
        if searchParameter == "manufacturer":
            manufacturer = request.form['searchValue']
            modules = queryByObject("manufacturer", manufacturer)
            return render_template("view.html", a=a, modules=modules)
        if searchParameter == "Model":
            model = request.form['searchValue']
            modules = queryByObject("model", model)
            return render_template("view.html", a=a, modules=modules)
        if searchParameter == "location":
            model = request.form['searchValue']
            modules = queryByObject("location",model)
            return render_template("update.html", a=a, modules=modules)
    return render_template("view.html", a=a)



@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop("loggedin", None)
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(port=5050)