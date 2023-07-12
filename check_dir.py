import os


def check_dirs():
    dir = f'{os.getcwd()}\\files\\'
    dir2 = f'{os.getcwd()}\\files\\collections\\'
    dir6 = f'{os.getcwd()}\\files\\col_product\\'
    dir3 = f'{os.getcwd()}\\files\\result\\'
    dir4 = f'{os.getcwd()}\\files\\result\\collections\\'
    dir5 = f'{os.getcwd()}\\files\\result\\tovar\\'

    if not os.path.exists(dir):
        os.mkdir(dir)

    if not os.path.exists(dir2):
        os.mkdir(dir2)

    if not os.path.exists(dir3):
        os.mkdir(dir3)

    # if not os.path.exists(dir4):
    #     os.mkdir(dir4)

    if not os.path.exists(dir5):
        os.mkdir(dir5)

    if not os.path.exists(dir6):
        os.mkdir(dir6)
