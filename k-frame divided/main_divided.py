import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor

from utils import calculate_tpfptnfn_kframe, calculate_fscore, default_excel, write_excel_by_row



def main(k, conf_thre, iou_thre):
    img_folder = r'C:\Users\李志卿\datasets\day'
    tp, fp, tn, fn = 0,0,0,0
    res = []
    a_start = 1
    b_start = 1

    excel = default_excel(img_folder.split('\\')[-1], k, conf_thre, iou_thre)


    for a in range(a_start, k+1):
        for b in range(b_start, k+1):
            for space in os.listdir(img_folder): 
                img_num = len(os.listdir(os.path.join(img_folder, space, 'images')))

                tru_txt_folder = fr'C:\Users\李志卿\datasets\day\{space}\labels'
                pre_txt_folder = fr'D:\白杖实验全部资料\yolov8实验结果\day_yolov8_sol\{space}\labels'

                tpfptnfn = calculate_tpfptnfn_kframe(tru_txt_path=tru_txt_folder, pre_txt_path=pre_txt_folder, file_pre=space+'.mp4',
                file_num=img_num, unit_size=k, a=a/k, b=b/k, conf_thre=conf_thre, iou_thre=iou_thre)

                tp += tpfptnfn[0]
                fp += tpfptnfn[1]
                tn += tpfptnfn[2]
                fn += tpfptnfn[3]

            f_score = round(calculate_fscore(tp, tn, fp, fn), 3)
            res.append([k, a, b, f_score])

            # 写结果到excel
            write_excel_by_row(excel, res)

            # 重置基本参数
            tp, fp, tn, fn = 0,0,0,0
            res = []

        print(f'k为{k}, a为{a}的一行数据已经写入。')

if __name__ == '__main__':
    k_list = (60, 90, 120, 150)
    iou_thre = 0.1

    with ThreadPoolExecutor(max_workers=len(k_list)) as pool:
        for k in k_list:
            for conf_thre in np.arange(0.1, 0.2, 0.1):
                conf_thre = round(conf_thre, 1)
                print(f'start >>> k:{k}，c:{conf_thre}')
                pool.submit(main, *(k, conf_thre, iou_thre))

    # main(2, 0.1, 0.1)

    