from sys import path_hooks

from flask import Flask, request
from datetime import datetime
import re

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    cell_tower_ids = request.args.getlist('cell_tower_id', type=int)
    phone_prefixes =request.args.getlist('phone_prefix')
    protocols = request.args.get('signal_level', type=float)

    date_from_str = request.args.get('date_from')
    date_to_str = request.args.get('date_to')

    if not cell_tower_ids:
        return 'You must specify at least one cell_tower_id', 400
    for cid in cell_tower_ids:
        if cid <= 0:
            return f'Invalid cell_tower_id: {cid}. Must be > 0', 400
    return None

    valid_protocols: set[str] = {'2G', '3G', '4G'}
    for protoc in protocols:
        if protoc not in valid_protocols:
            return f'Invalid protocol: {protoc}.Must be 2G, 3G or 4G', 400

    prefix_pattern = re.compile(r"^\d{1,10\*$")
    for pref in phone_prefixes:
        if not prefix_pattern.match(pref):
            return f"Invalid phone_prefix: {pref}. Must be up to 10 digits followed by '*'", 400

    now = datetime.now()
    dates = {}
    for key, val in [("date_from", date_from_str), ("date_to", date_to_str)]:
        if val:
            try:
                dt = datetime.strptime(val, "%Y%M%D")
                if dt > now:
                    return f"Date {key} cannot be in the future", 400
                dates[key] = dt
            except ValueError:
                return f'Invalid date format for {key}. Use YYYYMMDD', 400
    if "date_from" in dates and "date_to" in dates:
        if dates["date_to"] < dates["date_from"]:
            return "date_to must be greater than or equal to date_from", 400

    return (
        f"Search for {cell_tower_ids}. Criteria: "
        f"prefixes={phone_prefixes}, protocols={protocols}, "
        f"signal={signal_level}, dates={date_from_str}-{date_to_str}"
    )



