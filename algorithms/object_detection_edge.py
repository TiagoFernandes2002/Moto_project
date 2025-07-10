# from datetime import datetime
# # from algorithms.edgetpuyolo.utils import get_image_tensor
# # from algorithms.edgetpuyolo.edgetpumodel import EdgeTPUModel
# from processing.handler import handle_detection
# import logging
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# # Inicializar modelo
# model = EdgeTPUModel(
#     './algorithms/edgetpuyolo/yolov5n-int8_edgetpu_160.tflite',  # <-- substitui pelo caminho real
#     './algorithms/edgetpuyolo/data/coco.yaml',
#     conf_thresh=0.25,
#     iou_thresh=0.45,
#     v8=False
# )
# input_size = model.get_image_size()
#
#
# # Apenas a classe "Person"
# CLASSES = {
#     "person": "Person"
# }
#
# def detect_objects(frame, count):
#     """
#     Processa um frame e identifica objetos de interesse (apenas Pessoas).
#     """
#     full_image, net_image, pad = get_image_tensor(frame, input_size[0])
#     #print(full_image)
#     #print(net_image)
#     #print(pad)
#     predictions = model.predict(net_image)
#
#     model.process_predictions(predictions[0], full_image, pad)
#
#     tinference, tnms = model.get_last_inference_time()
#     logger.info("Frame done in {}".format(tinference + tnms))
#
#     i = count
#     #print(i)
#     # for detection in boxes:
#     #     cls_id = int(detection[5])
#     #     class_name = model.names[cls_id]
#     #
#     #     if class_name == "person":
#     #         width = detection[2] - detection[0]
#     #         height = detection[3] - detection[1]
#     #         area = width * height
#     #
#     #         data = {
#     #             "AlgorithmID": "Person",
#     #             "Timestamp": datetime.utcnow().isoformat() + "Z",
#     #             "Priority": "High" if area > 5000 else "Medium",
#     #             "Status": True,
#     #             "MessageID": i,
#     #             "Data": {
#     #                 "Object": class_name
#     #             }
#     #         }
#     #
#     #         handle_detection(data)
#     #
#     #     i += 1
#
#     return i
