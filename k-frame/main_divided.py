import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor

from utils import write_average_fscore, calculate_tpfptnfn_kframe, calculate_fscore, default_excel, write_excel



def main(k, conf_thre, iou_thre):
    excel = default_excel(k, conf_thre, iou_thre)

    tp, fp, tn, fn = 0,0,0,0
    f_score = 0
    best_perf = [0, 0, f_score]  # [a, b, f_score]
    row = 2
    a_start = 1
    b_start = 1

    
    img_folder = r'C:\Users\李志卿\datasets\day'
    for space in os.listdir(img_folder): 
        for a in range(a_start, k+1):
            for b in range(b_start, k+1):
                img_num = len(os.listdir(os.path.join(img_folder, space, 'images')))

                tru_txt_folder = fr'C:\Users\李志卿\datasets\day\{space}\labels'
                pre_txt_folder = fr'D:\白杖实验全部资料\yolov8实验结果\day_yolov8_sol\{space}\labels'

                tpfptnfn = calculate_tpfptnfn_kframe(tru_txt_path=tru_txt_folder, pre_txt_path=pre_txt_folder, file_pre=space+'.mp4',
                file_num=img_num, unit_size=k, a=a/k, b=b/k, conf_thre=conf_thre, iou_thre=iou_thre)

                tp = tpfptnfn[0]
                fp = tpfptnfn[1]
                tn = tpfptnfn[2]
                fn = tpfptnfn[3]
                
                new_f_score = calculate_fscore(tp, tn, fp, fn)

                if new_f_score > f_score:
                    best_perf = [a, b, new_f_score]

        # 写结果到excel
        write_excel(excel, row, space, best_perf, img_num)
        row += 1
    
    # 计算加权平均f值 
    write_average_fscore(excel)


if __name__ == '__main__':
    k_list = (2,)
    iou_thre = 0.1

    # with ThreadPoolExecutor(max_workers=len(k_list)) as pool:
    #     for k in k_list:
    #         for conf_thre in np.arange(0.1, 0.2, 0.1):
    #             conf_thre = round(conf_thre, 1)
    #             print(f'start >>> k:{k}，c:{conf_thre}')
    #             pool.submit(main, *(k, conf_thre, iou_thre))

    main(2, 0.1, 0.1)

    