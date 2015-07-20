import pyqrcode
import qrtools


def generate_qrcode(seed, dest):
    '''
        generate qrcode from seed, and save it to dest
    '''
    qr = pyqrcode.create(seed)
    qr.png(dest, scale=6)


def decode_qrcode(qrpng):
    '''
        decode qrpng to seed
    '''

    qr = qrtools.QR()
    qr.decode(qrpng)
    return qr.data

if __name__ == "__main__":
    dest = '/tmp/esse.png'
    generate_qrcode('hello esse', dest)
    seed = decode_qrcode(dest)
    print seed
