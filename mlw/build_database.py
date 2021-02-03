import os
from config import db
from models import MarinaLitterWatch

# Data to initialize database with
MLW = [
    {
        "appid": "Application1",
        "hname": "Server3"
    },
    {
        "appid": "Application2",
        "hname": "Server2"
    },
    {
        "appid": "Application3",
        "hname": "Server1"
    },
]

# Delete database file if it exists currently
if os.path.exists("mlw.db"):
    os.remove("mlw.db")

# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for item in MLW:
    i = MarinaLitterWatch(appid=item.get("appid"), hname=item.get("hname"))
    db.session.add(i)

db.session.commit()
