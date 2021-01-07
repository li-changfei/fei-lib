# import curses
import time
import subprocess
import numpy

print("hello world!")

video_chars = [[0 for i in range(2000)] for i in range(2000)]

video_chars = numpy.full([160, 25], '■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■')

myTemplate_e = ['■■■■■　　　　　　　　　　　　　　　■■■■■■■■■■',
                '■■■■■　　　　　　　　　　　　　　　■■■■■■■■■■',
                '■■■■■　　■■■■■■■■■■■■■■■■■■■■■■■',
                '■■■■■　　■■■■■■■■■■■■■■■■■■■■■■■',
                '■■■■■　　■■■■■■■■■■■■■■■■■■■■■■■',
                '■■■■■　　■■■■■■■■■■■■■■■■■■■■■■■',
                '■■■■■　　■■■■■■■■■■■■■■■■■■■■■■■',
                '■■■■■　　■■■■■■■■■■■■■■■■■■■■■■■',
                '■■■■■　　■■■■■■■■■■■■■■■■■■■■■■■',
                '■■■■■　　　　　　　　　　　　　　■■■■■■■■■■■',
                '■■■■■　　　　　　　　　　　　　　■■■■■■■■■■■',
                '■■■■■　　■■■■■■■■■■■■■■■■■■■■■■■',
                '■■■■■　　■■■■■■■■■■■■■■■■■■■■■■■',
                '■■■■■　　■■■■■■■■■■■■■■■■■■■■■■■',
                '■■■■■　　■■■■■■■■■■■■■■■■■■■■■■■',
                '■■■■■　　■■■■■■■■■■■■■■■■■■■■■■■',
                '■■■■■　　■■■■■■■■■■■■■■■■■■■■■■■',
                '■■■■■　　■■■■■■■■■■■■■■■■■■■■■■■',
                '■■■■■　　　　　　　　　　　　　　　■■■■■■■■■■',
                '■■■■■　　　　　　　　　　　　　　　■■■■■■■■■■']



width, height = len(video_chars[0][0]), len(video_chars[0])
print(str(width) + "/" + str(height) + "/" + str(len(video_chars)))
index = 0
loopCount1 = 0
loopCount2 = 0
loopCount3 = 0

index_e = 0
index_c= 0


def multi_sub(string, p, c):
    new = []
    for s in string:
        new.append(s)
    new[p] = c
    return ''.join(new)


for pic_i in range(len(video_chars)):
    # 英字「N」の表示
    if index < 56:
        loopCount1 = index
        if index > 20:
            loopCount1 = 20
            loopCount2 = index - 20
            if index > 36:
                loopCount2 = 16
                loopCount3 = index - 36
                if index > 52:
                    loopCount3 = 16
                for step_i3 in range(loopCount3):
                    # video_chars[pic_i][20 - step_i3][18] = 1
                    video_chars[pic_i][20 - step_i3] = multi_sub(video_chars[pic_i][20 - step_i3], 18, '　')
                    # video_chars[pic_i][20 - step_i3][18 + 1] = 1
                    video_chars[pic_i][20 - step_i3] = multi_sub(video_chars[pic_i][20 - step_i3], 19, '　')

            for step_i2 in range(loopCount2):
                startCount = 8 - (step_i2 // 2)
                # video_chars[pic_i][5 + step_i2][startCount + step_i2] = 1
                video_chars[pic_i][5 + step_i2] = multi_sub(video_chars[pic_i][5 + step_i2], startCount + step_i2, '　')
                # video_chars[pic_i][5 + step_i2][startCount + 1 + step_i2] = 1
                video_chars[pic_i][5 + step_i2] = multi_sub(video_chars[pic_i][5 + step_i2], startCount + step_i2 + 1, '　')

        for step_i1 in range(loopCount1):
            # video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i1][6] = "1"
            video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i1] = multi_sub(video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i1], 6, '　')
            # video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i1][6 + 1] = "1"
            video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i1] = multi_sub(video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i1], 7, '　')

        if 51 < index:
            for step_i4 in range(index - 51):
                # video_chars[pic_i][len(video_chars[pic_i]) - 1 - (index - 51)][6] = 0
                video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i4] = multi_sub(video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i4], 6, '■')
                # video_chars[pic_i][len(video_chars[pic_i]) - 1 - (index - 51)][6 + 1] = 0
                video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i4] = multi_sub(video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i4], 7, '■')
    elif index < 65:
        for step_i1 in range(20):
            # video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i1][6] = 1
            video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i1] = multi_sub(video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i1], 6, '　')
            # video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i1][6 + 1] = 1
            video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i1] = multi_sub(video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i1], 7, '　')
        for step_i2 in range(16):
            startCount = 8 - (step_i2 // 2)
            # video_chars[pic_i][5 + step_i2][startCount + step_i2] = 1
            video_chars[pic_i][5 + step_i2] = multi_sub(video_chars[pic_i][5 + step_i2], startCount + step_i2, '　')
            # video_chars[pic_i][5 + step_i2][startCount + 1 + step_i2] = 1
            video_chars[pic_i][5 + step_i2] = multi_sub(video_chars[pic_i][5 + step_i2], startCount + step_i2 + 1, '　')
        for step_i3 in range(16):
            # video_chars[pic_i][20 - step_i3][18] = 1
            video_chars[pic_i][20 - step_i3] = multi_sub(video_chars[pic_i][20 - step_i3], 18, '　')
            # video_chars[pic_i][20 - step_i3][18 + 1] = 1
            video_chars[pic_i][20 - step_i3] = multi_sub(video_chars[pic_i][20 - step_i3], 19, '　')
        for step_i4 in range(4):
            # video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i4][6] = 0
            video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i4] = multi_sub(video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i4], 6, '■')
            # video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i4][6 + 1] = 0
            video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i4] = multi_sub(video_chars[pic_i][len(video_chars[pic_i]) - 1 - step_i4], 7, '■')
    elif index < 115:
        if index_e < 21:
            for step_e_1 in range(index_e):
                video_chars[pic_i][step_e_1] = myTemplate_e[len(myTemplate_e)  - index_e + step_e_1]
        else:
            for step_e_1 in range(20):
                if step_e_1 + index_e - 20 < 25:
                    video_chars[pic_i][step_e_1 + index_e - 20] = myTemplate_e[len(myTemplate_e) - 20 + step_e_1]
        index_e = index_e + 1
    else:
        if index_c < 21:
            for step_c_1 in range(index_c):
                video_chars[pic_i][len(video_chars[pic_i]) - index_c + step_c_1] = myTemplate_e[step_c_1]
        else:
            for step_c_1 in range(20):
                if step_c_1 + index_c - 20 < 25:
                    video_chars[pic_i][len(video_chars[pic_i] - index_c + step_c_1) - index_c + step_c_1] = myTemplate_e[step_c_1]
        index_c = index_c + 1

    index = index + 1

    # 显示 pic_i，即第i帧字符画
    for line_i in range(height):
        # 将pic_i的第i行写入第i列。
        print(video_chars[pic_i][line_i])

    time.sleep(1 / 30)  # 粗略地控制播放速度。

    # 调用 shell 命令清屏
    # subprocess.run("clear", shell=True)  # linux 版
    subprocess.run("cls", shell=True)


