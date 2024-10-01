from paddleocr import PaddleOCR
from adb import ScreenCapture
from difflib import SequenceMatcher
import random
from colorama import init, Fore, Style
import os
from PIL import Image

init(autoreset=True)


class Script:
    # 获取当前文件所在目录的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 拼接相对路径
    # 构建检测模型的路径
    det_model_dir = os.path.join(current_dir, 'models', 'ch_PP-OCRv4_det_infer')
    # 构建识别模型的路径
    rec_model_dir = os.path.join(current_dir, 'models', 'ch_PP-OCRv4_rec_infer')
    # 构建分类模型的路径
    cls_model_dir = os.path.join(current_dir, 'models', 'ch_ppocr_mobile_v2.0_cls_infer')
    ocr = PaddleOCR(
        det_model_dir=det_model_dir,
        rec_model_dir=rec_model_dir,
        cls_model_dir=cls_model_dir,
        use_angle_cls=True, 
        lang="ch", 
        show_log=False
    )

    @staticmethod
    def OCR(x1, y1, x2, y2):
        img_path = ScreenCapture.screenshot(x1, y1, x2, y2)
        result = Script.ocr.ocr(img_path, cls=True)
        
        if not result or not result[0]:
            return "", [], 0
        
        texts, confidences = '', None
        first_line = result[0][0]
        positions, (text, confidences) = first_line
        
        texts += text.replace(" ", "")
        
        for line in result[0][1:]:
            _, (text, _) = line
            texts += text.replace(" ", "")

        position = (int(positions[0][0]) + x1, int(positions[0][1]) + y1)
        return texts, position, float(confidences)

    @staticmethod
    def OCREx(text, x1, y1, x2, y2):
        img_path = ScreenCapture.screenshot(x1, y1, x2, y2)
        result = Script.ocr.ocr(img_path, cls=True)
        similarity = 0
        similarity_first_part = 0
        similarity_second_part = 0
        first_part = ''
        second_part = ''
        
        if not result or not result[0]:
            return "", [], 0

        for line in result[0]:
            positions, (recognized_text, confidence) = line
            recognized_text = recognized_text.replace(" ", "")
            # 如果识别的文本中包含 "|" 分隔符，则进行分割；否则，设置默认值
            if "|" in recognized_text:
                parts = recognized_text.split("|")
                # 初始化一个列表来保存所有部分及其相似度
                similarities = []
                for part in parts:
                    # 计算当前部分与目标文本的相似度
                    similarity = SequenceMatcher(None, part, text).ratio() * 100
                    similarities.append(similarity)
            else:
                # 如果没有 "|"，则整个文本作为一个部分处理
                similarity = SequenceMatcher(None, recognized_text, text).ratio() * 100
                similarities = [similarity]

            # 取最大的相似度
            similarity = max(similarities)
            if similarity > 80:
                position = (int(int(positions[0][0])/3) + x1, int(int(positions[0][1])/3) + y1)
                print(
                    f"{Fore.RED}找到{Style.RESET_ALL}相似度为 {Style.BRIGHT}{Fore.BLUE}{similarity}% {Style.RESET_ALL}的类似答案。  "
                    f"{Fore.YELLOW}答案：{Fore.GREEN}{recognized_text}{Style.RESET_ALL}"
                )
                return recognized_text, position, float(confidence)
        
        return "", [], 0

    @staticmethod
    def random_offset(x, y, x_min=0, x_max=50, y_min=0, y_max=50):
        return x + random.randint(x_min, x_max), y + random.randint(y_min, y_max)



if __name__ == '__main__':
    while True:
        result = Script.OCR(439,393,521,422)
        print(result)
