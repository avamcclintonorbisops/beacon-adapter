# beacon-adapter

Beacon Adapter
The Beacon Adapter is a lightweight Flask-based web service that I built during my internship at Orbis Operations. Its purpose is to collect telemetry from Teltonika Eye beacons and expose that data to the Catalyst platform in a format that supports real-time awareness, monitoring, and decision-making.

Overview
The adapter acts as a bridge between physical sensors in the field and a software intelligence platform. Beacon data is received from a Teltonika router, indexed in memory, and then made accessible through a GraphQL API.
This enables users, dashboards, or tools like Catalyst to query the status of deployed devices, without requiring direct access to the router or low-level protocols.

How It Works
  1. Beacon Data Ingestion
The Teltonika router sends telemetry to:
POST /beacons
Payloads include:
Beacon ID or name
Battery level
Temperature
Movement / gyro data
Input status
GPS coordinates (when available)
Every time new data arrives, the service updates that beacon’s entry in an internal dictionary:
beacon_index = {}
Each beacon always reflects its most recent state.

  2. GraphQL Endpoint
A GraphQL API is exposed at:
/graphql
Supported queries:
beacons → return all devices
beacon(id) → return one device
beacons(ids) → return a selected list
The adapter also implements the:
{ _sdl }
introspection query, allowing Catalyst to automatically pull the schema and connect without manual configuration.
  
  3. JWT Validation
To secure access, the service performs JWT validation:
Checks the token signature (Ed25519)
Enforces expiration
Confirms the channel_id matches config
Tokens must be valid to access GraphQL results.
During development, I created a mode where signature enforcement was temporarily relaxed so teammates could query the adapter more easily while building dashboards.
  
  4. Deployment
The service runs as a container using Docker, with automated deployment to Fly.io.

Example URL:
https://beacon-adapter-dev.fly.dev
The router was configured to send telemetry directly to this endpoint.

Real-World Use
This adapter was used to feed live sensor data into Catalyst.

It allowed:
Remote teams to monitor beacon movement
Battery and environmental status awareness
On-screen visualization of sensors in the field
Faster alerts when something changed

I used real devices and a Teltonika RUTX11 router to generate beacon traffic. Debugging was done using browser tabs and logs at:
GET /beacons
which showed incoming updates in real time.

Challenges Solved
During development, I fixed several real-world problems, including:
Router sending invalid JSON ("input2": N/A)
Handling intermittent GPS availability
Token and channel validation issues
Live deployment and polling performance
These issues required debugging, logging, and collaboration with teammates on both the development and field sides.

Purpose
This project demonstrates how a small, focused service can unlock value by connecting:
Physical devices
Network routers
Cloud microservices
GraphQL
Security controls
Operational dashboards
The Beacon Adapter is a foundational building block in a modular system that automates the flow of telemetry into decision-making platforms.

Sample GraphQL Queries
Once the adapter is running (and JWT is valid), you can query it with any GraphQL client, cURL, or Catalyst.
1. Get all beacons
query {
  beacons {
    id
    battery
    temperature
    movement
    gps {
      lat
      lon
    }
    updatedAt
  }
}

What it returns:
A list of all currently known beacons
Their status values
Latest timestamps

2. Get a single beacon by ID
query {
  beacon(id: "BEACON_123") {
    id
    battery
    temperature
    movement
    gps {
      lat
      lon
    }
    updatedAt
  }
}
Useful for:
Dashboards
Alerting logic
Investigating an exact device

3. Get multiple selected beacons
query {
  beacons(ids: ["BEACON_123", "BEACON_456"]) {
    id
    battery
    movement
    updatedAt
  }
}
This is helpful when:
Monitoring priority devices
Filtering for a specific group

4. SDL Introspection (for Catalyst)
query {
  _sdl
}
Catalyst uses this response to:
Read the schema automatically
Connect without manual setup
Validate your queries
You don’t need to write anything custom — Catalyst discovers the API using _sdl.

5. Simple curl example
curl -X POST https://your-adapter.fly.dev/graphql \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ beacons { id battery } }"}'
Response:
{
  "data": {
    "beacons": [
      { "id": "BEACON_123", "battery": 94 },
      { "id": "BEACON_456", "battery": 88 }
    ]
  }
}

Notes
If authentication is enabled, you must pass a valid JWT token in the Authorization header.
Without a token (or with a bad token), the service responds with HTTP 401 Unauthorized.
