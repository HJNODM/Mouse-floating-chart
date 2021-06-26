# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 让jupyternotebook直接在单元格内显示生成的图形
# %matplotlib inline
# 解决matplotlib在windows电脑上中文乱码问题
plt.rcParams['font.sans-serif'] = 'SimHei'
# 解决matplotlib负号无法显示的问题
plt.rcParams['axes.unicode_minus'] = False


# 让图形变成矢量形式，显示更清晰
# %config InlineBackend.figure_format='svg'

def df_data_procee():
    df = pd.read_csv('ans.csv')
    df['未平仓认沽合约数（张）'] = df['未平仓认沽合约数（张）'].astype(int)
    df['未平仓认购合约数（张）'] = df['未平仓认购合约数（张）'].astype(int)
    df['认沽成交量（张）'] = df['认沽成交量（张）'].astype(int)
    df['认购成交量（张）'] = df['认购成交量（张）'].astype(int)
    df['num_1'] = round(df['未平仓认沽合约数（张）'] / df['未平仓认购合约数（张）'], 3)
    df['num_2'] = round(df['认沽成交量（张）'] / df['认购成交量（张）'], 3)
    return df


def matplotlib_make(x, y, title):
    len_y = len(y)
    x_index = range(len_y)
    _y = [y[-1]] * len_y

    fig = plt.figure(figsize=(20, 15))
    ax1 = fig.add_subplot(1, 1, 1)

    ax1.plot(x, y, color='blue')
    ax1.set_xticks([])
    line_x = ax1.plot(x_index, _y, color='skyblue')[0]
    line_y = ax1.axvline(x=len_y - 1, color='skyblue')

    ax1.set_title(title)

    text0 = plt.text(len_y - 1, y[-1], str(y[-1]), fontsize=10)

    def scroll(event):
        axtemp = event.inaxes
        x_min, x_max = axtemp.get_xlim()
        fanwei_x = (x_max - x_min) / 10
        if event.button == 'up':
            axtemp.set(xlim=(x_min + fanwei_x, x_max - fanwei_x))
        elif event.button == 'down':
            axtemp.set(xlim=(x_min - fanwei_x, x_max + fanwei_x))
        fig.canvas.draw_idle()

    def motion(event):
        try:
            temp = y[int(np.round(event.xdata))]
            for i in range(len_y):
                _y[i] = temp
            line_x.set_ydata(_y)
            line_y.set_xdata(event.xdata)
            text0.set_position((event.xdata, temp))
            text0.set_text(str(temp))

            fig.canvas.draw_idle()
        except:
            pass

    fig.canvas.mpl_connect('scroll_event', scroll)
    fig.canvas.mpl_connect('motion_notify_event', motion)

    plt.show()


if __name__ == '__main__':
    df = df_data_procee()
    x = list(df['日期'])
    y1 = list(df['num_1'])
    y2 = list(df['num_2'])
    matplotlib_make(x, y1, 'num_1')
    matplotlib_make(x, y2, 'num_2')
