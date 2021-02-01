import os
from config import db
from models import Inventory

# Data to initialize database with
INVENTORY = [
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
if os.path.exists("inventory.db"):
    os.remove("inventory.db")

# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for item in INVENTORY:
    i = Inventory(appid=item.get("appid"), hname=item.get("hname"))
    db.session.add(i)

db.session.commit()
