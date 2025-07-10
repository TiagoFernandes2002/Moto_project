CONFIG = {
    "CAN_BUS_CHANNEL": "can0",
    "ARBITRATION_IDS": {
        "BlindSpotDetection": 0x120,
        "RearCollision": 0x110,
        "FrontalCollision": 0x100,
        "PedestrianDetection": 0x105
    },
    "MQTT": {
        "ENABLED": True,
        "BROKER": "172.20.0.175",
        "PORT": 1883,
        "TOPIC": "amover/alertas"
    },
    "PRIORITY_LEVELS": {
        "1": "Severe",
        "2": "Medium",
        "3": "Light"
    }
}
