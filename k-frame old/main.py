import numpy as np
from concurrent.futures import ThreadPoolExecutor

from utils import getvideo_nameandflamenum, calculate_tpfptnfn_kframe, calculate_fscore, calculate_tpfptnfn_k1, write_excel



def main(conf_thre, iou_thre, k):
    tp, fp, tn, fn = 0,0,0,0
    video_inf = {}
    res = []

    # 计算使用Kframe的评价结果
    a_start = 1
    b_start = 1
    # for a in range(a_start, k+1):
    #     for b in range(b_start, k+1):
    for a in range(a_start, k+1):
        for b in range(b_start, k+1):
            # there are 23 experimental places.
            for i in range(1,2):        
                tru_img_path = fr'C:\Users\李志卿\datasets\place{i}\images'
                tru_txt_path = fr'C:\Users\李志卿\datasets\place{i}\labels'
                pre_txt_path = fr'D:\白杖实验全部资料\yolov8实验结果\day_row\exp{i}\labels'
                video_inf = getvideo_nameandflamenum(tru_img_path)
                for video, flamenum in video_inf.items():
                    tpfptnfn = calculate_tpfptnfn_kframe(tru_txt_path=tru_txt_path, pre_txt_path=pre_txt_path, file_pre=video,
                    file_num=flamenum, unit_size=k, a=a/k, b=b/k, conf_thre=conf_thre, iou_thre=iou_thre)
                    tp += tpfptnfn[0]
                    fp += tpfptnfn[1]
                    tn += tpfptnfn[2]
                    fn += tpfptnfn[3]
            fscore = calculate_fscore(tp, tn, fp, fn)
            res.append([k,a,b,fscore])
            print(fr'k:{k},a:{a}/{k},b:{b}/{k}, over')
    # 写结果到excel
    write_excel(k, res, f'conf_thre{conf_thre}')



def maink1(conf_thre:float, iou_thre:float):
    '''
    calculate the f1-score and write result into a excel
    para: conf_thre->confidence threshold
          iou_thre->iou threshold
    return: NULL
    '''
    # 需要和常见的f1score评价方法得出的结果比较，以显示kframe想法的优越性。
    tp, fp, tn, fn = 0,0,0,0
    video_inf = {}
    res = []

    for i in range(1,2):        
        tru_img_path = fr'D:\白杖实验全部资料\k-frame脚本\draw\pic'
        tru_txt_path = fr'D:\白杖实验全部资料\k-frame脚本\k-frame\real_test'
        pre_txt_path = fr'D:\白杖实验全部资料\k-frame脚本\sol\r_p1'
        video_inf = getvideo_nameandflamenum(tru_img_path)
        for video, flamenum in video_inf.items():
            tpfptnfn = calculate_tpfptnfn_k1(tru_txt_path=tru_txt_path, pre_txt_path=pre_txt_path, file_pre=video,
            file_num=flamenum, conf_thre=conf_thre, iou_thre=iou_thre)
            tp += tpfptnfn[0]
            fp += tpfptnfn[1]
            tn += tpfptnfn[2]
            fn += tpfptnfn[3]
    fscore = calculate_fscore(tp, tn, fp, fn)
    res.append([1,1,1,fscore])
    print('k=1, over')
    # 写结果到excel
    write_excel(k=1, results=res, file_pre=f'k=1_conf_thre{conf_thre}')


if __name__ == '__main__':
    k_list = (15,)
    iou_thre = 0.1
    # for k in k_list:
    #     for conf_thre in np.arange(0.1, 0.2, 0.1):
    #         conf_thre = round(conf_thre, 1)
    #         print(f'start >>> k:{k}，c:{conf_thre}')
    #         main(conf_thre, k, size, seta)

    # with ThreadPoolExecutor(max_workers=len(k_list)) as pool:
    #     for k in k_list:
    #         for conf_thre in np.arange(0.1, 0.2, 0.1):
    #             conf_thre = round(conf_thre, 1)
    #             print(f'start >>> k:{k}，c:{conf_thre}')
    #             pool.submit(main, *(conf_thre, iou_thre, k))

    
    maink1(0.1, 0.1)