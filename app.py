from flask import Flask, request, jsonify
from graphene import ObjectType, String, Field, Schema
import graphene
import json
import os
import jwt

app = Flask(__name__)

# ------------------ BEACON MEMORY STORE ------------------ #
beacon_index = {}

# ------------------ GRAPHQL TYPES ------------------ #

class BeaconType(graphene.ObjectType):
    name = graphene.String()
    beacon = graphene.String()
    gps = graphene.String()

class Query(graphene.ObjectType):
    beacons = graphene.List(BeaconType)
    beacon = graphene.Field(BeaconType, name=graphene.String(required=True))
    beacons_by_names = graphene.List(BeaconType, names=graphene.List(graphene.String, required=True))
    sdl = graphene.String(name="_sdl")  # Exposed as _sdl in GraphQL

    def resolve_beacons(parent, info):
        return [
            BeaconType(name=name, beacon=json.dumps(data["beacon"]), gps=json.dumps(data["gps"]))
            for name, data in beacon_index.items()
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

    def resolve_sdl(parent, info):
        return str(schema)

schema = Schema(query=Query)

# ------------------ ROUTES ------------------ #

@app.route('/')
def home():
    return "Beacon Adapter (Dev) is running!"

@app.route('/beacons', methods=['POST'])
def handle_beacon():
    try:
        data = request.get_json(silent=True)
        if not data:
            raw_body = request.data.decode('utf-8')
            cleaned = raw_body.replace('input2":{{', 'input2":{').replace('}}}', '}}')
            data = json.loads(cleaned)

        input1 = data.get("input1", [])
        input2 = data.get("input2", {})

        for item in input1:
            name = item.get("name")
            if name:
                beacon_index[name] = {
                    "beacon": item,
                    "gps": input2
                }

        return jsonify({"message": "Data stored successfully."}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 400

@app.route('/beacons', methods=['GET'])
def get_beacons():
    return jsonify(beacon_index)

@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    query = data.get("query", "")

    # ✅ Always require a token
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split(" ")[1]

    try:
        # ✅ Just decode to inspect — no signature or channel check
        decoded_claims = jwt.decode(token, options={"verify_signature": False})
        print("Token unpacked:", decoded_claims)
    except Exception as e:
        print("Token decode failed:", e)
        return jsonify({"error": "Could not decode token"}), 401

    # ✅ Allow entry regardless of channel match
    result = schema.execute(query)
    return jsonify({
        "data": result.data,
        "errors": [str(e) for e in result.errors] if result.errors else None
    })

# ------------------ RUN ------------------ #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
