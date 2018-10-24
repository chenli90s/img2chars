import numpy as np
import cv2
import imageio

def gif2Img(file, size):

    img_list = []

    caps = imageio.mimread(file)
    # print(caps)
    for cap in caps:
        # cap = np.array(cap)
        gary = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(gary, size, interpolation=cv2.INTER_AREA)
        img_list.append(img)

    return img_list*2

pixels = " .,-'`:!1+*abcdefghijklmnopqrstuvwxyz<>()\/{}[]?234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ%&@#$"

def img2chars(img):
    res = []
    height, width = img.shape
    for row in range(height):
        line = ""
        for col in range(width):
            # 灰度是用8位表示的，最大值为255。
            # 这里将灰度转换到0-1之间
            percent = img[row][col] / 255

            # 将灰度值进一步转换到 0 到 (len(pixels) - 1) 之间，这样就和 pixels 里的字符对应起来了
            index = int(percent * (len(pixels) - 1))

            # 添加字符像素（最后面加一个空格，是因为命令行有行距却没几乎有字符间距，用空格当间距）
            line += pixels[index] + " "
        res.append(line)
    return res

def imgs2chars(imgs):
    video_chars = []
    for img in imgs:
        video_chars.append(img2chars(img))

    return video_chars


import time
import subprocess
import os

def play_video(video_chars):
    """
    播放字符视频
    :param video_chars: 字符画的列表，每个元素为一帧
    :return: None
    """
    # 获取字符画的尺寸
    width, height = len(video_chars[0][0]), len(video_chars[0])

    for pic_i in range(len(video_chars)):
        # 显示 pic_i，即第i帧字符画
        for line_i in range(height):
            # 将pic_i的第i行写入第i列。
            print(video_chars[pic_i][line_i])
        time.sleep(1 / 24)  # 粗略地控制播放速度。

        # subprocess.call("clear")  # 调用shell命令清屏
        os.system("cls")


import curses

def play_unix_video(video_chars):
    """
    播放字符视频，
    :param video_chars: 字符画的列表，每个元素为一帧
    :return: None
    """
    # 获取字符画的尺寸
    width, height = len(video_chars[0][0]), len(video_chars[0])

    # 初始化curses，这个是必须的，直接抄就行
    stdscr = curses.initscr()
    curses.start_color()
    try:
        # 调整窗口大小，宽度最好略大于字符画宽度。另外注意curses的height和width的顺序
        stdscr.resize(height, width * 2)

        for pic_i in range(len(video_chars)):
            # 显示 pic_i，即第i帧字符画
            for line_i in range(height):
                # 将pic_i的第i行写入第i列。(line_i, 0)表示从第i行的开头开始写入。最后一个参数设置字符为白色
                stdscr.addstr(line_i, 0, video_chars[pic_i][line_i], curses.COLOR_GREEN)
            stdscr.refresh()  # 写入后需要refresh才会立即更新界面

            time.sleep(1 / 14)  # 粗略地控制播放速度。更精确的方式是使用游戏编程里，精灵的概念
    finally:
        # curses 使用前要初始化，用完后无论有没有异常，都要关闭
        curses.endwin()
    return


if __name__ == '__main__':
    imgs = gif2Img('./imgs.gif', (38, 44))
    video_chars = imgs2chars(imgs)
    # print(video_chars)
    # play_video(video_chars)
    play_unix_video(video_chars)
