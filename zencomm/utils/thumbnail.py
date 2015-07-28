import zencomm.log as logging
from PIL import Image
import StringIO

THUMBNAIL_SIZE = (2000, 2000)


def create_thumbnail(file_content, file_type, file_size=THUMBNAIL_SIZE):
    ''' create thumbnail for file_content
        @param file_size: (file_width, file_height)
        @return: thumbnail or None
    '''
    im = None
    input_buf = None
    ouput_buf = None

    if file_content is None or len(file_content) == 0:
        return None
    try:
        input_buf = StringIO.StringIO(file_content)
        im = Image.open(input_buf, 'r')
        im.thumbnail(file_size, Image.ANTIALIAS)
        output_buf = StringIO.StringIO()
        im.save(output_buf, file_type)
        thmnail = output_buf.getvalue()
        return thmnail
    except Exception, e:
        logging.warn('failed to create thumnail with exception : [%s]' % e)
        logging.exception(e)
        return None
    finally:
        if im:
            im.close()
        if input_buf:
            input_buf.close()
        if ouput_buf:
            ouput_buf.close()

if __name__ == "__main__":

    import sys
    import os
    if len(sys.argv) == 1:
        print "please input the file name"
        sys.exit(1)
    img_src = sys.argv[1]
    img_path = os.path.abspath(img_src)
    file_name = os.path.basename(img_path)
    file_type = 'jpeg'
    thumb_nail_file = open('/tmp/test_thumbnail.jpg', 'w')
    with open(img_src, 'r') as content:
        thumbnail = create_thumbnail(content.read(), file_type)
        thumb_nail_file.write(thumbnail)
        thumb_nail_file.close()

    print "please check thumnail file at /tmp/test_thumbnail.jpg"
