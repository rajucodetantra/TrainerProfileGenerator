from io import BytesIO
from pathlib import Path

import fitz
from PIL import Image


def extract_pdf_text(pdf_bytes: bytes) -> str:
    """
    Extract readable text from all pages of a PDF.

    Args:
        pdf_bytes: PDF file content in bytes.

    Returns:
        Extracted text as a single string.
    """

    text_parts = []

    with fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    ) as document:

        for page in document:

            page_text = page.get_text("text")

            if page_text:
                text_parts.append(page_text)

    return "\n".join(text_parts)


def extract_candidate_photo(
    pdf_bytes: bytes,
    output_path: str
):
    """
    Try to extract the candidate's photo from the PDF.

    The function checks images mainly from the first
    two pages and prefers portrait/square images.

    Args:
        pdf_bytes: PDF content in bytes.
        output_path: Location where extracted image
                     should be saved.

    Returns:
        Image path if a suitable image is found.
        None if no suitable image is found.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    best_image = None
    best_score = 0

    with fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    ) as document:

        pages_to_check = min(
            2,
            len(document)
        )

        for page_number in range(
            pages_to_check
        ):

            page = document[
                page_number
            ]

            images = page.get_images(
                full=True
            )

            for image_info in images:

                xref = image_info[0]

                try:

                    extracted_image = (
                        document.extract_image(
                            xref
                        )
                    )

                    image_bytes = (
                        extracted_image[
                            "image"
                        ]
                    )

                    image = Image.open(
                        BytesIO(
                            image_bytes
                        )
                    )

                    width, height = (
                        image.size
                    )

                    # Ignore very small icons/logos
                    if (
                        width < 100
                        or height < 100
                    ):
                        continue

                    aspect_ratio = (
                        width / height
                    )

                    # Candidate photos normally
                    # have portrait or square shape
                    if not (
                        0.45
                        <= aspect_ratio
                        <= 1.45
                    ):
                        continue

                    image_rectangles = (
                        page.get_image_rects(
                            xref
                        )
                    )

                    display_area = 0

                    for rect in (
                        image_rectangles
                    ):

                        area = (
                            rect.width
                            * rect.height
                        )

                        if area > display_area:
                            display_area = area

                    # Ignore tiny displayed images
                    if display_area < 2500:
                        continue

                    score = display_area

                    # Prefer portrait images
                    if height >= width:
                        score *= 1.30

                    # Prefer images from page 1
                    if page_number == 0:
                        score *= 1.20

                    if score > best_score:

                        best_score = score

                        best_image = (
                            image.copy()
                        )

                except Exception:
                    continue

    if best_image is None:
        return None

    # Convert image to RGB
    if best_image.mode not in (
        "RGB",
        "RGBA"
    ):

        best_image = (
            best_image.convert(
                "RGB"
            )
        )

    # Remove transparency if present
    if best_image.mode == "RGBA":

        background = Image.new(
            "RGB",
            best_image.size,
            "white"
        )

        background.paste(
            best_image,
            mask=best_image.getchannel(
                "A"
            )
        )

        best_image = background

    best_image.save(
        output_path,
        format="PNG"
    )

    return str(output_path)