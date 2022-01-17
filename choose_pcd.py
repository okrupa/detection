import os
from os import listdir
from os.path import isfile, join
import glob


def get_list():
    cwd = os.path.abspath(os.getcwd())
    path_img = os.path.join(cwd, "images")
    path_pcd = os.path.join(cwd, "pointclouds")
    if os.path.exists("images") and os.path.exists("pointclouds"):
        p_img = path_img+"/*.png"
        p_pcd = path_pcd + "/*.pcd"
        imgs = [f for f in glob.glob(p_img)]
        pcd = [f for f in glob.glob(p_pcd)]
        imgs.sort()
        pcd.sort()

        return imgs, pcd
    else:
        print("Direcory ./images or ./pointclouds doesnt exist.")
        return [], []

def get_pcd(imgs, pcd, num):
    # img = imgs[num]
    # pcd_file = pcd[num]
    # return pcd_file, img
    pcd_file = pcd[num]
    return pcd_file


def get_first():
    imgs, pcd = get_list()

    if imgs and pcd:
        # return get_pcd(imgs, pcd, 0)
        return [get_pcd(imgs, pcd, 0)]
    else:
        return

def get_sequence(step):
    # imgs, pcd = get_list()
    # num_files = len(pcd)
    # files = []
    # if imgs and pcd:
    #     for i in range(0, num_files, 10):
    #         files.append(get_pcd(imgs, pcd, i))
    #     return files
    # else:
    #     return
    imgs, pcd = get_list()
    num_files = len(pcd)
    files = []
    if imgs and pcd:
        for i in range(0, num_files, step):

            pcd_file = get_pcd(imgs, pcd, i)
            files.append(pcd_file)
        return files
    else:
        return