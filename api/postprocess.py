import random
import cv2


def make_color(labels):
    """隨機決定框線顏色"""
    colors = [[random.randint(0,255) for _ in range(3)] for _ in labels]
    color = random.choice(colors)
    return color


def make_line(result_image):
    """製作框線"""
    line = round(0.002 * max(result_image.shape[0:2])) + 1
    return line


def draw_lines(c1, c2, result_image, line, color):
    """在圖片添加四角形的框線"""
    cv2.rectangle(result_image, c1, c2, color, thickness=line)
    return cv2


def draw_texts(result_image, line, c1, color, display_txt):
    """在圖片中添加已經辨識的標籤"""
    font = max(line - 1, 1)
    t_size = cv2.getTextSize(
        display_txt, 0, fontScale=line / 3, thickness=font
    )[0]
    c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
    cv2.rectangle(result_image, c1, c2, color, -1)
    cv2.putText(
        result_image,
        display_txt,
        (c1[0], c1[1] - 2),
        0,
        line / 3,
        [225, 255, 255],
        thickness=font,
        lineType=cv2.LINE_AA
    )
    return cv2


def exec_detect(target_image_path):
    # 加載標籤
    labels = current_app.config['LABELS']
    # 加載圖片
    image = Image.open(target_image_path)
    # 將圖片資料轉成張量(tensor)型態的數值資料
    image_tensor = torchvision.transforms.functional.to_tensor(image)

    # 加載已學習模型
    model = torch.load(Path(current_app.root_path, 'detector', 'model.pt'))
    # 切換模型的推論模式
    model = model.eval()
    # 執行推論
    output = model([image_tensor])[0]

    tags = []
    result_image = np.array(image.copy())

    # 在圖片添加模型已識別的物體處理
    for box, label, score in zip(
        output['boxes'], output['labels'], output['scores']
    ):
        if score >0.5 and labels[label] not in tags:
                # 決定框線的顏色
            color = make_color(labels)
            # 製作匡線
            line = make_line(result_image)
            # 偵測圖片和文字標籤的框線位置資訊
            c1 = (int(box[0]), int(box[1]))
            c2 = (int(box[2]), int(box[3]))
            # 在圖片添加匡線
            cv2 = draw_lines(c1, c2, result_image, line, color)
            # 在圖片添加文字標籤
            cv2 = draw_texts(result_image, line, c1, cv2, color, labels, label)
            tags.append(labels[label])
    # 產生已識別的圖像檔案名稱
    detected_image_file_name = str(uuid.uuid4()) + '.jpg'
    # 取得圖片複製目的地的路徑
    detected_image_file_path = str(
        Path(current_app.config['UPLOAD_FOLDER'],
             detected_image_file_name)
    )
    # 將加工後的圖片檔案複製至儲存目的地
    cv2.imwrite(
        detected_image_file_path, cv2.cvtColor(
            result_image, cv2.COLOR_RGB2BGR
        )
    )

    return tags, detected_image_file_name