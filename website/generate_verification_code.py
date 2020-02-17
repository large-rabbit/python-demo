"""
利用Opencv随机生成验证码图片

Version: 1.0
Author: large-rabbit
"""
import cv2
import numpy as np
import string

img_hight, img_width = 40, 40


def generate_char_code(code_len=4):
    """
    生成指定长度的字符验证码，包含数字与字母大小写

    :param code_len: 验证码长度，默认4位
    :return: 包含验证码的字符串
    """
    all_code = string.digits + string.ascii_letters
    all_code_len = len(all_code)
    code = ''
    for _ in range(code_len):
        index = np.random.randint(0, all_code_len)
        code += all_code[index]
    return code


def generate_img_code(text_code):
    """
    将生成的文字验证码通过变形，加干扰线得到图片验证码

    :param text_code: 需要转换的文字验证码
    :return: 生成的图形验证码
    """
    text_code_len = len(text_code)
    img_code = np.empty((img_hight, img_width*text_code_len, 3), np.uint8)
    for index, elem in enumerate(text_code):
        img_code[:, index*img_width:(index+1)*img_width] = change_shape(elem)
    img_code = change_background(img_code)
    img_code = add_line(img_code, text_code_len)
    return img_code


def change_shape(ch):
    """
    将单个字符进行变形与旋转，还未实现变形功能
    
    :param ch: 需要变形的字符
    :return: 变形的字符
    """
    scale_h, scale_w = int(img_hight/8), int(img_width/8)
    # =====================================================
    # color 的类型必须是tuple，从numpy直接转成tuple会有问题
    # =====================================================
    img_color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
    img_single = np.zeros((img_hight, img_width, 3), np.uint8)  # 生成黑背景
    img_single = cv2.putText(img_single, ch, (scale_w, 7*scale_h),
                             cv2.FONT_HERSHEY_SIMPLEX, 1.5, img_color, 2, cv2.LINE_AA)  # 写字符到图片
    # 对图片使用透视变换进行形变
    before_change_pos = np.float32([[0, 0], [0, img_hight], [img_width, img_hight], [img_width, 0]])
    after_change_pos = np.float32([[0, 0],
                                   np.random.randint([0, img_hight-2*scale_h], [2*scale_w, img_hight], 2),
                                   np.random.randint([img_width-2*scale_w, img_hight-2*scale_h], [img_width, img_hight], 2),
                                   [img_width, 0]])
    matrix = cv2.getPerspectiveTransform(before_change_pos, after_change_pos)   # 计算变化矩阵
    img_single = cv2.warpPerspective(img_single, matrix, (img_hight, img_width))  # 进行透视变换
    # 对图片使用仿射变换进行旋转
    matrix = cv2.getRotationMatrix2D((img_hight / 2, img_width / 2), np.random.randint(-45, 45), 1)  # 计算旋转矩阵
    img_single = cv2.warpAffine(img_single, matrix, (img_hight, img_width))  # 进行仿射变换
    return img_single


def add_line(img_code, text_code_len):
    """
    在验证码上加入干扰线

    :param img_code: 未加干扰线的图片验证码
    :param text_code_len: 验证码字符数
    :return: 加上干扰线的图片验证码
    """
    line_num = 10
    for _ in range(line_num):
        random_pos1 = (np.random.randint(0, img_width*text_code_len), np.random.randint(0, img_hight))
        random_pos2 = (np.random.randint(0, img_width*text_code_len), np.random.randint(0, img_hight))
        line_color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        cv2.line(img_code, random_pos1, random_pos2, line_color, np.random.randint(1, 2))
    return img_code


def change_background(img_code):
    """
    将图片背景从黑色变为加噪点的特定背景

    :param img_code: 需要改变背景的图片
    :return: 加噪点后的图片
    """
    img_code_shape = img_code.shape
    for row in range(img_code_shape[0]):
        for col in range(img_code_shape[1]):
            if all(img_code[row, col] == [0, 0, 0]):
                img_code[row, col] = np.random.randint(100, 200, 3, np.uint8)
    return img_code


def main():
    code_list = np.zeros((1000, 1), np.string_)
    for index in range(1000):
        text_code = generate_char_code(5)
        if np.sum(code_list == text_code) == 0:
            img_code = generate_img_code(text_code)
            code_list[index, 0] = text_code
            cv2.imencode('.png', img_code)[1].tofile('C:\\Users\\28602\\Desktop\\验证码\\{0}.png'.format(text_code))
            print('写第{0}张'.format(index))
        else:
            index -= 1

    # cv2.imshow('img_code', img_code)
    # cv2.waitKey(0)


if __name__ == '__main__':
    main()
