import requests
from typing import List
import io
import zipfile
import os
import tempfile

API_URL = "https://api.ideogram.ai/v1/ideogram-v3/generate"

def _raise_for_status_verbose(r: requests.Response):
    try:
        detail = r.json()
    except Exception:
        detail = r.text
    r.raise_for_status()  # genererà l'eccezione, ma prima salvo i dettagli
    return detail

def generate_images(
    api_key: str,
    prompt: str,
    aspect_ratio: str = "",
    resolution: str = "",
    num_images: int = 1,
    seed: str = "",
    negative_prompt: str = "",
    style_type: str = "",
    rendering_speed: str = "",
    magic_prompt: str = "",
    # se in futuro userai riferimenti di stile/character, passali qui:
    style_reference_images: list | None = None,
    character_reference_images: list | None = None,
) -> List[bytes]:
    """
    Genera immagini con Ideogram.
    - Se NON ci sono file da caricare -> invia JSON (più stabile per text-only).
    - Se ci sono file -> usa multipart/form-data.
    Restituisce un array di bytes PNG.
    """
    style_reference_images = style_reference_images or []
    character_reference_images = character_reference_images or []

    # Build dei parametri (solo quelli valorizzati)
    payload = {"prompt": prompt}
    for k, v in [
        ("aspect_ratio", aspect_ratio),
        ("resolution", resolution),
        ("num_images", num_images),
        ("seed", seed),
        ("negative_prompt", negative_prompt),
        ("style_type", style_type),
        ("rendering_speed", rendering_speed),
        ("magic_prompt", magic_prompt),
    ]:
        if v not in ("", None):
            payload[k] = v

    headers = {"Api-Key": api_key}

    # Se non abbiamo file -> JSON (come da quickstart ufficiale)
    if not style_reference_images and not character_reference_images:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=90)
        if r.status_code >= 400:
            try:
                msg = r.json()
            except Exception:
                msg = r.text
            raise requests.HTTPError(f"{r.status_code} {r.reason}: {msg}")
    else:
        # Multipart (per quando caricherai immagini di stile/character)
        files = list(payload.items())
        for img in style_reference_images:
            files.append(("style_reference_images", img))
        for img in character_reference_images:
            files.append(("character_reference_images", img))
        r = requests.post(API_URL, headers=headers, files=files, timeout=90)
        if r.status_code >= 400:
            try:
                msg = r.json()
            except Exception:
                msg = r.text
            raise requests.HTTPError(f"{r.status_code} {r.reason}: {msg}")

    data = r.json().get("data", [])
    out = []
    for item in data:
        url = item.get("url")
        if not url:
            continue
        img = requests.get(url, timeout=90)
        if img.status_code >= 400:
            try:
                msg = img.json()
            except Exception:
                msg = img.text
            raise requests.HTTPError(f"Download error {img.status_code}: {msg}")
        out.append(img.content)
    return out

def save_images_to_temp(images: List[bytes], prefix: str = "image") -> List[str]:
    temp_dir = tempfile.mkdtemp(prefix="wealth_vision_")
    paths = []
    for i, b in enumerate(images, start=1):
        p = os.path.join(temp_dir, f"{prefix}_{i}.png")
        with open(p, "wb") as f:
            f.write(b)
        paths.append(p)
    return paths

def create_zip_from_files(file_paths: List[str]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for p in file_paths:
            z.write(p, arcname=os.path.basename(p))
    buf.seek(0)
    return buf.read()

