import base64
import uuid

from app.supabase import supabase

BUCKET = "online-catalog-bucket"


def upload_base64_image(
    image_base64: str,
    product_id: int,
) -> str:
    content_type = "image/jpeg"
    ext = "jpg"

    if image_base64.startswith("data:"):
        header, image_base64 = image_base64.split(",", 1)
        mime = header.split(";")[0].replace("data:", "").strip()

        if mime:
            content_type = mime
            if mime == "image/svg+xml":
                ext = "svg"
            elif mime == "image/jpeg":
                ext = "jpg"
            else:
                ext = mime.split("/")[-1].split("+")[0]

    elif "," in image_base64:
        image_base64 = image_base64.split(",", 1)[1]

    missing_padding = len(image_base64) % 4
    if missing_padding != 0:
        image_base64 += "=" * (4 - missing_padding)

    image_bytes = base64.b64decode(image_base64)

    file_name = f"{uuid.uuid4()}.{ext}"
    path = f"products/{product_id}/{file_name}"

    supabase.storage.from_(BUCKET).upload(
        path=path,
        file=image_bytes,
        file_options={"content-type": content_type},
    )

    return path


def delete_image(path_or_url: str) -> None:
    if not path_or_url:
        return

    marker = f"/storage/v1/object/public/{BUCKET}/"


    if marker in path_or_url:
        path = path_or_url.split(marker, 1)[1]

    elif path_or_url.startswith("products/"):
        path = path_or_url
    else:
        return

    path = path.split("?")[0]

    supabase.storage.from_(BUCKET).remove([path])