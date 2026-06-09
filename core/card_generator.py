from PIL import (
    Image,
    ImageDraw,
    ImageFilter
)

import requests
import os

from io import BytesIO


CARD_WIDTH = 1280
CARD_HEIGHT = 720


def rounded_image(image, radius=40):

    mask = Image.new(
        "L",
        image.size,
        0
    )

    draw = ImageDraw.Draw(mask)

    draw.rounded_rectangle(
        (
            0,
            0,
            image.size[0],
            image.size[1]
        ),
        radius=radius,
        fill=255
    )

    image.putalpha(mask)

    return image


def download_thumbnail(url):

    response = requests.get(
        url,
        timeout=15
    )

    image = Image.open(
        BytesIO(response.content)
    )

    return image.convert("RGB")


def generate_card(
    song,
    requested_by="Unknown",
    chat_id=0
):

    os.makedirs(
        "cache/cards",
        exist_ok=True
    )

    thumb = download_thumbnail(
        song["thumbnail"]
    )

    # =========================
    # Blurred Background
    # =========================

    background = thumb.resize(
        (
            CARD_WIDTH,
            CARD_HEIGHT
        )
    )

    background = background.filter(
        ImageFilter.GaussianBlur(30)
    )

    background = background.convert(
        "RGBA"
    )

    # =========================
    # Center Thumbnail
    # =========================

    cover = thumb.resize(
        (
            650,
            450
        )
    )

    cover = cover.convert(
        "RGBA"
    )

    cover = rounded_image(
        cover,
        35
    )

    cover_x = (
        CARD_WIDTH - 650
    ) // 2

    cover_y = (
        CARD_HEIGHT - 450
    ) // 2

    background.alpha_composite(
        cover,
        (
            cover_x,
            cover_y
        )
    )

    # =========================
    # Save
    # =========================

    output = (
        f"cache/cards/{chat_id}.png"
    )

    background.convert(
        "RGB"
    ).save(
        output,
        quality=95
    )

    return output