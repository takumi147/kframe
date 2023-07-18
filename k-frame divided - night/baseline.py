"""
不使用kframe，一帧一帧逐个计算检测结果。
"""

import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor

from utils import calculate_tpfptnfn_kframe, calculate_fscore, default_excel, write_excel_by_row



def main(k, conf_thre, iou_thre):
    img_folder = r'C:\Users\李志卿\datasets\day'
    tp, fp, tn, fn = 0,0,0,0
    res = []

    excel = default_excel(img_folder.split('\\')[-1], k, conf_thre, iou_thre)

    for space in os.listdir(img_folder): 
        img_num = len(os.listdir(os.path.join(img_folder, space, 'images')))

        tru_txt_folder = fr'C:\Users\李志卿\datasets\day\{space}\labels'
        pre_txt_folder = fr'D:\白杖实验全部资料\yolov8实验结果\day_yolov8_sol\{space}\labels'

        tpfptnfn = calculate_tpfptnfn_kframe(tru_txt_path=tru_txt_folder, pre_txt_path=pre_txt_folder, file_pre=space+'.mp4',
        file_num=img_num, unit_size=k, a=1, b=1, conf_thre=conf_thre, iou_thre=iou_thre)

        tp += tpfptnfn[0]
        fp += tpfptnfn[1]
        tn += tpfptnfn[2]
        fn += tpfptnfn[3]

    f_score = round(calculate_fscore(tp, tn, fp, fn), 3)
    res.append([1, 1, 1, f_score])  # [k, a, b, f_score]

    # 写结果到excel
    write_excel_by_row(excel, res)


if __name__ == '__main__':
    k = 1
    conf_thre = 0.1
    iou_thre = 0.1
    main(k, conf_thre, iou_thre)

    