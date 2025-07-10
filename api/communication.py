import atexit
import csv
import logging
import time
from datetime import datetime

import can

from shared.config import CONFIG

log = logging.getLogger(__name__)

# ---------- CSV (em tmpfs para não cansar o cartão) ----------
CSV_FILE = "results/amover_results.csv"   # cria pasta results/ no projeto

csv_fh = open(CSV_FILE, "a", buffering=1, newline="")
csv_wr = csv.writer(csv_fh)
if csv_fh.tell() == 0:          # cabeçalho se novo
    csv_wr.writerow([
        "t_env_iso",
        "t_det_iso",
        "lat_ms_tot",
        "infer_ms",
        "queue_ms",
        "msg_id",
        "alg",
        "prio",
        "status",
        "obj",
    ])
atexit.register(csv_fh.close)

# ---------- CAN ----------
bus = can.interface.Bus(channel=CONFIG["CAN_BUS_CHANNEL"],
                        bustype="socketcan")

_last_flush = time.monotonic()


def json_to_can(data: dict) -> can.Message:
    """Converte dicionário em can.Message."""
    alg = data["AlgorithmID"]
    prio = CONFIG["PRIORITY_LEVELS"].get(alg, 3)
    arb_id = CONFIG["ARBITRATION_IDS"].get(alg, 0x1FF) - prio

    t_det = datetime.fromisoformat(data["timestamp_det_iso"].rstrip("Z"))
    can_bytes = [
        1 if data["Status"] else 0,
        1,                                        # object==person
        t_det.minute,
        t_det.second,
        (t_det.microsecond >>  0) & 0xFF,
        (t_det.microsecond >>  8) & 0xFF,
        (t_det.microsecond >> 16) & 0xFF,
        data["MessageID"] & 0xFF,
    ]
    return can.Message(arbitration_id=arb_id,
                       data=can_bytes,
                       is_extended_id=False)


def send_can_message(data: dict):
    """Envia no barramento CAN e escreve CSV."""
    try:
        bus.send(json_to_can(data), timeout=0.005)
    except can.CanError as e:
        log.error(f"Erro CAN: {e}")
        return

    now_iso = datetime.utcnow().isoformat() + "Z"
    total_ms = (time.perf_counter_ns() - data["timestamp_det_ns"]) / 1e6

    csv_wr.writerow([
        now_iso,
        data["timestamp_det_iso"],
        f"{total_ms:.3f}",
        f"{data['inference_ms']:.3f}",
        f"{data.get('queue_ms',0):.3f}",
        data["MessageID"],
        data["AlgorithmID"],
        data["Priority"],
        data["Status"],
        data["Data"]["Object"],
    ])

    global _last_flush
    if time.monotonic() - _last_flush > 2:
        csv_fh.flush()
        _last_flush = time.monotonic()
