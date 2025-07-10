#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processo principal:
 – detecção (EdgeTPU + OpenCV)   [Processo-1]
 – envio CAN + registo em CSV    [Processo-2]

Removidos todos os print(), usando logging em vez disso.
Adicionados tempos de inferência, latência de fila, etc.
"""

import argparse
import logging
import os
import sys
import time
from datetime import datetime
from multiprocessing import Process, freeze_support

import cv2
import numpy as np

from edgetpuyolo.edgetpumodel import EdgeTPUModel
from utils import get_image_tensor
from processing.handler import handle_detection
from processing.message_queue import message_queue
from api.communication import send_can_message

# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
CLASSES = {"person": "Person"}

# ----------------------------------------------------------------------
def detector_proc(model_path, names_path,
                  conf_thresh, iou_thresh, v8,
                  source, is_stream):

    model = EdgeTPUModel(model_path, names_path,
                         conf_thresh=conf_thresh,
                         iou_thresh=iou_thresh,
                         v8=v8)
    input_size = model.get_image_size()

    cap = cv2.VideoCapture(int(source) if is_stream else source)
    if not cap.isOpened():
        logger.error("Não foi possível abrir a fonte de vídeo/stream.")
        return

    msg_id = 0
    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            logger.info("Fim do vídeo ou erro ao ler frame.")
            break

        # ------------ Inferência -----------------
        t0_ns = time.perf_counter_ns()
        full_img, net_img, pad = get_image_tensor(frame, input_size[0])
        pred = model.forward(net_img)
        inference_ms = (time.perf_counter_ns() - t0_ns) / 1e6
        # ------------------------------------------

        if pred and len(pred[0]):
            for det in pred[0]:
                cls_id = int(det[5])
                if model.names[cls_id].lower() not in CLASSES:
                    continue  # ignorar outras classes

                # decidir prioridade por área da bbox
                x1, y1, x2, y2, conf, _ = det
                area = (x2 - x1) * (y2 - y1)
                priority = "High" if area > 5_000 else "Medium"

                message = {
                    "AlgorithmID": CLASSES["person"],
                    "MessageID":  msg_id,
                    "Priority":   priority,
                    "Status":     True,
                    "Data": {"Object": "person"},

                    # ---------- métricas ----------
                    "timestamp_det_iso": datetime.utcnow().isoformat() + "Z",
                    "timestamp_det_ns":  t0_ns,
                    "inference_ms":      inference_ms,
                }
                msg_id += 1
                handle_detection(message)
                logger.debug(f"Frame OK – enfileirado ID {message['MessageID']}")

        # opcional: latência interna do modelo
        t_inf, t_nms = model.get_last_inference_time()
        logger.debug(f"Inference+NMS: {(t_inf+t_nms)*1e3:.2f} ms")

    cap.release()
    logger.info("Detector finalizado.")


# ----------------------------------------------------------------------
def sender_proc():
    """Processo separado: retira da Queue → envia CAN → regista CSV."""
    logger.info("Processo de envio CAN iniciado.")
    while True:
        data = message_queue.get()          # bloqueante
        data["queue_ms"] = (time.perf_counter_ns()
                            - data["timestamp_det_ns"]) / 1e6
        send_can_message(data)


# ----------------------------------------------------------------------
def _parse_cli():
    p = argparse.ArgumentParser("EdgeTPU detector multiprocessing")
    p.add_argument("-m", "--model", required=True, help=".tflite compilado p/ TPU")
    p.add_argument("--names", required=True, help="ficheiro .yaml com nomes")
    p.add_argument("--conf_thresh", type=float, default=0.25)
    p.add_argument("--iou_thresh",  type=float, default=0.45)
    p.add_argument("--image", "-i", help="vídeo de teste")
    p.add_argument("--stream", action="store_true", help="usar camera")
    p.add_argument("--device", type=int, default=0, help="índice camera")
    p.add_argument("--v8", action="store_true", help="modelo YOLOv8")
    return p.parse_args()


# ----------------------------------------------------------------------
if __name__ == "__main__":
    freeze_support()
    args = _parse_cli()

    src = args.device if args.stream else args.image
    if src is None:
        logger.error("Indica --image <ficheiro> ou --stream.")
        sys.exit(1)

    proc_det = Process(target=detector_proc,
                       args=(args.model, args.names,
                             args.conf_thresh, args.iou_thresh,
                             args.v8, src, args.stream))
    proc_send = Process(target=sender_proc)

    proc_det.start()
    proc_send.start()
    proc_det.join()
    proc_send.join()
