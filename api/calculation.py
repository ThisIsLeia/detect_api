from pathlib import Path
import numpy as np
import cv2
import torch
from flask import current_app, jsonify
from detect_api.api.preparation import load_image
from detect_api.api.preprocess import image_to_tensor
from detect_api.api.postprocess import make_color, make_line, draw_lines, draw_texts

basedir = Path(__file__).parent.parent


def detection(request):
    dict_results = {}
    # 加載標籤
    labels = current_app.config['LABELS']
    # 加載圖片
    image, filename = load_image(request)
    # 將圖片資料轉為張量型態的數值資料
    image_tensor = image_to_tensor(image)

    # 加載已學習模型
    try:
        model = torch.load('model.pt')
    except FileNotFoundError:
        return jsonify('The model is noe found'), 404
    
    # 切換模型的推論模式
    model = model.eval()
    # 執行推論
    output = model([image_tensor])[0]

    result_image = np.array(image.copy())

    # 在已經學習模型識別的物體圖片，增加匡線和標籤
    for box, label, score in zip(output['boxes'], 
                                 output['labels'], 
                                 output['scores']):
        # 篩選信賴分數 > 0.6 且不重複的標籤
        if score > 0.6 and labels[label] not in dict_results:
            # 決定匡線顏色
            color = make_color(labels)
            # 產生匡線
            line = make_line(result_image)
            # 識別圖片與文字標籤的匡線位置資訊
            c1 = int(box[0]), int(box[1])
            c2 = int(box[2]), int(box[3])
            # 圖片增加匡線
            draw_lines(c1, c2, result_image, line, color)
            # 圖片增加文字標籤
            draw_texts(result_image, line, c1, color, labels[label])
            # 建立已識別標籤與信賴分數字典
            dict_results[labels[label]] = round(100 * score.item())

    # 建立圖片所在位置的目錄全路徑
    dir_image = str(basedir/'data'/'output'/filename)
    # 儲存識別後的圖片檔案
    cv2.imwrite(dir_image, cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))

    return jsonify(dict_results), 201
