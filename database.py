import mysql.connector as dpabi2
from flask import session, current_app
from Teacher import Teacher
from teaching import Teaching
from comment import Comment
from lstats import Lstats
from tstats import Tstats

connection = dpabi2.connect(
    host = 'localhost', 
    user='root',
    passwd='12345',
    database = "websitedb"
)

class Database:
    def __init__(self):
        mycursor = connection.cursor() 
        mycursor.execute("CREATE DATABASE IF NOT EXISTS websitedb")
        statement ="""CREATE TABLE IF NOT EXISTS Teacher (
            T_username VARCHAR(20) PRIMARY KEY,
            Name VARCHAR(20) NOT NULL,
            Surname VARCHAR(20) NOT NULL,
            age int NOT NULL,
            Lesson_type VARCHAR(30) NOT NULL,
            Teaching_rating float default 0.0,
            Votes_counter int default 0,
            Password VARCHAR(20) NOT NULL)
        """
        mycursor.execute(statement)
        mycursor.close()
        mycursor = connection.cursor()
        statement ="""CREATE TABLE IF NOT EXISTS Student (
            S_username VARCHAR(20) PRIMARY KEY,
            Name VARCHAR(20) NOT NULL,
            Surname VARCHAR(20) NOT NULL,
            age int NOT NULL,
            gender VARCHAR(8),
            Password VARCHAR(20) NOT NULL)
        """
        mycursor.execute(statement)
        mycursor.close()
        mycursor = connection.cursor()
        statement ="""CREATE TABLE IF NOT EXISTS Teaching_table (
            T_username VARCHAR(20) NOT NULL,
            S_username VARCHAR(20) NOT NULL, 
            PRIMARY KEY(T_username,S_username),
            FOREIGN KEY(T_username) References Teacher(T_username),
            FOREIGN KEY(S_username) References Student(S_username))
        """
        mycursor.execute(statement)
        mycursor.close()
        mycursor = connection.cursor()
        statement ="""CREATE TABLE IF NOT EXISTS Commentt(
            Comment_id int AUTO_INCREMENT PRIMARY KEY,
            T_username VARCHAR(20) NOT NULL,
            S_username VARCHAR(20) NOT NULL,
            rating int NOT NULL,
            Comment_text text NOT NULL,
            Date Date NOT NULL,
            Like_count int default 0,
            Dislike_count int default 0,
            UNIQUE(T_username,S_username),
            CHECK((rating>=0) AND (rating<=10)),
            FOREIGN KEY(T_username) References Teacher(T_username),
            FOREIGN KEY(S_username) References Student(S_username))
        """
        mycursor.execute(statement)
        mycursor.close()
        mycursor = connection.cursor()
        statement = """CREATE TABLE IF NOT EXISTS Commenting(
           Comment_id int NOT NULL,
           Voter_username  VARCHAR(20) NOT NULL,
           Like_type int NOT NULL,
           PRIMARY KEY(Comment_id,Voter_username),
           UNIQUE(Comment_id,Voter_username),
           FOREIGN KEY(Comment_id) References Commentt(Comment_id))
        """    
        mycursor.execute(statement)
        mycursor.close()
        connection.close()

    def teacher_sign(self,T_username,name,surname,age,lesson_type,password): #teacher sign operation
        connection = dpabi2.connect(
         host = 'localhost', 
         user='root',
         passwd='12345',
         database = "websitedb"
        )        
        mycursor = connection.cursor()
        statement ="INSERT INTO Teacher (T_username,Name,Surname,age,Lesson_type,Password) VALUES(%s,%s,%s,%s,%s,%s)"
        mycursor.execute(statement,(T_username,name,surname,age,lesson_type,password))
        connection.commit()
        mycursor.close() 
        connection.close()


    def issigned(self,username,type):
        connection = dpabi2.connect(
            host = 'localhost', 
            user='root',
            passwd='12345',
            database = "websitedb"
            )   
        if type == 1:
            mycursor = connection.cursor()
            statement ="SELECT * FROM Teacher WHERE T_username = %s"
            mycursor.execute(statement,(username,))
            a = mycursor.fetchone()
            print(a)
            mycursor.close() 
            connection.close()
            if a is None:
                return False
            else:
                return True

        elif type == 2:
            mycursor = connection.cursor()
            statement ="SELECT * FROM STUDENT WHERE S_username = %s"
            mycursor.execute(statement,(username,))
            a = mycursor.fetchone()
            mycursor.close() 
            connection.close()
            if a is None:
                return False
            else:
                return True


    def student_sign(self,S_username,name,surname,age,gender,password):   #student sign operation
        connection = dpabi2.connect(
         host = 'localhost', 
         user='root',
         passwd='12345',
         database = "websitedb"
        )
        mycursor = connection.cursor()
        statement ="INSERT INTO Student (S_username,Name,Surname,age,gender,Password) VALUES(%s,%s,%s,%s,%s,%s)"
        mycursor.execute(statement,(S_username,name,surname,age,gender,password,))
        connection.commit()
        mycursor.close() 
        connection.close()

    def teacher_login(self,T_username,Password):    #teacher login operation
        connection = dpabi2.connect(
         host = 'localhost', 
         user='root',
         passwd='12345',
         database = "websitedb"
        )
        mycursor = connection.cursor()
        mycursor.execute("Select * FROM Teacher WHERE ((T_username = %s) AND (Password = %s))",(T_username,Password))
        account = mycursor.fetchone()
        mycursor.close()
        connection.close()
        if account is None:
            return False
        else:
            session["username"] = account[0]
            session["Name"] = account[1]
            session["Surname"] = account[2]
            session["Age"] = account[3]             
            session["Lesson_type"] = account[4]
            session["Teaching_rating"] = account[5]
            session["Votes_counter"] = account[6]
            session["user"] = "teacher" 
            return True

    def student_login(self,S_username,Password):
        connection = dpabi2.connect(
         host = 'localhost', 
         user='root',
         passwd='12345',
         database = "websitedb"
        )
        mycursor = connection.cursor()
        mycursor.execute("Select * FROM Student WHERE ((S_username = %s) AND (Password = %s))",(S_username,Password))
        account = mycursor.fetchone()
        mycursor.close()
        connection.close()
        if account is None:
            return False
        else:
            session["username"] = account[0]
            session["Name"] = account[1]
            session["Surname"] = account[2]
            session["Age"] = account[3]
            session["Gender"] = account[4]
            session["user"] = "student"             
            return True
        
    def getteachers(self):
        connection = dpabi2.connect(
         host = 'localhost', 
         user='root',
         passwd='12345',
         database = "websitedb"
        )
        teachers = []
        mycursor = connection.cursor()
        mycursor.execute("Select * FROM Teacher")
        for T_username, Name, Surname, Age, Lesson_type, Teaching_rating, Votes_counter, Password in mycursor:
            Teacher_ = Teacher(T_username,Name,Surname,Age,Lesson_type,Teaching_rating,Votes_counter)
            teachers.append((T_username,Teacher_))  
        mycursor.close()
        connection.close()
        return teachers

    def getteacher(self,T_username):
        connection = dpabi2.connect(
         host = 'localhost', 
         user='root',
         passwd='12345',
         database = "websitedb"
        )
        mycursor = connection.cursor()
        sql = "Select * FROM Teacher WHERE (T_username = %s)"
        mycursor.execute(sql,(T_username,))
        teacher = mycursor.fetchone()
        mycursor.close()
        connection.close()
        return teacher 

    def getstudent(self,S_username):
        connection = dpabi2.connect(
         host = 'localhost', 
         user='root',
         passwd='12345',
         database = "websitedb"
        )
        mycursor = connection.cursor()
        sql = "Select * FROM Student WHERE (S_username = %s)"
        mycursor.execute(sql,(S_username,))
        student = mycursor.fetchone()
        mycursor.close()
        connection.close()
        return student 

    def teacheradd(self,T_username,S_username):
        connection = dpabi2.connect(
         host = 'localhost', 
         user='root',
         passwd='12345',
         database = "websitedb"
        )
        mycursor = connection.cursor()
        mycursor.execute("INSERT INTO Teaching_table (T_username,S_username) VALUES(%s,%s)", (T_username,S_username))
        connection.commit()   
        mycursor.close()
        connection.close()

    def commentadd(self,T_username,S_username,rating,comment,date):
        connection = dpabi2.connect(
         host = 'localhost', 
         user='root',
         passwd='12345',
         database = "websitedb"
        )
        mycursor = connection.cursor()
        mycursor.execute("INSERT INTO Commentt (T_username,S_username,rating,Comment_text,Date) VALUES(%s,%s,%s,%s,%s)", (T_username,S_username,rating,comment,date))
        connection.commit()   
        mycursor.close()
        mycursor = connection.cursor()
        sql = "UPDATE Teacher SET Teaching_rating = (((Votes_counter * Teaching_rating) + %s) / (Votes_counter + 1)) WHERE T_username = %s"
        mycursor.execute(sql,(rating,T_username,))
        connection.commit()
        mycursor.close()
        mycursor = connection.cursor()
        sql = "UPDATE Teacher SET Votes_counter = (Votes_counter + 1) WHERE T_username = %s"
        mycursor.execute(sql,(T_username,))
        connection.commit()
        mycursor.close()
        connection.close()

    def teacherremove(self,T_username,S_username):
        connection = dpabi2.connect(
         host = 'localhost', 
         user='root',
         passwd='12345',
         database = "websitedb"
        )
        mycursor = connection.cursor()
        mycursor.execute("DELETE FROM Teaching_table WHERE (T_username = %s AND S_username = %s)", (T_username,S_username))
        connection.commit() 
        mycursor.close()
        connection.close()

    def commentremove(self,T_username,S_username):
        connection = dpabi2.connect(
         host = 'localhost', 
         user='root',
         passwd='12345',
         database = "websitedb"
        )
        mycursor = connection.cursor()
        mycursor.execute("SELECT Comment_id FROM Commentt WHERE (T_username = %s AND S_username = %s)", (T_username,S_username))
        comment_id = mycursor.fetchone()
        mycursor.close()
        mycursor = connection.cursor()
        mycursor.execute("SELECT Votes_counter FROM Teacher WHERE T_username = %s", (T_username,))
        Votes_counter_ = mycursor.fetchone()
        mycursor.close()
        mycursor = connection.cursor()
        mycursor.execute("SELECT rating FROM Commentt WHERE (T_username = %s AND S_username = %s)", (T_username,S_username))
        for rating in mycursor:
            rating_ = rating
        mycursor.close()
        mycursor = connection.cursor()
        mycursor.execute("DELETE FROM Commenting WHERE Comment_id = %s", (comment_id))
        connection.commit() 
        mycursor.close()
        mycursor = connection.cursor()
        mycursor.execute("DELETE FROM Commentt WHERE (T_username = %s AND S_username = %s)", (T_username,S_username))
        connection.commit() 
        mycursor.close()
        if Votes_counter_[0] > 1: #i used if to avoid division with 0
            mycursor = connection.cursor()
            sql = "UPDATE Teacher SET Teaching_rating = (((Votes_counter * Teaching_rating) - %s) / (Votes_counter - 1)) WHERE T_username = %s"
            mycursor.execute(sql,(rating_[0],T_username,))
            connection.commit()
            mycursor.close()
        else:
            mycursor = connection.cursor()
            sql = "UPDATE Teacher SET Teaching_rating =  0 WHERE T_username = %s"
            mycursor.execute(sql,(T_username,))
            connection.commit()
            mycursor.close()
        mycursor = connection.cursor()
        sql = "UPDATE Teacher SET Votes_counter = (Votes_counter - 1) WHERE T_username = %s"
        mycursor.execute(sql,(T_username,))
        connection.commit()
        mycursor.close()
        connection.close()

    def checkenrollment(self,T_username,S_username):
        connection = dpabi2.connect(
         host = 'localhost', 
         user='root',
         passwd='12345',
         database = "websitedb"
        )
        mycursor = connection.cursor()
        mycursor.execute( "Select * FROM Teaching_table WHERE (T_username = %s) AND (S_username = %s)", (T_username,S_username))
        a = mycursor.fetchone()
        if a is None:
            return False
        else:
            return True

    def checkcommented(self,T_username,S_username):
        connection = dpabi2.connect(
         host = 'localhost', 
         user='root',
         passwd='12345',
         database = "websitedb"
        )
        mycursor = connection.cursor()
        mycursor.execute( "Select * FROM Commentt WHERE (T_username = %s) AND (S_username = %s)", (T_username,S_username))
        a = mycursor.fetchone()
        if a is None:
            return False
        else:
            return True
    
    def getstudentteachers(self,S_username):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )
        teaching = []
        mycursor = connection.cursor()  
        sql ="""SELECT Teacher.T_username,Teacher.NAME,Teacher.Surname 
        FROM Teaching_table JOIN Teacher 
        ON(Teacher.T_username = Teaching_table.T_username) WHERE (S_username = %s) 
        """
        mycursor.execute(sql,(S_username,))
        for T_username, Name, Surname in mycursor:
           teaching_ = Teaching(T_username,Name,Surname,S_username,0,0)
           teaching.append(teaching_)  
        mycursor.close()
        connection.close()
        return teaching

    def getteachersstudents(self,T_username):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )
        teaching = []
        mycursor = connection.cursor()  
        sql ="""SELECT Student.S_username,Student.NAME,Student.Surname 
        FROM Teaching_table JOIN Student 
        ON(Student.S_username = Teaching_table.S_username) WHERE (T_username = %s) 
        """
        mycursor.execute(sql,(T_username,))
        for S_username, Name, Surname in mycursor:
           teaching_ = Teaching(T_username,0,0,S_username,Name,Surname)
           teaching.append(teaching_)  
        mycursor.close()
        connection.close()
        return teaching
    
    def checkvoted(self,comment_id,s_username):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )
        mycursor = connection.cursor()
        mycursor.execute( "Select Commenting.Like_type FROM Commenting WHERE Comment_id = %s AND Voter_username=%s ", (comment_id,s_username,))
        a = mycursor.fetchone()
        if a is None:
            return 1
        elif a[0] == 1:
            return 2
        elif a[0] == 2:
            return 3
    
    def addlikevote(self,comment_id,s_username):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )
        mycursor = connection.cursor()
        sql ="""
            UPDATE Commentt SET Like_count = (Like_count + 1) WHERE Comment_id = %s
        """
        mycursor.execute(sql,(comment_id,))
        mycursor.close()
        mycursor = connection.cursor()
        c = 1
        sql ="""
            INSERT INTO Commenting(Comment_id,Voter_username,Like_type) VALUES(%s,%s,%s)
        """
        mycursor.execute(sql,(comment_id,s_username,c))
        connection.commit()
        mycursor.close()
        mycursor = connection.cursor()
        mycursor.execute("Select T_username FROM Commentt WHERE (Comment_id = %s)",(comment_id,))
        teacher = mycursor.fetchone()
        return teacher[0]


    def adddislikevote(self,comment_id,s_username):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )
        mycursor = connection.cursor()
        sql ="""
            UPDATE Commentt SET Dislike_count = (Dislike_count + 1) WHERE Comment_id = %s
        """
        mycursor.execute(sql,(comment_id,))
        mycursor.close()
        mycursor = connection.cursor()
        c = 2
        sql ="""
            INSERT INTO Commenting(Comment_id,Voter_username,Like_type) VALUES(%s,%s,%s)
        """
        mycursor.execute(sql,(comment_id,s_username,c))
        connection.commit()
        mycursor.close()
        mycursor = connection.cursor()
        mycursor.execute("Select T_username FROM Commentt WHERE (Comment_id = %s)",(comment_id,))
        teacher_username = mycursor.fetchone()
        mycursor.close()
        return teacher_username[0]


    def removelikevote(self,comment_id,s_username):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )
        mycursor = connection.cursor()
        sql ="""
            UPDATE Commentt SET Like_count = (Like_count - 1) WHERE Comment_id = %s
        """
        mycursor.execute(sql,(comment_id,))
        mycursor.close()
        mycursor = connection.cursor()
        mycursor.execute("Select T_username FROM Commentt WHERE (Comment_id = %s)",(comment_id,))
        teacher_username = mycursor.fetchone()
        mycursor.close()
        mycursor = connection.cursor()
        sql ="""
            DELETE FROM Commenting WHERE Comment_id = %s
        """
        mycursor.execute(sql,(comment_id,))
        connection.commit() 
        mycursor.close()
        return teacher_username[0]


    def removedislikevote(self,comment_id,s_username):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )
        mycursor = connection.cursor()
        sql ="""
            UPDATE Commentt SET Dislike_count = (Dislike_count - 1) WHERE Comment_id = %s
        """
        mycursor.execute(sql,(comment_id,))
        mycursor.close()
        mycursor = connection.cursor()
        mycursor.execute("Select T_username FROM Commentt WHERE (Comment_id = %s)",(comment_id,))
        teacher_username = mycursor.fetchone()
        mycursor.close()
        mycursor = connection.cursor()
        sql ="""
            DELETE FROM Commenting WHERE Comment_id = %s
        """
        mycursor.execute(sql,(comment_id,))
        connection.commit() 
        mycursor.close()
        return teacher_username[0]


    def getcomments(self,T_username):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )
        teaching = []
        mycursor = connection.cursor()  
        sql ="""SELECT Commentt.Comment_id,Commentt.S_username,Commentt.rating,Commentt.Comment_text,Commentt.Date,Commentt.Like_count,Commentt.Dislike_count FROM Commentt
        WHERE (T_username = %s) 
        """
        mycursor.execute(sql,(T_username,))
        for comment_id,s_username,rating, Comment_text,date,like_count,dislike_count in mycursor:
           teaching_ = Comment(comment_id,s_username,rating,Comment_text,date,like_count,dislike_count,0)
           teaching.append(teaching_)  
        mycursor.close()
        connection.close()
        return teaching

    def getjustcomments(self,S_username,T_username,commented):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )
        db = current_app.config["db"]
        allcomments = []
        comparedcomments = []
        allcomments = db.getcomments(T_username)

        mycursor = connection.cursor()  
        sql ="""SELECT Commentt.Comment_id,Commentt.S_username,Commentt.rating,
        Commentt.Comment_text,Commentt.Date,Commentt.Like_count,Commentt.Dislike_count
        FROM Commentt
        WHERE (T_username = %s AND S_username = %s) 
        """
        mycursor.execute(sql,(T_username,S_username,))
        for comment_id,s_username,rating, Comment_text,date,like_count,dislike_count in mycursor:
           teaching_ = Comment(comment_id,s_username,rating,Comment_text,date,like_count,dislike_count,3)
           comparedcomments.append(teaching_)  
        mycursor.close()

        mycursor = connection.cursor()  
        sql ="""SELECT Commentt.Comment_id,Commentt.S_username,Commentt.rating,Commentt.Comment_text,
        Commentt.Date,Commentt.Like_count,Commentt.Dislike_count 
        FROM Commenting JOIN Commentt 
        ON(Commenting.Comment_id = Commentt.Comment_id) WHERE (Voter_username = %s AND Like_type = %s AND Commentt.T_username = %s) 
        """
        mycursor.execute(sql,(S_username,1,T_username,))
        for comment_id,s_username,rating, Comment_text,date,like_count,dislike_count in mycursor:
           teaching_ = Comment(comment_id,s_username,rating,Comment_text,date,like_count,dislike_count,1)
           comparedcomments.append(teaching_)  
        mycursor.close()
        mycursor = connection.cursor()
        sql ="""SELECT Commentt.Comment_id,Commentt.S_username,Commentt.rating,Commentt.Comment_text,
        Commentt.Date,Commentt.Like_count,Commentt.Dislike_count 
        FROM Commenting JOIN Commentt 
        ON(Commenting.Comment_id = Commentt.Comment_id) WHERE (Voter_username = %s AND Like_type = %s AND Commentt.T_username = %s) 
        """
        mycursor.execute(sql,(S_username,2,T_username,))
        for comment_id,s_username,rating, Comment_text,date,like_count,dislike_count in mycursor:
           teaching_ = Comment(comment_id,s_username,rating,Comment_text,date,like_count,dislike_count,2)
           comparedcomments.append(teaching_)  
        mycursor.close()
        connection.close()

        for x in range(0,len(allcomments)):
            for a in range(0,len(comparedcomments)):
                if allcomments[x].comment_id == comparedcomments[a].comment_id:
                    if comparedcomments[a].liked == 1:
                        allcomments[x].liked = 1 

                    elif comparedcomments[a].liked == 2:
                        allcomments[x].liked = 2 
                
        if commented == 1:
            for x in range(0,len(allcomments)):
                if allcomments[x].comment_id == comparedcomments[0].comment_id:
                    if allcomments[x].liked == 1:
                        allcomments[x].liked = 4
                    elif allcomments[x].liked == 2:
                        allcomments[x].liked = 5
                    elif allcomments[x].liked == 0:
                        allcomments[x].liked = 3
          
        return allcomments


    def filterteachers(self,lesson,minage,maxage,rating,votecounter,order):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )       
        teachers = []
        mycursor = connection.cursor()
        sql ="""SELECT * FROM TEACHER   
            WHERE ((age <= %s AND age >= %s) AND Lesson_type = %s AND Teaching_rating >= %s AND Votes_counter >= %s)
            ORDER BY Name ASC 
            """
        if order == 1:
            sql ="""SELECT * FROM TEACHER   
            WHERE ((age <= %s AND age >= %s) AND Lesson_type = %s AND Teaching_rating >= %s AND Votes_counter >= %s) 
            ORDER BY Rating DESC 
            """
        elif order == 2:
            sql ="""SELECT * FROM TEACHER   
            WHERE ((age <= %s AND age >= %s) AND Lesson_type = %s AND Teaching_rating >= %s AND Votes_counter >= %s) 
            ORDER BY Votes_counter DESC 
            """
        mycursor.execute(sql,(maxage,minage,lesson,rating,votecounter,))
        for T_username, Name, Surname, Age, Lesson_type, Teaching_rating, Votes_counter, Password in mycursor:
            Teacher_ = Teacher(T_username,Name,Surname,Age,Lesson_type,Teaching_rating,Votes_counter)
            teachers.append((T_username,Teacher_))  
        mycursor.close()
        connection.close()
        return teachers

    def getlessonstats(self):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )       
        mycursor = connection.cursor()
        stats = []
        sql ="""SELECT COUNT(m.T_username), AVG(m.Teaching_rating) , m.Lesson_type    
        FROM Teacher AS m INNER JOIN Teaching_table AS g
        ON m.T_username = g.T_username
        GROUP BY m.Lesson_type 
        ORDER BY m.Teaching_rating DESC
        """
        mycursor.execute(sql,)
        for count, average, lesson_type in mycursor:
            stat = Lstats(count,average,lesson_type)
            stats.append(stat)
        mycursor.close()
        connection.close()
        return stats

    def getteacherstats(self):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )       
        mycursor = connection.cursor()
        stats = []
        sql ="""SELECT COUNT(g.S_username) AS total, AVG(m.Teaching_rating) ,m.Name, m.Surname    
        FROM Teacher AS m INNER JOIN Teaching_table AS g
        ON m.T_username = g.T_username
        GROUP BY m.T_username
        ORDER BY total DESC 
        """
        mycursor.execute(sql,)
        for count, average, name, surname in mycursor:
            stat = Tstats(count,average,name,surname)
            stats.append(stat)
        mycursor.close()
        connection.close()
        return stats

    def deleteteacher(self,username):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )       
        mycursor = connection.cursor()
        sql = """
            DELETE FROM Teaching_table WHERE T_username = %s  
        """
        mycursor.execute(sql,(username,))
        connection.commit()
        mycursor.close()
        mycursor = connection.cursor()
        sql = """
            Select Comment_id FROM Commentt 
            WHERE T_username = %s  
        """
        mycursor.execute(sql,(username,))
        c = mycursor.fetchall()
        mycursor.close()
        for comment_id in c:
            mycursor = connection.cursor()
            sql ="""
                DELETE FROM Commenting 
                WHERE Comment_id = %s  
            """
            mycursor.execute(sql,(comment_id[0],))
            connection.commit()
            mycursor.close()
        mycursor = connection.cursor()
        sql = """
            DELETE FROM Commentt WHERE T_username = %s  
        """
        mycursor.execute(sql,(username,))
        connection.commit()
        mycursor.close()
        mycursor = connection.cursor()
        sql = """
            DELETE FROM Teacher WHERE T_username = %s  
        """
        mycursor.execute(sql,(username,))
        connection.commit()
        mycursor.close()

    def deletestudent(self,username):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )       
        db = current_app.config["db"]
        mycursor = connection.cursor()
        sql = """
            SELECT T_username FROM Teaching_table WHERE S_username = %s  
        """
        mycursor.execute(sql,(username,))
        x = mycursor.fetchall()
        mycursor.close()
        for T_username in x:
            db.teacherremove(T_username[0],username)
        mycursor = connection.cursor()
        sql = """
            Select Comment_id FROM Commenting WHERE Voter_username = %s AND Like_type= %s  
        """
        mycursor.execute(sql,(username,1,))
        x = mycursor.fetchall()
        mycursor.close()
        for comment_id in x:
            db.removelikevote(comment_id[0],username)
        mycursor = connection.cursor()
        sql = """
            Select Comment_id FROM Commenting WHERE Voter_username = %s AND Like_type= %s  
        """
        mycursor.execute(sql,(username,2,))
        x = mycursor.fetchall()
        mycursor.close()
        for comment_id in x:
            db.removedislikevote(comment_id[0],username)
        mycursor = connection.cursor()
        sql = """
            SELECT T_username FROM Commentt WHERE S_username = %s  
        """
        mycursor.execute(sql,(username,))
        x = mycursor.fetchall()
        mycursor.close()
        for T_username in x:
            db.commentremove(T_username[0],username)
        mycursor = connection.cursor()
        sql = """
            DELETE FROM STUDENT WHERE S_username = %s  
        """
        mycursor.execute(sql,(username,))
        connection.commit()
        mycursor.close()
        connection.close()

    def changestudentinfo(self,name,surname,age,gender,password):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )    
        oldusername = session["username"]
        mycursor = connection.cursor()
        sql = """
        UPDATE Student SET Name = %s
        WHERE S_username = %s
        """
        mycursor.execute(sql,(name,oldusername,))
        connection.commit()
        mycursor.close()
        session["Name"] = name
        mycursor = connection.cursor()
        sql = """
        UPDATE Student SET Surname = %s
        WHERE S_username = %s
        """
        mycursor.execute(sql,(surname,oldusername,))
        connection.commit()
        mycursor.close()
        session["Surname"] = surname
        mycursor = connection.cursor()
        sql = """
        UPDATE Student SET age = %s
        WHERE S_username = %s
        """
        mycursor.execute(sql,(age,oldusername,))
        connection.commit()
        mycursor.close()
        session["Age"] = age
        mycursor = connection.cursor()
        sql = """
        UPDATE Student SET gender = %s
        WHERE S_username = %s
        """
        mycursor.execute(sql,(gender,oldusername,))
        connection.commit()
        mycursor.close()
        session["Gender"] = gender
        mycursor = connection.cursor()
        sql = """
        UPDATE Student SET Password = %s
        WHERE S_username = %s
        """
        mycursor.execute(sql,(password,oldusername,))
        connection.commit()
        mycursor.close()
        connection.close()


    def changeteacherinfo(self,name,surname,age,lesson_type,password):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )    
        oldusername = session["username"]
        mycursor = connection.cursor()
        sql = """
        UPDATE Teacher SET Name = %s
        WHERE T_username = %s
        """
        mycursor.execute(sql,(name,oldusername,))
        connection.commit()
        mycursor.close()
        session["Name"] = name
        mycursor = connection.cursor()
        sql = """
        UPDATE Teacher SET Surname = %s
        WHERE T_username = %s
        """
        mycursor.execute(sql,(surname,oldusername,))
        connection.commit()
        mycursor.close()
        session["Surname"] = surname
        mycursor = connection.cursor()
        sql = """
        UPDATE Teacher SET age = %s
        WHERE T_username = %s
        """
        mycursor.execute(sql,(age,oldusername,))
        connection.commit()
        mycursor.close()
        session["Age"] = age
        mycursor = connection.cursor()
        sql = """
        UPDATE Teacher SET Lesson_type = %s
        WHERE T_username = %s
        """
        mycursor.execute(sql,(lesson_type,oldusername,))
        connection.commit()
        mycursor.close()
        session["Lesson_type"] = lesson_type
        mycursor = connection.cursor()
        sql = """
        UPDATE Teacher SET Password = %s
        WHERE T_username = %s
        """
        mycursor.execute(sql,(password,oldusername,))
        connection.commit()
        mycursor.close()
        connection.close()

    def changecomment(self,S_username,text,rating,T_username):
        connection = dpabi2.connect(
        host = 'localhost', 
        user='root',
        passwd='12345',
        database = "websitedb"
        )   
        mycursor = connection.cursor()
        sql = """
        UPDATE Commentt SET Comment_text = %s
        WHERE (T_username = %s AND S_username = %s)
        """
        mycursor.execute(sql,(text,T_username,S_username,))
        connection.commit()
        mycursor.close()
        mycursor = connection.cursor()
        sql = """
        UPDATE Commentt SET rating = %s
        WHERE (T_username = %s AND S_username = %s)
        """
        mycursor.execute(sql,(rating,T_username,S_username,))
        connection.commit()
        mycursor.close()


