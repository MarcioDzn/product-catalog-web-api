import base64
import uuid

from app.supabase import supabase


BUCKET = "online-catalog-bucket"

def upload_base64_image(
    image_base64: str,
    product_id: int,
):
    if "," in image_base64:
        image_base64 = image_base64.split(",", 1)[1]

    image_bytes = base64.b64decode(image_base64)

    file_name = f"{uuid.uuid4()}.jpg"
    path = f"products/{product_id}/{file_name}"

    supabase.storage.from_(BUCKET).upload(
        path,
        image_bytes,
        {
            "content-type": "image/jpeg",
        },
    )

    return path
