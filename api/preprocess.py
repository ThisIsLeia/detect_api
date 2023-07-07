import torchvision


def image_to_tensor(image):
    """ 將圖片資料轉為張量型態的數值資料 """
    image_tensor = torchvision.transforms.functional.to_tensor(image)
    return image_tensor