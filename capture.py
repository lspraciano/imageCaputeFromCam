import os
from datetime import datetime

import cv2
import numpy as np

ZOOM: str = "objetiva_marcada_10x"
OUTPUT_PATH: str = f"./images/{ZOOM}"
SAMPLE_NAME: str = "sample_072"


def create_sample_dir(output_path: str, sample_name: str) -> str:
    sample_dir: str = os.path.join(output_path, sample_name)
    os.makedirs(name=sample_dir, exist_ok=True)
    return sample_dir


def save_image(image: np.ndarray, sample_dir: str, sample_name: str):
    existing_images = [
        f for f in os.listdir(sample_dir)
        if f.startswith(sample_name) and f.endswith(".jpg")
    ]
    sequence_number = len(existing_images) + 1
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{sample_name}_{timestamp}_{sequence_number}.jpg"
    file_path = os.path.join(sample_dir, file_name)

    print(f"Tentando salvar em: {file_path}")
    print(f"Imagem shape: {image.shape}, dtype: {image.dtype}")

    success = cv2.imwrite(file_path, image)
    if success:
        print(f"✅ Imagem salva como {file_path}")
    else:
        print("❌ Falha ao salvar a imagem com cv2.imwrite()")


def capture_loop(output_path: str, sample_name: str):
    cap: cv2.VideoCapture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Defina a resolução desejada (4K)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

    # Verifique se a câmera abriu corretamente
    if not cap.isOpened():
        print("❌ Erro: câmera não conectada ou inacessível.")
        return

    # Mostrar resolução real
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"📷 Resolução atual da câmera: {int(actual_width)}x{int(actual_height)}")

    sample_dir: str = create_sample_dir(output_path, sample_name)

    while True:
        status, frame = cap.read()
        key = cv2.waitKey(1)

        if not status or frame is None:
            print("❌ Erro ao capturar imagem da câmera.")
            break

        # Armazena o frame original para salvar
        original_frame = frame.copy()

        # Redimensiona apenas para visualização
        display_frame = cv2.resize(original_frame, (1024, 640))
        cv2.imshow("Camera", display_frame)

        if key == ord("c"):
            save_image(original_frame, sample_dir, sample_name)
        elif key == 27:  # Esc para sair
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_loop(OUTPUT_PATH, SAMPLE_NAME)
