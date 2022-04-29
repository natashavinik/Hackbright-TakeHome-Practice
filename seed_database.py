"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb melonappointments")
os.system("createdb melonappointments")

model.connect_to_db(server.app)
model.db.create_all()


for n in range(10):
    email = f"user{n}@test.com"  # Voila! A unique email!

    user = crud.create_user(email)
    model.db.session.add(user)




model.db.session.commit()
