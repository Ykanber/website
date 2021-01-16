from flask import Flask, render_template
from datetime import datetime
import view
from database import Database



app = Flask(__name__)
app.secret_key="1234"

app.add_url_rule("/", view_func=view.home_page) 
app.add_url_rule("/delete", view_func=view.deletepage) 
app.add_url_rule("/my_Teacher_profile", view_func=view.my_Teacher_profile)
app.add_url_rule("/my_Student_profile", view_func=view.my_Student_profile)
app.add_url_rule("/logoutforteacher", view_func=view.logoutforteacher)
app.add_url_rule("/logoutforstudent", view_func=view.logoutforstudent)
app.add_url_rule("/teacherstatspage", view_func=view.teacherstatspage)
app.add_url_rule("/teachersearch_page", view_func=view.teachersearch_page, methods=["GET","POST"])
app.add_url_rule("/teacher/<T_username>", view_func=view.teacherpage, methods=["GET","POST"])
app.add_url_rule("/student/<S_username>", view_func=view.studentpage)
app.add_url_rule("/teacheraddpage", view_func=view.teacheraddpage, methods=["GET","POST"])
app.add_url_rule("/commentaddpage", view_func=view.commentaddpage, methods=["GET","POST"])
app.add_url_rule("/likecommentpage", view_func=view.likecommentpage, methods=["GET","POST"])
app.add_url_rule("/dislikecommentpage", view_func=view.dislikecommentpage, methods=["GET","POST"])
app.add_url_rule("/commentremovepage", view_func=view.commentremovepage, methods=["GET","POST"])
app.add_url_rule("/teacherremovepage", view_func=view.teacherremovepage, methods=["GET","POST"])
app.add_url_rule("/login_page", view_func=view.login_page, methods=["GET", "POST"])
app.add_url_rule("/Teachersignup_page", view_func=view.Teachersignup_page, methods=["GET", "POST"])
app.add_url_rule("/Studentsignup_page", view_func=view.Studentsignup_page, methods=["GET", "POST"])

db = Database()
app.config["db"] = db

