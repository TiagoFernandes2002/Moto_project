from ultralytics import YOLO
model = YOLO("yolo11n.pt")
input_size=(256,256)
model.export(format="onnx", imgsz=input_size)

# from onnxruntime.quantization import quantize_dynamic, QuantType

# # Define input and output ONNX model paths
# model_path = "yolo11s.onnx"
# quantized_model_path = "yolo11s_quantized.onnx"

# # Apply dynamic quantization
# quantize_dynamic(
#     model_input=model_path,
#     model_output=quantized_model_path,
#     weight_type=QuantType.QInt8  # Use QInt8 for INT8 quantization
# )

# print(f"Quantized model saved to {quantized_model_path}")
