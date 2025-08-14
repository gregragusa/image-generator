import requests
from typing import List
import io
import zipfile
import os
import tempfile

# Endpoint Ideogram v3
API_URL = "https://api.ideogram.ai/v1/ideogram-v3/generate"


def generate_images(api_key: str, prompt: str,
                    aspect_ratio: str = "",
                    resolution: str = "",
                    num_images: int = 1,
                    seed: str = "",
                    negative_prompt: str = "",
                    style_type: str = "",
                    rendering_speed: str = "",
                    magic_prompt: str = "") -> List[bytes]:
    """Invia un prompt all’API Ideogram e ritorna le immagini come byte."""
    data = {"prompt": prompt}
    # Aggiungi solo i parametri opzionali non vuoti
    for key, value in [
        ("aspect_ratio", aspect_ratio),
        ("resolution", resolution),
        ("num_images", num_images),
        ("seed", seed),
        ("negative_prompt", negative_prompt),
        ("style_type", style_type),
        ("rendering_speed", rendering_speed),
        ("magic_prompt", magic_prompt),
    ]:
        if value:
            data[key] = str(value)
    response = requests.post(
        API_URL,
        headers={"Api-Key": api_key},
        files=list(data.items()),
        timeout=60,
    )
    response.raise_for_status()
    images = []
    for item in response.json().get("data", []):
        url = item.get("url")
        if url:
            img_resp = requests.get(url, timeout=60)
            img_resp.raise_for_status()
            images.append(img_resp.content)
    return images


def save_images_to_temp(images: List[bytes], prefix: str = "image") -> List[str]:
    """Salva le immagini in una cartella temporanea e ritorna i percorsi."""
    temp_dir = tempfile.mkdtemp(prefix="wealth_vision_")
    file_paths = []
    for idx, img_bytes in enumerate(images, start=1):
        file_path = os.path.join(temp_dir, f"{prefix}_{idx}.png")
        with open(file_path, "wb") as f:
            f.write(img_bytes)
        file_paths.append(file_path)
    return file_paths


def create_zip_from_files(file_paths: List[str]) -> bytes:
    """Crea un archivio ZIP in memoria a partire da una lista di file."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for path in file_paths:
            zf.write(path, arcname=os.path.basename(path))
    buf.seek(0)
    return buf.read()
