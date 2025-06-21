import os
from datetime import datetime

import cv2
import numpy as np

OUTPUT_PATH: str = "./images"
SAMPLE_NAME: str = "sample_002"


def create_sample_dir(
        output_path: str,
        sample_name: str
) -> str:
    sample_dir: str = os.path.join(output_path, sample_name)
    os.makedirs(name=sample_dir, exist_ok=True)
    return sample_dir


def save_image(
        image: np.ndarray,
        sample_dir: str,
        sample_name: str
):
    existing_images = []
    for f in os.listdir(sample_dir):
        if f.startswith(sample_name) and f.endswith(".jpg"):
            existing_images.append(f)

    sequence_number = len(existing_images) + 1

    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name: str = f"{sample_name}_{timestamp}_{sequence_number}.jpg"
    file_path: str = os.path.join(sample_dir, file_name)

    cv2.imwrite(filename=file_path, img=image)
    print(f"Imagem salva como {file_path}")


def capture_loop(
        output_path: str,
        sample_name: str
):
    cap: cv2.VideoCapture = cv2.VideoCapture(0)

    sample_dir: str = create_sample_dir(
        output_path=output_path,
        sample_name=sample_name
    )

    while True:
        status: bool
        frame: np.ndarray
        status, frame = cap.read()
        key: int = cv2.waitKey(delay=1)

        if not status:
            print("Erro ao capturar imagem da câmera.")
            break

        frame: cv2.typing.MatLike = cv2.resize(src=frame, dsize=(800, 800))

        cv2.imshow(winname="Camera", mat=frame)

        if key == ord("c"):
            save_image(image=frame, sample_dir=sample_dir, sample_name=sample_name)
        elif key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_loop(OUTPUT_PATH, SAMPLE_NAME)
