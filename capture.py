import os
from datetime import datetime

import cv2
import numpy as np

OUTPUT_PATH = "./images"
cap = cv2.VideoCapture(0)


def save_image(
        image: np.ndarray,
        output_path: str
):
    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name: str = f"{timestamp}.jpg"
    file_path: str = os.path.join(output_path, file_name)
    cv2.imwrite(filename=file_path, img=image)
    print(f"Imagem salva como {file_name}")


while True:

    status: bool
    frame: np.ndarray
    status, frame = cap.read()
    key: int = cv2.waitKey(delay=1)

    frame: np.ndarray = cv2.resize(
        src=frame,
        dsize=(1024, 1024)
    )

    cv2.imshow(
        winname="Camera",
        mat=frame
    )

    if key == ord("c"):
        save_image(
            image=frame,
            output_path=OUTPUT_PATH
        )
    elif key == 27:
        break
