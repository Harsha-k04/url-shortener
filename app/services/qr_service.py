import os
import qrcode


def generate_qr_code(short_url: str, short_code: str):

    folder = "app/static/qr_codes"

    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(
        folder,
        f"{short_code}.png"
    )

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(short_url)
    qr.make(fit=True)

    image = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    image.save(file_path)

    return file_path