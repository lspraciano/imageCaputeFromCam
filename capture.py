import os
from datetime import datetime

import cv2
import numpy as np

TASK_TYPE: str = "objetiva_marcada_10x"
OUTPUT_PATH: str = f"./images/{TASK_TYPE}"
SAMPLES_NUMBER: int = 10
IMAGES_PER_SAMPLE: int = 5
ZERO_FILL_NUMBER: int = 3
SAMPLE_NAME_PREFIX: str = "sample_"


def create_sample_dir(
        output_path: str,
        sample_name: str
) -> str:
    sample_dir: str = os.path.join(
        output_path,
        sample_name
    )

    os.makedirs(
        name=sample_dir,
        exist_ok=True
    )

    return sample_dir


def save_image(
        image: np.ndarray,
        sample_dir: str,
        sample_name: str
):
    existing_images = [
        f for f in os.listdir(path=sample_dir)
        if f.startswith(sample_name) and f.endswith(".jpg")
    ]
    sequence_number = len(existing_images) + 1
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{sample_name}_{timestamp}_{sequence_number}.jpg"
    file_path = os.path.join(sample_dir, file_name)

    print(f"Tentando salvar em: {file_path}")
    print(f"Imagem shape: {image.shape}, dtype: {image.dtype}")

    success = cv2.imwrite(
        filename=file_path,
        img=image
    )
    if success:
        print(f"✅ Imagem salva como {file_path}")
    else:
        print("❌ Falha ao salvar a imagem com cv2.imwrite()")


def loop():
    os.makedirs(
        name=OUTPUT_PATH,
        exist_ok=True
    )

    for sample in range(1, SAMPLES_NUMBER + 1):
        sample_zerofill: str = str(sample).zfill(ZERO_FILL_NUMBER)
        sample_name: str = SAMPLE_NAME_PREFIX + sample_zerofill
        sample_dir: str = os.path.join(
            OUTPUT_PATH,
            sample_name
        )

        os.makedirs(
            name=sample_dir,
            exist_ok=True
        )

        images_on_sample_dir: list[str] = []

        for file in os.listdir(path=sample_dir):
            file_full_path: str = os.path.join(
                sample_dir,
                file
            )

            if file.startswith(sample_name) and file.endswith(".jpg"):
                images_on_sample_dir.append(file_full_path)
            else:
                os.remove(file_full_path)

        if len(images_on_sample_dir) >= IMAGES_PER_SAMPLE:
            continue

        current_number_of_images: int = len(images_on_sample_dir)
        cap: cv2.VideoCapture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(propId=cv2.CAP_PROP_FRAME_WIDTH, value=3840)
        cap.set(propId=cv2.CAP_PROP_FRAME_HEIGHT, value=2160)

        if not cap.isOpened():
            print("❌ Erro: câmera não conectada ou inacessível.")
            return

        actual_width: float = cap.get(propId=cv2.CAP_PROP_FRAME_WIDTH)
        actual_height: float = cap.get(propId=cv2.CAP_PROP_FRAME_HEIGHT)
        print(f"📷 Resolução atual da câmera: {int(actual_width)}x{int(actual_height)}")

        while current_number_of_images < IMAGES_PER_SAMPLE:
            sequence_number: int = current_number_of_images + 1
            timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_name: str = f"{sample_name}_{timestamp}_{sequence_number}.jpg"
            image_full_path: str = os.path.join(sample_dir, image_name)
            status, frame = cap.read()
            key: int = cv2.waitKey(delay=1)

            if not status or frame is None:
                print("❌ Erro ao capturar imagem da câmera.")
                break

            original_frame: np.ndarray = frame.copy()

            display_frame: np.ndarray = cv2.resize(
                src=original_frame,
                dsize=(1024, 640)
            )

            cv2.putText(
                img=display_frame,
                text=f"{sample_name}_{sequence_number}.jpg",
                org=(20, 30),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.8,
                color=(0, 255, 0),
                thickness=2,
                lineType=cv2.LINE_AA
            )

            cv2.imshow(
                winname="Camera",
                mat=display_frame
            )

            if key == ord("c"):
                print(f"Tentando salvar em: {image_full_path}")
                print(f"Imagem shape: {original_frame.shape}, dtype: {original_frame.dtype}")

                success = cv2.imwrite(
                    filename=image_full_path,
                    img=original_frame
                )

                if success:
                    print(f"✅ Imagem salva como {image_full_path}")

                else:
                    print("❌ Falha ao salvar a imagem com cv2.imwrite()")

                current_number_of_images += 1

            elif key == 27:
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    loop()
