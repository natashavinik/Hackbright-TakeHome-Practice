
"""Server for melon tasting schedule app."""

from flask import Flask, render_template, flash, request, session, redirect, jsonify
from model import connect_to_db, db
import crud
import os, json
import codecs
from datetime import datetime, timedelta

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("home.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")

    user = crud.get_user_by_email(email)
    if not user:
        user = crud.create_user(email)
        db.session.add(user)
        db.session.commit()

        flash("Welcome new user!")
        return redirect(f"/{user.user_id}")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")
        return redirect(f"/{user.user_id}")

@app.route("/seeavailable", methods=["POST"])
def check_avail():
    """See available appointments that day"""

    #retrived from the form
    # user_dates = request.form.get("alluserdates")
    user_id = request.form.get("userid")
    datetocheck = request.form.get("searchdate")
    starttime = request.form.get("starttime")
    endtime = request.form.get("endtime")

    user = crud.get_user_by_id(user_id)
    # print("CHOSENDATE", datetocheck)
    # print("USERS DATES", user_dates)
    # sch_appts = crud.get_appointments_by_userid(user_id)
    # list_s_dates = []
    # for n in sch_appts:
    #     list_s_dates.append(n.date)
    # print("BETTER USERS DATES", list_s_dates)
    #turned into datetime
    endtime = datetime.strptime(datetocheck +" "+ endtime, '%Y-%m-%d %H:%M')
    starttime = datetime.strptime(datetocheck +" "+ starttime, '%Y-%m-%d %H:%M')
    
    #range times rounded
    starttime = crud.round_minutes(starttime, 'up', 30)
    endtime = crud.round_minutes(endtime, "down", 30)

    #if datetocheck is the same as an attribute
    # of an appointment related to a user_id
    print("\n" * 4 )
    print("`SAME DATES AND TIMES TO CHECK")
    samedateappts = crud.check_no_appts_on_date(user_id, datetocheck)
    print('APPT SAME DAY?', samedateappts)
    if samedateappts is not None:
        flash("You already have an appt scheduled that day, please choose a different day.")
        return redirect(f"/{user.user_id}")

    #number of half hour increments

    num_halfhours = crud.get_num_halfhours(starttime, endtime)
    # testplus30 = starttime + timedelta(minutes=30)``
    start_time_list = crud.liststarttimes(starttime, num_halfhours)
    start_time_set = set(start_time_list)
    appts_that_day = set(crud.get_appointments_by_date(datetocheck))
    print("STARTTIME LIST", start_time_list)
    print("DAYS APPTS", appts_that_day)
    taken_appts = start_time_set.intersection(appts_that_day)
    for xtaken in taken_appts:
        start_time_list.remove(xtaken)
    print("OVERLAP", taken_appts)
 
    
    # for n in appts_set:
    #     print(n.start_time)
    #

    for n in start_time_list:
        print(n)
    print("STARTTIME TYPE TEST")
    print(num_halfhours)

    print("\n" * 4 )
    print("DATES AND TIMES TO CHECK")
    print(datetocheck)
    print(starttime)
    print(start_time_list)
    print("userid", user_id)
    print(endtime)
    print("\n" * 4 )
    #if the user already has appointment for that day, cant make one
    #figure out how to subtract endtime from start time
    #or make a list of times every 30 minutes from start to end
    #query that day if there is an appt at those times, delete from list
    #pass through the date, the times, the user ID
    return render_template("appointmentresults.html", start_time_list=start_time_list, user_id=user_id)




@app.route("/makeappt", methods=["GET","POST"])
def make_appt():
    """Make appt"""
    favobj = request.args.get('starttime')
    user_id = request.args.get('userid')
    print("STARTTIME", favobj)
    print(type(favobj))
    print("USERID", user_id)
    print(type(user_id))
    # datetomake = request.form.get("searchdate")
    # starttime = request.form.get("starttime")
    # endtime = request.form.get("endtime")
    print("\n" * 4 )
    print("DATES TIME CHOSEN")
    full_starttime = datetime.strptime(favobj, '%Y-%m-%d %H:%M:%S')
    print(full_starttime)
    print(type(full_starttime))
    endtime = full_starttime + timedelta(minutes=30)
    datetomake = full_starttime.strftime("%Y-%m-%d")
    starttime = full_starttime.strftime("%H:%M")
    endtime = endtime.strftime("%H:%M")
    # print(datetomake)
    # print(starttime)
    # print(endtime)
    print("\n" * 4 )
    appointment = crud.create_appointment(user_id, datetomake, starttime, endtime, full_starttime)
    db.session.add(appointment)
    db.session.commit()
    print(crud.get_appointments())
    return favobj
    # return redirect(f"/users/{user_id}")
    # return render_template("scheduledappointments.html")
    # return render_template("appointmentresults.html")

@app.route("/seescheduled/<user_id>", methods=["GET", "POST"])
def see_scheduled(user_id):
    """See users scheduled appts"""
    sch_appts = crud.get_appointments_by_userid(user_id)
    print("SCHEDULED APPTS", sch_appts)
    print(type(sch_appts))


    return render_template("scheduledappointments.html", user_id=user_id, apptlist = sch_appts)


@app.route("/<user_id>")
def show_user(user_id):
    """Show details on a user."""

    print(user_id)
    user = crud.get_user_by_id(user_id)
    print("wow")
    print(user)
    sch_appts = crud.get_appointments_by_userid(user_id)
    list_s_dates = []
    for n in sch_appts:
        list_s_dates.append(n.date)
    # print(user)
    
    # return render_template("user_details.html")
    return render_template("user_details.html", user_id=user_id, list_s_dates = list_s_dates)




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)