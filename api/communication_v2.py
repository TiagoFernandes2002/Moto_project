import can
from shared.config import CONFIG
from datetime import datetime

def json_to_can(data):
    """
    Converte os dados da deteção para uma mensagem CAN.
    """
    algorithm = data["AlgorithmID"]
    priority = CONFIG["PRIORITY_LEVELS"].get(algorithm, 3)
    arbitration_id = CONFIG["ARBITRATION_IDS"].get(algorithm, 0x1FF) - priority

    # Timestamp da deteção
    timestamp_dt = datetime.fromisoformat(data["Timestamp"].replace("Z", ""))

    minuto = timestamp_dt.minute
    segundo = timestamp_dt.second
    micros_6dec = timestamp_dt.microsecond

    message_id = int(data["MessageID"])  # Garante que é inteiro

    can_data = [
        1 if data["Status"] else 0,
        1 if data["Data"]["Object"] == "person" else 0,
        minuto,
        segundo,
        (micros_6dec >> 0) & 0xFF,
        (micros_6dec >> 8) & 0xFF,
        (micros_6dec >> 16) & 0xFF,
        message_id & 0xFF
    ]

    message = can.Message(
        arbitration_id=arbitration_id,
        data=can_data,
        is_extended_id=False
    )

    return message, timestamp_dt  # retorna também o tempo da deteção

def send_can_message(data):
    """
    Envia uma mensagem CAN e imprime a latência entre deteção e envio.
    """
    message, timestamp_deteccao = json_to_can(data)

    try:
        bus = can.interface.Bus(channel=CONFIG["CAN_BUS_CHANNEL"], bustype="socketcan")
        timestamp_envio = datetime.utcnow()

        bus.send(message)
        bus.shutdown()

        # Cálculo da diferença
        latencia = (timestamp_envio - timestamp_deteccao).total_seconds() * 1000  # em ms

        print(f"[CAN] Tempo deteção: {timestamp_deteccao.time()} | Envio: {timestamp_envio.time()} | Diferença: {latencia:.2f} ms")

    except can.CanError as e:
        print(f"[CAN] Erro no envio: {e}")
