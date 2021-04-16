import requests
import time
from PIL import Image
from aip import AipOcr
from pymouse import PyMouse
import win32gui, win32ui, win32con, win32api
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *

m = PyMouse()


def window_capture():
    hwnd = win32gui.FindWindow(None, '雷电模拟器')
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    img.save('D:\image.png')


def get_word_by_img():
    # 文字识别
    APP_ID = '23125232'
    API_KEY = 'Vh5i2Ft0RuOARzr6lMEpPGZ3'
    SECRET_KEY = 'Kk2GzHuZzdeuvAIfkAPF5Qg31Hw5eZvs'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    i = open('new_img_fb.png', 'rb')
    img = i.read()
    img_res = client.basicGeneral(img)
    print(img_res)
    return img_res


def baidu(question, answers):
    # 进行百度
    url = 'https://www.baidu.com/s'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57"
    }
    data = {
        'wd': question
    }
    res = requests.get(url=url, params=data, headers=headers)
    res.encoding = 'utf-8'
    html = res.text
    for i in range(len(answers)):
        answers[i] = (html.count(answers[i]), answers[i], i)
    answers.sort(reverse=True)

    if (len(answers) > 0):
        if (answers[0][2] == 0 and answers[0][0] > 0):
            m.click(831, 657)
        elif (answers[0][2] == 1):
            m.click(905, 747)
        elif (answers[0][2] == 2):
            m.click(923, 846)
        elif (answers[0][2] == 3):
            m.click(936, 945)

    m.click(684, 882)
    return answers


def run():
    while True:
        time.sleep(5)
        window_capture()
        img = Image.open('D:\image.png')
        title_img = img.crop((760, 430, 1160, 510))
        answers_img = img.crop((760, 600, 1160, 1000))
        new_img = Image.new('RGBA', (400, 480))
        new_img.paste(title_img, (0, 0, 400, 80))
        new_img.paste(answers_img, (0, 80, 400, 480))
        new_img.save('new_img_fb.png')

        info = get_word_by_img()
        answers = [x['words'] for x in info['words_result'][1:]]
        if (len(answers) > 0):
            list1 = answers[0].split(',')
            answers[0] = list1[0]
        if (len(answers) > 1):
            list2 = answers[1].split(',')
            answers[1] = list2[0]
        if (len(answers) > 2):
            list3 = answers[2].split(',')
            answers[2] = list3[0]
        if (len(answers) > 3):
            list4 = answers[3].split(',')
            answers[3] = list4[0]
        print(answers)
        question = ''.join([x['words'] + "是什么意思" for x in info['words_result'][:1]])
        if (question == '开始对战'):
            m.move(684, 882)
            m.click()
        resy = baidu(question, answers)
        print(question)
        print(resy)


if __name__ == '__main__':
    run()
