"""CRUD operations"""

from model import db, User, Appointment, connect_to_db
from datetime import datetime, timedelta

from sqlalchemy import extract


def create_user(email):
    """Create and return a new user."""

    user = User(email=email)

    return user

def get_num_halfhours(starttime, endtime):
    """gets the number of half hours in a time range"""
    int_start = int((starttime.timestamp()) / 60)
    int_end = int((endtime.timestamp()) / 60)
    minute_duration = int_end - int_start
    num_halfhours = minute_duration / 30
    return int(num_halfhours)

def liststarttimes(starttime, num_halfhours):
    """creates a list of potential start times based on range input"""
    l_starttimes = []

    for n in range(num_halfhours):
        print(starttime)
        l_starttimes.append(starttime)
        starttime += timedelta(minutes=30)
    return l_starttimes

def round_minutes(dt, direction, resolution):
    """Round minutes up or down"""
    new_minute = (dt.minute // resolution + (1 if direction == 'up' else 0)) * resolution
    return dt + timedelta(minutes=new_minute - dt.minute)

def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)

def get_users():
    """Return all users."""

    return User.query.all()

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def create_appointment(user_id, date, start_time, end_time, full_starttime):
    """Create and return a new appointment"""

    appointment = Appointment(user_id=user_id, date=date, start_time=start_time, end_time=end_time, full_starttime=full_starttime)

    return appointment

def get_appointments():
    """returns all appointments"""

    return Appointment.query.all()

def get_appointments_by_userid(user_id):
    """returns all appointments"""

    return Appointment.query.filter_by(user_id=user_id).all()

def check_no_appts_on_date (user_id, datetocheck):
    """return appointment by user_id and date to check"""
    return Appointment.query.filter_by(user_id=user_id, date=datetocheck).first()
    
def get_appointments_by_date(ndate):
    """return all appointments on a day"""
    apps_that_day = []
    dayapps = Appointment.query.filter_by(date=ndate).all()
    for n in dayapps:
        apps_that_day.append(n.full_starttime)
    return  apps_that_day



if __name__ == "__main__":
    from server import app

    connect_to_db(app)