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
    mlw = MarinaLitterWatch.query.order_by(
        MarinaLitterWatch.communityname).all()

    # Serialize the data for the response
    mlw_schema = MarinaLitterWatchSchema(many=True)
    data = mlw_schema.dump(mlw)
    return data


def read_one(index):
    """
    This function responds to a request for /mlw/{index}
    with one matching item from mlw

    :param index:   Id of mlw to find
    :return:               Mlw matching id
    """
    # Get the item requested
    mlw = MarinaLitterWatch.query.filter(
        MarinaLitterWatch.index == index).one_or_none()

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
            "MLW Register not found for Id: {index}".format(
                index=index),
        )
