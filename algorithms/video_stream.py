import cv2


def video_capture(video_path, frame_queue):
    """
    Captura frames de um vídeo e envia para a fila de processamento.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("[ERROR] Não foi possível abrir o vídeo.")
        return

    print("[INFO] Iniciando captura de vídeo...")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("[INFO] Fim do vídeo.")
            break

        frame_queue.put(frame)

    cap.release()
    print("[INFO] Captura finalizada.")
