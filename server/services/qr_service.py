import qrcode, datetime, requests

def create_qr_code(data):
    generator = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_M,
        box_size = 10,
        border=4,
    )

    generator.add_data(data)
    generator.make()

    return generator.make_image()

    
