"""
Quick and dirty server between db and kivy
"""

from flask import Flask, Response, jsonify, request, render_template
from db_interface import db_interface_pg as dbi

app = Flask(__name__)


@app.route('/user/<can_dirty>')
def get_user_by_can(can_dirty):
    """
    Lookup the CAN provided and return a user row (or an error if there is no
    such user)

    :param can_dirty: CAN to be transformed into db format
    :return:
    """
    try:
        # transforming CAN into db format is done inside the db interface code
        response_raw = dbi.get_user_by_can(can_dirty, as_json=True)
        if response_raw:
            return Response(response_raw,
                            mimetype='application/json')
        else:
            # Empty string for no user
            return jsonify(error='no user')
    except ValueError as e:
        return jsonify(error=e.args[0])


@app.route('/item/by_user/<int:user_id>')
def get_user_items(user_id):
    """
    Get all of a user's deposited items, most recent first

    :param user_id: user id (not the CAN)
    :return:
    """
    try:
        return Response(dbi.get_user_items(user_id, as_json=True),
                        mimetype='application/json')
    except ValueError as e:
        return jsonify(error=e.args[0])


@app.route('/leaderboard')
def leaderboard():
    """
    Returns the leaderboard.

    This is run through the template to get a pretty html output
    :return:
    """
    return render_template('full-screen-table.html', result=dbi.get_leaderboard())


@app.route('/user', methods=['POST'])
def create_user():
    """
    Add a new user to the db
    name and phone_number can be None
    :return:
    """
    try:
        params_raw = request.get_json()
        # only want these 4 keys
        params = {k: v for k, v in params_raw.items()
                  if k in ('can', 'name', 'display_name', 'phone_number')}

        # but if we didn't get exactly 4 params...
        if len(params) != 4:
            raise ValueError('Parameter error')

        user_id = dbi.create_user(
            **params,
            active=True
        )

        # return the user id
        return jsonify(user_id=user_id)
    except ValueError as e:
        return jsonify(error=e.args[0])


@app.route('/item', methods=['POST'])
def create_item():
    """
    Add a new item (by depositing into the bin).
    category is an int! deposited_by is a user id (see next function for a more
    convenient endpoint)

    :return:
    """
    try:
        params_raw = request.get_json()
        params = {k: v for k, v in params_raw.items()
                  if k in ('score', 'mass', 'category', 'deposited_by')}

        if len(params) != 4:
            raise ValueError('Parameter error')

        item_id = dbi.create_item(**params)

        return jsonify(item_id=item_id)
    except ValueError as e:
        return jsonify(error=e.args[0])


@app.route('/item/by_can', methods=['POST'])
def create_item_by_can():
    """
    Add a new item, using a user's CAN to access their id.
    :return:
    """
    try:
        params_raw = request.get_json()
        params = {k: v for k, v in params_raw.items()
                  if k in ('score', 'mass', 'category', 'depositing_can')}

        if len(params) != 4:
            raise ValueError('Parameter error')

        item_id = dbi.create_item_by_can(**params)

        return jsonify(item_id=item_id)
    except ValueError as e:
        return jsonify(error=e.args[0])

if __name__ == "__main__":
    app.run()
