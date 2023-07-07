"""
所有的标注都是双语，第一行中文，第二行英文，内容一样。希望能帮上你^v^。
All the labels are bilingual, the first line is Chinese, the second line is English, the content is the same. Hope it helps you ^v^.

运用在yolo检测完得到的label.txt上面，过滤背景中静物之后，得到只剩下运动物体的label.txt
Use the label.txt obtained after yolo detection, after filtering the still life in the background, get the label.txt with only moving objects

sol的全名是static object list，之后可能有别的叫法，但我认为这个更好理解。
The full name of sol is static object list, and there may be other names later, but I think this is better understood.
"""

import os

def main(row_label_path, object_label_path, size=15, seta=0.13, scale=1.2, conf_thre=0.1):
    """
    过滤yolo检测结果中的静物。
    Filter static objects in yolo detection results.

    :param  row_label_path: labels folder.
            object_label_path: folder where you want to save sol labels.
            size: sol update every 'size' flames.
            scale: the size of static objects will be enlarged 'scale' times before recorded.
            conf_thre: confidence thread to abandon unreliable detected objects.
    :return none
    """

    # sol parameters.
    sols = []
    count = 0
    tmpsols = []

    # 获取所有label.txt的最后一个txt的序号。比如：place1_whitecane01.mp4_379.txt，我就得到379这个数字，不能直接用文件夹内txt的数量，因为可能中间几帧没有检测结果导致数量少于379。sol需要考虑所有帧。
    # sol的目标是处理所有label.txt，所以这里不使用实际视频的帧数。
    # Get the serial number of the last label.txt. example：place1_whitecane01.mp4_379.txt，we get 379. We cannot use the number of txt in the folder, because there may be no detection results in the middle frames and the number is less than 379. sol needs to consider all frames.
    # In sol, we only need to deal with label.txt, so we dont use flame number of whole video.
    flame_nums = [0]
    if os.listdir(row_label_path):
        # # day
        # flame_nums = [i.split('_')[2].split('.')[0] for i in os.listdir(row_label_path)]
        # night 
        flame_nums = [i.split('_')[1].split('.')[0] for i in os.listdir(row_label_path)]  
    final_flame_num = int(max(flame_nums))
    if final_flame_num == 0:
        print(f'{row_label_path}里没有label！程序退出')
        return

    video_name = os.listdir(row_label_path)[0].split('.')[0]

    # 遍历所有label。注意，如果yolo检测当前帧没有目标，就不会生成当前帧的label.txt。
    # 以前认为会生成一个空的label.txt
    # for all labels.txt. Note that if yolo detects that there is no target in the current frame, the label.txt of the current frame will not be generated.
    # It was previously thought that an empty label.txt would be generated
    for i in range(0, final_flame_num):
        count += 1

        # 每size帧更新一次sols。sols里就是静物的坐标。通过参考sols进行过滤。
        # Update sols every size frame. In sols are the coordinates of the static objects. Filter labels by sols.
        if count % size == 0:
            count = 0
            sols, tmpsols = refreshsols(sols, tmpsols, size, seta)

        # 准备记录sol过滤之后的label。
        # labels after sol filters.
        new_labels = ''
        pre_boxes = []
        
        if 0 <= i < 10:
            label_txt = video_name + '.mp4_00' + str(i) + '.txt'
        elif 10 <= i < 100:
            label_txt = video_name + '.mp4_0' + str(i) + '.txt'
        else:
            label_txt = video_name + '.mp4_' + str(i) + '.txt'

        # 如果当前帧检测出目标，则使用sol过滤。
        # If an object is detected in the current frame, use sol.
        if os.path.exists(os.path.join(row_label_path, label_txt)):
            pre_boxes = get_pre_boxes(os.path.join(row_label_path, label_txt))
            for box in pre_boxes:
                c = box[-1]
                xywh = box[1:-1]
                if c >= conf_thre and not in_sols(sols, xywh):
                    box = [str(i) for i in box]
                    new_labels += ' '.join(box) 
                    new_labels += '\n'

        # 写结果。过滤完没有了就记录一个空的label。
        # save labels after sols filter.
        with open(os.path.join(object_label_path, label_txt), 'w+') as t:
            t.write(new_labels)
        print(f'{label_txt} saved')

        # 更新tmp sol。
        # refresh temporary sol.
        for box in pre_boxes:
            c = box[-1]
            xywh = box[1:-1]
            if c >= conf_thre:
                for tmpsol in tmpsols:
                    if in_tmpsol(tmpsol, xywh):
                        tmpsol[-1] += 1
                        break
                else:
                    tmpsols += [enlarge_box(xywh, scale) + [1]]

    return True


def get_pre_boxes(file):
    """
    extract box information from txt
    :file: file path
    :param file: "xxx.txt"
    :return [[cxywhc],]
    """
    # read txt and split different boxes
    txt = open(file, 'r').read().split('\n')
    
    # create the boxes list
    boxes = []

    # add boxes information into list
    # pre_txt: [n, x, y, w, h, c] to [bottom line, left line, top line, right line, c]
    # tru_txt: [n, x, y, w, h] to [bottom line, left line, top line, right line]
    for box in txt:
        if box:
            box = box.split(' ')
            box = [float(i) for i in box]
            box[-1] = round(box[-1], 2)
            boxes.append(box)

    return boxes


def refreshsols(sols, tmpsols, size, seta):
    """
    replace sols with tmpsols.
    para:
    sols: [[xywh],]
    tmpsols: [[xywhc],], c is count.
    seta should be between 0~1
    """
    sols = [box[:-1] for box in tmpsols if box[-1] >= int(size*seta)]
    tmpsols = [box + [1] for box in sols]
    return sols, tmpsols


def enlarge_box(xywh, scale=1.2):
    # elarge box， xywh is [x,y,w,h]
    return [xywh[0], xywh[1], xywh[2]*scale, xywh[3]*scale]


def in_tmpsol(tmpsol, xywh):
    # if xywh in temporary sol, return True.
    # tmpsol: [xywhc], c is count, not conf_threshold.
    if not tmpsol:
        return False
    xyxy = my_xywh2xyxy(xywh)
    tmpsol = my_xywh2xyxy(tmpsol[:-1])
    if tmpsol[0] <= xyxy[0] and tmpsol[1] >= xyxy[1]\
        and tmpsol[2] >= xyxy[2] and tmpsol[3] <= xyxy[3]:
        return True
    return False


def my_xywh2xyxy(xywh):
    # list xywh to xyxy.
    # :return [xyxy], left line, top line, right line, bottom line.
    xyxy = [0] * 4
    xyxy[0] = xywh[0] - xywh[2]/2
    xyxy[1] = xywh[1] + xywh[3]/2
    xyxy[2] = xywh[0] + xywh[2]/2
    xyxy[3] = xywh[1] - xywh[3]/2
    return xyxy


def in_sols(sols, xywh):
    # if xywh in sol, return True.
    # sols: [[xywh],].
    if not sols:
        return False
    xyxy = my_xywh2xyxy(xywh)
    sols = [my_xywh2xyxy(i) for i in sols]
    for sol in sols:
        if sol[0] <= xyxy[0] and sol[1] >= xyxy[1]\
            and sol[2] >= xyxy[2] and sol[3] <= xyxy[3]:
            return True
    return False



if __name__ == '__main__':
    row_label_folder = r'D:\白杖实验全部资料\yolov8实验结果_new\night_yolov8_row'
    object_label_folder = r'D:\白杖实验全部资料\yolov8实验结果_new\night_yolov8_sol'
    for folder in os.listdir(row_label_folder): 
        object_label_path = os.path.join(object_label_folder, folder, 'labels')
        try:
            os.mkdir(os.path.join(object_label_folder, folder))
            os.mkdir(os.path.join(object_label_folder, folder, 'labels'))
            print(f'{object_label_path}已生成')
        except:
            print(f'{object_label_path}已存在')
        main(os.path.join(row_label_folder, folder,'labels'), object_label_path)
        print(f'{object_label_path}过滤完成')
        print('-------------------------------------')

    # main('D:\白杖实验全部资料\yolov8实验结果_new\day_yolov8_row\place1_whitecane01\labels', 
    #      'D:\白杖实验全部资料\yolov8实验结果_new\day_yolov8_sol\place1_whitecane01\labels')