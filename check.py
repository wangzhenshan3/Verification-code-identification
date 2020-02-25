import requests
import pytesseract
import re
from PIL import Image

def deal_img():
    i = 0
    img = Image.open('C:\\Users\\DELL\\PycharmProjects\\untitled\\1.jpg')
    img = img.convert("RGBA")
    while i < 5:
        i = i + 1
        pixdata = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][0] < 120:
                    pixdata[x, y] = (0, 0, 0, 255)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][1] < 120:
                    pixdata[x, y] = (0, 0, 0, 255)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][2] > 0:
                    pixdata[x, y] = (255, 255, 255, 255)

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][0] < 254:
                    pixdata[x, y] = (0, 0, 0, 255)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][1] < 254:
                    pixdata[x, y] = (0, 0, 0, 255)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][2] > 0:
                    pixdata[x, y] = (255, 255, 255, 255)


        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y] == (255, 255, 0, 255):
                    pixdata[x, y] = (0, 0, 0, 255)
    img.save('C:\\Users\\DELL\\PycharmProjects\\untitled\\2.png', "png")

def fall ():
    white = (255,255,255,255)
    black = (0,0,0,255)
    img = Image.open('C:\\Users\\DELL\\PycharmProjects\\untitled\\2.png')
    pixdata = img.load()
    X = img.size[0]-1
    Y = img.size[1]-1

    def icolor(RGBA):
        if RGBA == white:
            return(1)
        else:
            return(0)

    for y in range(Y):
        for x in range(X):
            if (x<1 or y<1):
                pass
            else:
                if icolor(pixdata[x,y]) == 1:
                    pass
                else:
                    if (
                         icolor(pixdata[x+1,y])+
                         icolor(pixdata[x,y+1])+
                         icolor(pixdata[x-1,y])+
                         icolor(pixdata[x,y-1])+
                         icolor(pixdata[x-1,y-1])+
                         icolor(pixdata[x+1,y-1])+
                         icolor(pixdata[x-1,y+1])+
                         icolor(pixdata[x+1,y+1])
                         )>5:

                        pixdata[x,y] = white


    for y in range(Y):
        for x in range(X):
            if (x<1 or y<1):
                pass
            else:
                if icolor(pixdata[x,y]) == 0:
                    pass
                else:
                    if (
                         (icolor(pixdata[x+1,y]))+
                         (icolor(pixdata[x,y+1]))+
                         (icolor(pixdata[x-1,y]))+
                         (icolor(pixdata[x,y-1]))
                         )<2:

                        pixdata[x,y] = black

    for y in range(Y):
        for x in range(X):
            if (x<1 or y<1):
                pass
            else:
                if icolor(pixdata[x,y]) == 1:
                    pass
                else:
                    if (
                         icolor(pixdata[x+1,y])+
                         icolor(pixdata[x,y+1])+
                         icolor(pixdata[x-1,y])+
                         icolor(pixdata[x,y-1])
                         )>2:
                        pixdata[x,y] = white
    img.save('C:\\Users\\DELL\\PycharmProjects\\untitled\\3.png', "png")

def readcCode():
    try:
        img = Image.open('C:\\Users\\DELL\\PycharmProjects\\untitled\\3.png')
        tessdata_dir_config = '--tessdata-dir "C:\\Users\\DELL\\PycharmProjects\\untitled\\venv.py\\Lib\\site-packages\\Tesseract-OCR\\tessdata"'
        text = pytesseract.image_to_string(img, config=tessdata_dir_config)
        text = text.replace(' ', '')
        tip = True
        if text == "":
            tip = False

        if re.search(r'[0-9a-zA-Z]{4}',text):
            pass
        else:
            tip = False
        if len(text) !=4:
            tip = False

    except UnicodeDecodeError as e:
        tip = False


    if tip == False:

        print("验证码识别失败")
        exit(-1)

    else:
        print("识别到验证码为")
        print(text)
        return(text)


def login():
    s=requests.session()
    url="http://jwxt.bupt.edu.cn"
    url2="http://jwxt.bupt.edu.cn/validateCodeAction.do?random="
    url3="http://jwxt.bupt.edu.cn/jwLoginAction.do"
    post_data={
        'zjh':'***',
        'mm':'***',
        'type': 'sso',
        'v_yzm':None
    }
    res=s.get(url2)
    with open('1.jpg','wb')as f:
        f.write(res.content)

    deal_img()
    fall()
    post_data['v_yzm']=readcCode()
    res=s.post(url3, data=post_data)
    print(res.text)


login()