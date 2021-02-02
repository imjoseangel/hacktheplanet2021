"""
This is the mlw module and supports all the REST actions for the
mlw data
"""

from flask import make_response, abort
from config import db
from models import MarinaLitterWatch, MarinaLitterWatchSchema


def read_all():
    """
    This function responds to a request for /mlw
    with the complete lists of items

    :return:        json string of list of items
    """
    # Create the list of servers from our data
    mlw = MarinaLitterWatch.query.order_by(MarinaLitterWatch.hname).all()

    # Serialize the data for the response
    mlw_schema = MarinaLitterWatchSchema(many=True)
    data = mlw_schema.dump(mlw)
    return data


def read_one(mlw_id):
    """
    This function responds to a request for /mlw/{mlw_id}
    with one matching item from mlw

    :param mlw_id:   Id of mlw to find
    :return:               Mlw matching id
    """
    # Get the item requested
    mlw = MarinaLitterWatch.query.filter(
        MarinaLitterWatch.mlw_id == mlw_id).one_or_none()

    # Did we find a mlw?
    if mlw is not None:

        # Serialize the data for the response
        mlw_schema = MarinaLitterWatchSchema()
        data = mlw_schema.dump(mlw)
        return data

    # Otherwise, nope, didn't find that item
    else:
        abort(
            404,
            "MLW Register not found for Id: {mlw_id}".format(
                mlw_id=mlw_id),
        )


def create(mlw):
    """
    This function creates a new item in the mlw structure
    based on the passed in mlw data

    :param mlw:  item to create in mlw structure
    :return:           201 on success, 406 on mlw exists
    """
    appid = mlw.get("appid")
    hname = mlw.get("hname")

    existing_mlw = (MarinaLitterWatch.query.filter(
        MarinaLitterWatch.appid == appid).filter(
            MarinaLitterWatch.hname == hname).one_or_none())

    # Can we insert this item?
    if existing_mlw is None:

        # Create a mlw instance using the schema and the passed in item
        schema = MarinaLitterWatchSchema()
        new_mlw = schema.load(mlw, session=db.session)

        # Add the mlw to the database
        db.session.add(new_mlw)
        db.session.commit()

        # Serialize and return the newly created mlw in the response
        data = schema.dump(new_mlw)

        return data, 201

    # Otherwise, nope, mlw exists already
    else:
        abort(
            409,
            "MLW Register {appid} {hname} exists already".format(
                appid=appid, hname=hname),
        )


def update(mlw_id, mlw):
    """
    This function updates an existing item in the mlw structure

    :param mlw_id:   Id of the mlw to update
    :param mlw:      mlw to update
    :return:               updated mlw structure
    """
    # Get the item requested from the db into session
    update_mlw = MarinaLitterWatch.query.filter(
        MarinaLitterWatch.mlw_id == mlw_id).one_or_none()

    # Did we find a item?
    if update_mlw is not None:

        # turn the passed in mlw into a db object
        schema = MarinaLitterWatchSchema()
        update = schema.load(mlw, session=db.session)

        # Set the id to the mlw we want to update
        update.mlw_id = update_mlw.mlw_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated mlw in the response
        data = schema.dump(update_mlw)

        return data, 200

    # Otherwise, nope, didn't find that item
    else:
        abort(
            404,
            "MLW Register not found for Id: {mlw_id}".format(
                mlw_id=mlw_id),
        )


def delete(mlw_id):
    """
    This function deletes an item from the mlw structure

    :param mlw_id:   Id of the mlw to delete
    :return:               200 on successful delete, 404 if not found
    """
    # Get the item requested
    mlw = MarinaLitterWatch.query.filter(
        MarinaLitterWatch.mlw_id == mlw_id).one_or_none()

    # Did we find a MLW Register?
    if mlw is not None:
        db.session.delete(mlw)
        db.session.commit()
        return make_response(
            "MLW Register {mlw_id} deleted".format(
                mlw_id=mlw_id), 200)

    # Otherwise, nope, didn't find that mlw
    else:
        abort(
            404,
            "MLW Register not found for Id: {mlw_id}".format(
                mlw_id=mlw_id),
        )
