from pathlib import Path
import PIL

basedir = Path(__file__).parent.parent


def load_image(request, reshaped_size=(256, 256)):
    """ 加載圖片 """
    filename = request.json['filename']
    dir_image = str(basedir/'data'/'original'/filename)
    # 建立圖片資料物件
    image_obj = PIL.Image.open(dir_image).convert('RGB')
    # 修改圖片大小尺寸
    image = image_obj.resize(reshaped_size)
    return image, filename