from flask import Flask, request, jsonify
from graphene import ObjectType, String, Field, Schema
import graphene
import json
import re  # Needed for the _sdl support
import os
import base64
import requests
import jwt
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


app = Flask(__name__)

# In-memory store of beacons
beacon_index = {}

# ------------------------ FLASK ROUTES ------------------------ #

@app.route('/')
def home():
    return "Beacon Adapter is running!"

@app.route('/beacons', methods=['POST'])
def handle_beacon():
    try:
        data = request.get_json(silent=True)

        if not data:
            raw_body = request.data.decode('utf-8')
            print("Raw (non-JSON) request:", raw_body)
            cleaned = raw_body.replace('input2":{{', 'input2":{').replace('}}}', '}}')
            data = json.loads(cleaned)

        input1 = data.get("input1", [])
        input2 = data.get("input2", {})

        for item in input1:
            name = item.get("name")
            if not name:
                continue
            beacon_index[name] = {
                "beacon": item,
                "gps": input2
            }

        print("input1:", input1)
        print("input2:", input2)

        return jsonify({"message": "Data stored successfully."}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 400

@app.route('/beacons', methods=['GET'])
def get_beacons():
    return jsonify(beacon_index)

# ------------------------ GRAPHQL TYPES ------------------------ #

class BeaconType(graphene.ObjectType):
    name = graphene.String()
    beacon = graphene.String()
    gps = graphene.String()

class Query(graphene.ObjectType):
    beacons = graphene.List(BeaconType)
    beacon = graphene.Field(BeaconType, name=graphene.String(required=True))
    beacons_by_names = graphene.List(BeaconType, names=graphene.List(graphene.String, required=True))

    def resolve_beacons(parent, info):
        return [
            BeaconType(name=name, beacon=json.dumps(value["beacon"]), gps=json.dumps(value["gps"]))
            for name, value in beacon_index.items()
        ]

    def resolve_beacon(parent, info, name):
        if name in beacon_index:
            data = beacon_index[name]
            return BeaconType(name=name, beacon=json.dumps(data["beacon"]), gps=json.dumps(data["gps"]))
        return None

    def resolve_beacons_by_names(parent, info, names):
        return [
            BeaconType(name=name, beacon=json.dumps(beacon_index[name]["beacon"]), gps=json.dumps(beacon_index[name]["gps"]))
            for name in names if name in beacon_index
        ]

schema = Schema(query=Query)

@app.route('/graphql', methods=['POST'])
def graphql_server():
    # JWT validation is skipped for now
    # auth_header = request.headers.get("Authorization")
    # if not auth_header:
    #     return jsonify({"error": "Authorization header missing"}), 401

    # token = auth_header.split(" ")[1]
    # if not validate_jwt(token):
    #     return jsonify({"error": "Invalid JWT"}), 401

    data = request.get_json()
    query = data.get("query")

    # Handle SDL introspection for Catalyst
    if re.match(r"^\s*{\s*_sdl\s*}\s*$", query):
        return jsonify({"data": {"_sdl": str(schema)}})

    result = schema.execute(query)

    return jsonify({
        "data": result.data,
        "errors": [str(e) for e in result.errors] if result.errors else None
    })

# ------------------------ RUN APP ------------------------ #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
