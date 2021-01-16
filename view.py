from flask import abort, Flask, render_template, current_app, request, url_for, redirect, session
from datetime import date
from teaching import Teaching

def home_page():
    return render_template("home.html")

def Studentsignup_page():
    db = current_app.config["db"]
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        surname = request.form['surname']
        age = request.form['age']
        gender = request.form['gender']
        password = request.form['password']
        db.student_sign(username,name,surname,age,gender,password)
        return render_template("home.html")
    else:
        return render_template("Studentsignup.html")

def Teachersignup_page():
    db = current_app.config["db"]
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        surname = request.form['surname']
        age = request.form['age']
        lesson_type = request.form['lesson_type']
        password = request.form['password']
        db.teacher_sign(username,name,surname,age,lesson_type,password)
        return render_template("home.html")
    else:
        return render_template("Teachersignup.html")

def deletepage():
    db = current_app.config["db"]
    user = session['user']
    if user == "teacher":
        username = session['username']
        db.deleteteacher(username)
        return redirect(url_for("logoutforteacher"))
    else:
        username = session['username']
        db.deletestudent(username)
        return redirect(url_for("logoutforstudent"))

def login_page():
    db = current_app.config["db"]
    if request.method == 'POST':
        username = request.form['username']
        Password = request.form['Password']
        user = request.form['user']
        if user == "teacher":
            abc = db.teacher_login(username,Password)
            if abc == True:
                return redirect(url_for("my_Teacher_profile"))
            else:
                return render_template("login.html")
        
        else:
            abc = db.student_login(username,Password)
            if abc == True:
                return redirect(url_for("my_Student_profile"))
            else:
                return render_template("login.html")
    else:
        return render_template("login.html") 


def teacherpage(T_username):
    db = current_app.config["db"]
    teacher = db.getteacher(T_username)
    students = db.getteachersstudents(T_username)
    comments = db.getcomments(T_username)
    if session["user"] == "teacher":
        return render_template("Teacherprofile.html", arr=teacher,students= students,comments=comments)
    else:
        S_username = session["username"]
        isenrolled = db.checkenrollment(T_username,S_username)
        iscommented = db.checkcommented(T_username,S_username)
        if isenrolled == True:
            if iscommented == True:
                justcomments = db.getjustcomments(S_username,T_username,1)
                return render_template("teacherprofileforstudentcommented.html", arr=teacher, students=students,comments=justcomments)
            justcomments = db.getjustcomments(S_username,T_username,2)
            return render_template("teacherprofileforstudentsenrolled.html", arr=teacher, students=students,comments=justcomments)
        elif isenrolled == False:
            return render_template("teacherprofileforstudents.html", arr=teacher, students=students,comments=comments) 

def studentpage(S_username):
    db = current_app.config["db"]
    student = db.getstudent(S_username)
    teachers = db.getstudentteachers(S_username)
    if session["user"] == "student":
        return render_template("studentprofile.html", arr=student, teachers=teachers)
    else:
        return render_template("studentprofileforteachers.html", arr=student, teachers=teachers)

def my_Teacher_profile():
    arr=[session["username"],session["Name"],session["Surname"],session["Age"],session["Lesson_type"],session["Teaching_rating"],session["Votes_counter"],session["username"],session["username"]]
    db = current_app.config["db"]
    students = db.getteachersstudents(session["username"])
    comments = db.getcomments(session["username"])
    return render_template("Teacherprofile.html", arr=arr, students=students, comments = comments)

def my_Student_profile():
    arr=[session["username"],session["Name"],session["Surname"],session["Age"],session["Gender"],session["username"],session["username"]]
    db = current_app.config["db"]
    teachers = db.getstudentteachers(session["username"])
    return render_template("Studentprofile.html", arr=arr, teachers=teachers)

    
def teachersearch_page():
    db = current_app.config["db"]
    teachers = db.getteachers()
    if request.method == 'POST':
        lesson = request.form['lesson']
        minage = request.form['minage']
        maxage = request.form['maxage']
        rating = request.form['rating']

        filteredteachers = db.filterteachers(lesson,minage,maxage,rating)
        if session["user"] == "student":
            return render_template("teachersearch.html", teachers=filteredteachers)
        else:
            return render_template("teachersearchforteachers.html", teachers=filteredteachers)

    else:
        if session["user"] == "student":
            return render_template("teachersearch.html", teachers=teachers)
        else:
            return render_template("teachersearchforteachers.html", teachers=teachers)
    
def teacheraddpage():
    if request.method == 'POST':
        db = current_app.config["db"]
        T_username = request.form['T_username']
        S_username = session["username"]
        isduplicate = db.checkenrollment(T_username,S_username)
        if isduplicate == False:
            db.teacheradd(T_username,S_username)
            return redirect(url_for("teacherpage", T_username = T_username))   # dikkat
        else:
            return redirect(url_for("my_Student_profile"))
    else:
        return redirect(url_for("teacherpage"), T_username = T_username)

def commentaddpage():
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    S_username = session["username"]
    T_username = request.form["T_username"]
    rating = request.form["rating"]
    comment = request.form["comment_text"]
    db = current_app.config["db"]
    if request.method == 'POST':
        isduplicate = db.checkcommented(T_username,S_username)
        if isduplicate == False:
            db.commentadd(T_username,S_username,rating,comment,d1)
            return redirect(url_for("teacherpage", T_username = T_username))
        else:
            return redirect(url_for("my_Student_profile"))
    else:
        return render_template("commentpage.html")

def commentremovepage():
    S_username = session["username"]
    T_username = request.form["T_username"]
    db = current_app.config["db"]
    if request.method == 'POST':
        db.commentremove(T_username,S_username)
        return redirect(url_for("teacherpage", T_username = T_username))
    else:
        return render_template("commentpage.html")

def teacherremovepage():
    if request.method == 'POST':
        db = current_app.config["db"]
        T_username = request.form['T_username']
        S_username = session["username"]
        isenrolled = db.checkenrollment(T_username,S_username)
        if isenrolled == True:
            db.teacherremove(T_username,S_username)
            return redirect(url_for("teacherpage", T_username = T_username))
        else:
            return redirect(url_for("my_Student_profile"))
    else:
        return redirect(url_for("teacherpage"), T_username = T_username)

def logoutforteacher():
    session.pop("username",None)
    session.pop("Name",None)
    session.pop("Surname",None)
    session.pop("Age",None)
    session.pop("Lesson_type",None)
    session.pop("Teaching_rating",None)
    session.pop("Student_counter",None)
    session.pop("Votes_counter",None)
    session.pop("user",None)
    return redirect(url_for('home_page'))

def logoutforstudent():
    session.pop("username",None)
    session.pop("Name",None)
    session.pop("Surname",None)
    session.pop("Age",None)
    session.pop("user",None)
    return redirect(url_for('home_page'))

def likecommentpage():
    S_username = session["username"]
    comment_id = request.form["comment_id"]
    db = current_app.config["db"]
    if request.method == 'POST':
        isduplicate = db.checkvoted(comment_id,S_username)
        if isduplicate == 1:    #no vote 
            T_username = db.addlikevote(comment_id,S_username)
            return redirect(url_for("teacherpage", T_username = T_username)) 
        elif isduplicate == 2: #liked before
            T_username = db.removelikevote(comment_id,S_username)    #like kaldiran func
            return redirect(url_for("teacherpage", T_username = T_username)) 
        elif isduplicate == 3:   #disliked before
            T_username = db.removedislikevote(comment_id,S_username)
            T_username = db.addlikevote(comment_id,S_username)
            return redirect(url_for("teacherpage", T_username = T_username))
        else:
            return redirect(url_for("my_Student_profile"))
    else:
        return render_template("my_Student_profile.html")

def dislikecommentpage():
    S_username = session["username"]
    comment_id = request.form["comment_id"]
    db = current_app.config["db"]
    if request.method == 'POST':
        isduplicate = db.checkvoted(comment_id,S_username)
        if isduplicate == 1:
            T_username = db.adddislikevote(comment_id,S_username)
            return redirect(url_for("teacherpage", T_username = T_username)) 
        elif isduplicate == 2: #liked before
            T_username = db.removelikevote(comment_id,S_username)    #like kaldiran func
            T_username = db.adddislikevote(comment_id,S_username)   
            return redirect(url_for("teacherpage", T_username = T_username)) 

        elif isduplicate == 3:   #disliked before
            T_username = db.removedislikevote(comment_id,S_username)
            return redirect(url_for("teacherpage", T_username = T_username))
        else:
            return redirect(url_for("my_Student_profile"))
    else:
        return render_template("my_Student_profile.html")


def teacherstatspage():
    db = current_app.config["db"]
    lesson_stats = db.getlessonstats()
    teacher_stats = db.getteacherstats()
    return render_template("teacherstatspage.html", lesson_stats = lesson_stats, teacher_stats = teacher_stats)

