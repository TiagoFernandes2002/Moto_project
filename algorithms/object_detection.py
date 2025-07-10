import time

from ultralytics import YOLO
from datetime import datetime
from processing.handler import handle_detection
from datetime import datetime
# Carregar o modelo de deteçãov
'''model = YOLO('person_trafficsign_640.pt')
model.fuse()  # Otimização para inferência

# Classes que nos interessam para deteção
CLASSES = {
    "person": "Person",
    "traffic sign": "Traffic Sign"
}'''


def detect_objects(frame, count):
    """
    Processa um frame e identifica objetos de interesse (Pessoas e Sinais de Trânsito).
    """
    results = model.predict(source=frame, conf=0.5)
    i = count
    for result in results:

        for detection in result.boxes.data.tolist():
            data = {
                "AlgorithmID": None,
                "Example": None,
                "Timestamp": "",
                "Priority": None,
                "Status": None,
                "MessageID": None,
                "Data": {
                    "Object": None
                }
            }

            class_name = model.names[int(detection[5])]

            if class_name in CLASSES:
                width = detection[2] - detection[0]
                height = detection[3] - detection[1]
                area = width * height
                #print(class_name)
                #print(time.monotonic())
                data = {
                    "AlgorithmID": CLASSES[class_name],
                    "Timestamp": datetime.utcnow().isoformat() + "Z",
                    "Priority": "High" if area > 5000 else "Medium",
                    "Status": True,
                    "MessageID": i,
                    "Data": {
                        "Object": class_name,
                    }
                }

                #print(f"[DETECTION] Evento gerado: {data}")
                handle_detection(data)

            i = i + 1

    return i