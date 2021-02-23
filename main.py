from flask  import Flask, render_template, request,session,send_from_directory,Response
from os import path
import pymysql
import os
import ctypes
from link_preview import link_preview


conn=pymysql.connect(host="localhost",user="root",password="root",db="linkpreview")
cursor=conn.cursor()
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app=Flask(__name__)
app.secret_key = 'jsbcdsjkvbdjkbvdjcbkjf'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/UserReg')
def UserReg():

    return render_template('UserReg.html')


@app.route('/UserRegister1',methods=['POST'])
def UserRegister1():
    target = os.path.join(APP_ROOT, 'images/')
    for upload in request.files.getlist("file"):
            name = request.form.get('name')
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            phone = request.form.get('phone')
            gender = request.form.get('gender')
            address = request.form.get('address')
            filename = upload.filename

            print(filename)
            destination = "/".join([target, filename])
            upload.save(destination)


            result = cursor.execute(
                " insert into ureg(name,username,email,password,phone,gender,address,pic)values('" + name + "','" + username + "','" + email + "','" + password + "','" + phone + "','" + gender + "','" + address + "','"+filename+"')");
            conn.commit()

            if result > 0:

                ctypes.windll.user32.MessageBoxW(0, "Registration Sucess", "Registration Status", "color:black;")
                return render_template('index.html')

            else:
                ctypes.windll.user32.MessageBoxW(0, "Registration Fails", "Registration Status", "color:black;")
                return render_template('UserReg.html')





@app.route('/UserLogin1')
def UserLogin1():
    username = request.args.get('username')
    password = request.args.get('password')

    result = cursor.execute(" select * from ureg where username='" + username + "' and password='" + password + "' ")
    userDetails=cursor.fetchall()
    conn.commit()

    if result > 0:

        for user in userDetails:
            email=user[3]
            id = user[0]
            print(email)

            session['username'] = user[2]
            session['email']=email
            session['id']=id
            ctypes.windll.user32.MessageBoxW(0, "Login Success", "Login Status", "color:black;")

            return render_template('userHome.html')


    else:
        ctypes.windll.user32.MessageBoxW(0, "Login Fails", "Login Status", "color:black;")

        return render_template('index.html')



@app.route('/Logout')
def Logout():
    session.pop('username', None)
    session.pop('email', None)
    session.pop('user_id', None)

    return render_template('index.html')



@app.route('/searchuser')
def searchuser():
    return render_template('searchuser.html')



@app.route('/searchuser1')
def searchuser1():
    username=request.args.get('username')
    a=cursor.execute("select * from ureg where username='"+username+"'")
    if a > 0:

        details=cursor.fetchall()
        return render_template('searchresult.html',userdetails=details)
    else:
        ctypes.windll.user32.MessageBoxW(0, "Based on Searching Name Profile details are not available", "Search Status", "color:black;")

        return render_template('searchuser.html')


@app.route('/sendRequest')
def sendRequest():
    reqto=request.args.get('reqto')
    reqtoid = request.args.get('reqtoid')
    reqfrom=session['username']
    print(reqfrom)
    if reqto == reqfrom:
        ctypes.windll.user32.MessageBoxW(0,
                                         "You Cant Send Friend request",
                                         "Request status",
                                         "color:black;")
        return searchuser()


    else:

        c=cursor.execute("select * from friendreq where reqto='"+reqto+"' or reqfrom='"+reqfrom+"' and status='accept'")

        b=cursor.execute("select * from friendreq where reqto='"+reqto+"' or reqfrom='"+reqfrom+"'")
        if b > 0:
            #return  render_template('userMessage.html',msg="you already send friend request waitng for response")
            ctypes.windll.user32.MessageBoxW(0,
                                             "You are already sent friend Request Please wait the response",
                                             "Request status",
                                             "color:black;")
            return searchuser()
        elif c > 0:
            #return  render_template('userMessage.html',msg="you already  friend")
            ctypes.windll.user32.MessageBoxW(0,
                                             "You are already friend",
                                             "Request status",
                                             "color:black;")
            return searchuser()
        else:

            a=cursor.execute("insert into friendreq(reqto,reqtoid,reqfrom) values('"+reqto+"','"+reqtoid+"','"+reqfrom+"')")
            conn.commit()

            if a  > 0:
                #return render_template('userMessage.html', msg="Friend Request Sent Sucessfully")
                ctypes.windll.user32.MessageBoxW(0,
                                                 "Request sent Success",
                                                 "Request status",
                                                 "color:black;")
                return searchuser()
            else:
                #return render_template('userMessage.html', msg="Friend Request sent fails")
                ctypes.windll.user32.MessageBoxW(0,
                                                 "Request sent Fails",
                                                 "Request status",
                                                 "color:black;")
                return searchuser()




@app.route('/viewFriendreqdel')
def viewFriendreqdel():
    reqto=session['username']
    a=cursor.execute("select * from friendreq where reqto='"+reqto+"' and status='pending'")
    details=cursor.fetchall()
    if a > 0:
        return render_template('viewFriendRequest.html',reqdetails=details)
    else:
        ctypes.windll.user32.MessageBoxW(0,
                                         "Request Details arenot available",
                                         "Request status",
                                         "color:black;")
        return searchuser()


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/clickhere')
def clickhere():
    reqfrom=request.args.get('reqfrom')
    cursor.execute("select * from ureg where username='" + reqfrom + "'")
    details = cursor.fetchall()
    return render_template('userprofile.html', userdetails=details)


@app.route('/Acceptreq')
def Acceptreq():
    id = request.args.get('id')
    a=cursor.execute("update friendreq set status='accept' where id='"+id+"'")
    conn.commit()
    if a > 0:
        return viewFriendreqdel()
    else:
        ctypes.windll.user32.MessageBoxW(0,
                                         "Request Accepted Fails",
                                         "Request status",
                                         "color:black;")
        return viewFriendreqdel()

@app.route('/myfriends')
def myfriends():
    username=session['username']
    a=cursor.execute("select * from friendreq where reqfrom='"+username+"' or reqto='"+username+"' and status='accept'")
    details=cursor.fetchall()
    if a > 0 :
        return render_template('myfriends.html', userdetails=details)
    else:
        ctypes.windll.user32.MessageBoxW(0,
                                         "Request Details arenot available",
                                         "Request status",
                                         "color:black;")
        return render_template('userHome.html')


@app.route('/Chat')
def Chat():
    a=cursor.execute("select * from ureg where username !='"+session['username']+"' ")
    cdel=cursor.fetchall()
    if a > 0:
        return render_template('chat.html',cdel=cdel)
    else:
        ctypes.windll.user32.MessageBoxW(0,
                                         "Users are not available",
                                         "Request status",
                                         "color:black;")
        return render_template('userHome.html')


@app.route('/char')
def char():
    email=request.args.get('email')
    username = request.args.get('username')
    return render_template('char.html',email=email,username=username)




@app.route('/storeData')
def storeData():
    msgto=request.args.get('id')
    msg=request.args.get('msg')
    s=msg.__contains__('http')
    if s:
        print("i am true")
        dict_elem = link_preview.generate_dict(msg)  # this is a dict()

        # Access values
        title = dict_elem['title']
        description = dict_elem['description']
        image = dict_elem['image']
        website = dict_elem['website']
        a = cursor.execute("insert into chat(msgfrom,msgto,message,datee,title,descr,website,image) values('" + session[
            'email'] + "','" + msgto + "','" + msg + "',now(),'"+title+"','"+description+"','"+website+"','"+image+"')")
        conn.commit()
        if a > 0:
            return render_template('chat3.html', id=id, msg=msg)

        else:
            return render_template('chat3.html', id=id, msg=msg)
        print("i am false")
        print("am in storedata")
    else:
        a = cursor.execute("insert into chat(msgfrom,msgto,message,datee,title,descr,website,image) values('" + session[
            'email'] + "','" + msgto + "','" + msg + "',now(),'','','','')")
        conn.commit()
        if a > 0:
            return render_template('chat3.html', id=id, msg=msg)

        else:
            return render_template('chat3.html', id=id, msg=msg)
        print("i am false")
        print("am in storedata")
    '''
   
    '''

@app.route('/getdata')
def getdata():
    msgto=request.args.get('id')
    print(" am in get data")
    a=cursor.execute("select * from chat where (msgfrom='"+session['email']+"' and msgto='"+msgto+"') or (msgfrom='"+msgto+"' and msgto='"+session['email']+"')")
    mdel=cursor.fetchall()
    if a > 0:
        print(mdel)
        return render_template('getdata.html',mdel=mdel,msgto=msgto)




@app.route('/char1')
def char1():
    reqf=request.args.get('reqf')
    reft = request.args.get('reft')
    if session['username'] == reqf:
        cursor.execute("select * from ureg where username='"+reft+"' ")
        cdel=cursor.fetchall()
        for c in cdel:

            return render_template('char.html',email=c[3],username=c[2])
    elif session['username'] == reft:
        cursor.execute("select * from ureg where username='" + reqf + "' ")
        cdel = cursor.fetchall()
        for c in cdel:
            return render_template('char.html', email=c[3], username=c[2])




@app.route('/withImage')
def withImage():
    return render_template('makepost.html')





@app.route('/upload1',methods=['post'])
def upload1():
    print("hii 1")
    target = os.path.join(APP_ROOT, 'images/')
    print("hii2")
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        username=session['username']
        descr = request.form.get('descr')

        filename = upload.filename
        destination = "/".join([target, filename])
        upload.save(destination)
        data = [descr]


        a=cursor.execute("insert into post(postby,descr,image,datee) values('" + username + "','" + descr + "','" + upload.filename + "',now())")
        conn.commit()
        if a > 0:
            ctypes.windll.user32.MessageBoxW(0,
                                             "Image Posted Success",
                                             "Request status",
                                             "color:black;")
            return render_template('makepost.html')



        else:
            ctypes.windll.user32.MessageBoxW(0,
                                             "Image Posted Fails",
                                             "Request status",
                                             "color:black;")
            return render_template('makepost.html')


@app.route('/onlyText')
def onlyText():
    return render_template('onlyText.html')


@app.route('/text1',methods=['post'])
def text1():

        username=session['username']
        descr = request.form.get('descr')


        data = [descr]


        a=cursor.execute("insert into post(postby,descr,image,datee) values('" + username + "','" + descr + "','',now())")
        conn.commit()
        if a > 0:
            ctypes.windll.user32.MessageBoxW(0,
                                             "Text Posted Success",
                                             "Request status",
                                             "color:black;")
            return render_template('onlyText.html')



        else:
            ctypes.windll.user32.MessageBoxW(0,
                                             "text Posted Fails",
                                             "Request status",
                                             "color:black;")
            return render_template('onlyText.html')


@app.route('/userhome')
def userhome():

        cursor.execute("select * from post where postby !='"+session['username']+"' ")
        cdel=cursor.fetchall()
        return render_template('userHome.html',cdel=cdel)


@app.route('/myPost')
def myPost():

        cursor.execute("select * from post where postby ='"+session['username']+"' ")
        cdel=cursor.fetchall()
        return render_template('mypost.html',cdel=cdel)





if __name__ == '__main__':
    app.run(debug=True)