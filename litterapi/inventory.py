"""
This is the inventory module and supports all the REST actions for the
inventory data
"""

from flask import make_response, abort
from config import db
from models import Inventory, InventorySchema


def read_all():
    """
    This function responds to a request for /inventory
    with the complete lists of items

    :return:        json string of list of items
    """
    # Create the list of servers from our data
    inventory = Inventory.query.order_by(Inventory.hname).all()

    # Serialize the data for the response
    inventory_schema = InventorySchema(many=True)
    data = inventory_schema.dump(inventory)
    return data


def read_one(inventory_id):
    """
    This function responds to a request for /inventory/{inventory_id}
    with one matching item from inventory

    :param inventory_id:   Id of inventory to find
    :return:               Inventory matching id
    """
    # Get the item requested
    inventory = Inventory.query.filter(
        Inventory.inventory_id == inventory_id).one_or_none()

    # Did we find a inventory?
    if inventory is not None:

        # Serialize the data for the response
        inventory_schema = InventorySchema()
        data = inventory_schema.dump(inventory)
        return data

    # Otherwise, nope, didn't find that item
    else:
        abort(
            404,
            "Inventory not found for Id: {inventory_id}".format(
                inventory_id=inventory_id),
        )


def create(inventory):
    """
    This function creates a new item in the inventory structure
    based on the passed in inventory data

    :param inventory:  item to create in inventory structure
    :return:           201 on success, 406 on inventory exists
    """
    appid = inventory.get("appid")
    hname = inventory.get("hname")

    existing_inventory = (Inventory.query.filter(
        Inventory.appid == appid).filter(
            Inventory.hname == hname).one_or_none())

    # Can we insert this item?
    if existing_inventory is None:

        # Create a inventory instance using the schema and the passed in item
        schema = InventorySchema()
        new_inventory = schema.load(inventory, session=db.session)

        # Add the inventory to the database
        db.session.add(new_inventory)
        db.session.commit()

        # Serialize and return the newly created inventory in the response
        data = schema.dump(new_inventory)

        return data, 201

    # Otherwise, nope, inventory exists already
    else:
        abort(
            409,
            "Inventory {appid} {hname} exists already".format(
                appid=appid, hname=hname),
        )


def update(inventory_id, inventory):
    """
    This function updates an existing item in the inventory structure

    :param inventory_id:   Id of the inventory to update
    :param inventory:      inventory to update
    :return:               updated inventory structure
    """
    # Get the item requested from the db into session
    update_inventory = Inventory.query.filter(
        Inventory.inventory_id == inventory_id).one_or_none()

    # Did we find a item?
    if update_inventory is not None:

        # turn the passed in inventory into a db object
        schema = InventorySchema()
        update = schema.load(inventory, session=db.session)

        # Set the id to the inventory we want to update
        update.inventory_id = update_inventory.inventory_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated inventory in the response
        data = schema.dump(update_inventory)

        return data, 200

    # Otherwise, nope, didn't find that item
    else:
        abort(
            404,
            "Inventory not found for Id: {inventory_id}".format(
                inventory_id=inventory_id),
        )


def delete(inventory_id):
    """
    This function deletes an item from the inventory structure

    :param inventory_id:   Id of the inventory to delete
    :return:               200 on successful delete, 404 if not found
    """
    # Get the item requested
    inventory = Inventory.query.filter(
        Inventory.inventory_id == inventory_id).one_or_none()

    # Did we find a Inventory?
    if inventory is not None:
        db.session.delete(inventory)
        db.session.commit()
        return make_response(
            "Inventory {inventory_id} deleted".format(
                inventory_id=inventory_id), 200)

    # Otherwise, nope, didn't find that inventory
    else:
        abort(
            404,
            "Inventory not found for Id: {inventory_id}".format(
                inventory_id=inventory_id),
        )
