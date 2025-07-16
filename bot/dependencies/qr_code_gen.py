import tempfile

import qrcode


def generate_temp_qr(data: str) -> str:
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        img = qrcode.make(data)
        img.save(tmp)
        return tmp.name
