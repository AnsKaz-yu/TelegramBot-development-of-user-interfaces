import os
import time

import numpy as np
from matplotlib import pyplot as plt
import warnings


def make_graph(bot, chat_id, percents):
    warnings.simplefilter("ignore", UserWarning)
    plt.style.use('dark_background')
    plt.figure(figsize=(5, 1))
    plt.barh(10, width=percents, height=10)
    plt.xlim([0, 100])
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    ts = int(time.time())
    img_path = str(chat_id) + str(ts) + '.png'
    plt.savefig(img_path, dpi=100)
    img = open(img_path, 'rb')
    bot.send_photo(chat_id, img)
    img.close()
    try:
        os.remove(img_path)
    except OSError:
        pass


