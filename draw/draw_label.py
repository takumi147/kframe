import cv2
import os

def draw(img, label):
    """
    :para img, the path of img,
          label, the path of sol label
    """

    global out_dir
    global img_folder

    # 默认config
    image = cv2.imread(os.path.join(img_folder, img))
    xywhs = []  
    font = cv2.FONT_HERSHEY_SIMPLEX

    # 定义长方形的位置和尺寸
    width, height = image.shape[1], image.shape[0]

    with open(label, 'r') as t:
        xywhs = t.read().split('\n')
        boxes = [ i[2:] for i in xywhs if i]  # [[xywhs],]
    for box in boxes:
        xywhs = box.split(' ')
        xywhs = xywhs[1:]
        xywhs = [float(i) for i in xywhs]
        text = f'whitecane {round(xywhs[-1], 2)}'

        x1,y1 = int((xywhs[0]-xywhs[2]/2)*width), int((xywhs[1]-xywhs[3]/2)*height)
        x2,y2 = int((xywhs[0]+xywhs[2]/2)*width), int((xywhs[1]+xywhs[3]/2)*height)
        # 绘制长方形
        cv2.rectangle(image, (x1, y1), (x2,y2),(0, 0, 255), 5)

        # 添加文本
        cv2.rectangle(image, (x1, y1), (x1+200,y1-20),(0, 0, 255), -1)
        z1, z2 = int((xywhs[0]-xywhs[2]/2)*width), int((xywhs[1]-xywhs[3]/2)*height)
        cv2.putText(image, text, (z1, z2), font, 0.9, (255, 255, 255), 2)
    
    
    out_img = os.path.join(out_dir, os.path.basename(img))

    assert cv2.imwrite(out_img, image) , '没有sol_img文件夹！程序结束！'
    print(f'{out_img}已保存，检测出{len(boxes)}目标！')

    # 显示图像
    # cv2.imshow('Image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":  
    # label_dir = r'D:\白杖实验全部资料\k-frame脚本\draw\r_p1'
    # img_path = r'D:\白杖实验全部资料\k-frame脚本\draw\pic'
    # out_dir = r'D:\白杖实验全部资料\k-frame脚本\draw\r_pic'

    # for img in os.listdir(img_path):
    #     if not os.path.isfile((os.path.join(img_path, img))):
    #         continue
    #     label_name = img[:-4] + '.txt'
    #     label_path = os.path.join(label_dir, label_name)
    #     if not os.path.exists(label_path):
    #         print(label_path,'不存在！')
    #         continue
    #     draw(os.path.join(img_path, img), label_path)

    img_root_path = r'C:\Users\李志卿\datasets\day'

    for space in os.listdir(img_root_path):
        img_folder = os.path.join(img_root_path, space, 'images')
        out_dir = f'D:\白杖实验全部资料\yolov8实验结果\day_yolov8_sol\{space}\images'
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        for img in os.listdir(img_folder):
            label_name = img[:-4] + '.txt'
            label_path = fr'D:\白杖实验全部资料\yolov8实验结果\day_yolov8_sol\{space}\labels\{label_name}'
            if not os.path.exists(label_path):
                print(img,'没有检测出白杖')
            else:
                draw(img, label_path)