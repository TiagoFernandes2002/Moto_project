import logging

from edgetpumodel import EdgeTPUModel

# Optional: set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar modelo
model = EdgeTPUModel(
    './edgetpuyolo/yolov5n-int8_edgetpu_160.tflite',  # <-- substitui pelo caminho real
    './edgetpuyolo/data/coco.yaml',
    conf_thresh=0.25,
    iou_thresh=0.45,
    v8=False
)


def run_inference(image_path):
    """
    Run object detection on a single image using EdgeTPU YOLO model.

    Args:
        image_path (str): Path to the input image.

    Returns:
        List[Dict]: List of detection results (bounding boxes, scores, class labels, etc.).
    """
    # Perform prediction
    print(22222)
    logger.info(f"Running inference on image: {image_path}")
    results = model.predict(image_path)

    return results
