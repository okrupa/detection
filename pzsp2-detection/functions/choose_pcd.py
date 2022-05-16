import os
import glob
import shutil

def get_list(cwd):
    path_img = os.path.join(cwd, "images")
    path_pcd = os.path.join(cwd, "pointclouds")

    if os.path.exists(path_img) and os.path.exists(path_pcd):
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
    pcd_file = pcd[num]
    return pcd_file


def save_jpg(imgs,num, path):
    src = imgs[num]
    shutil.copy(src, path)


def get_first(dir):
    imgs, pcd = get_list(dir)

    if imgs and pcd:
        path_save_jpg = os.path.join(dir, "jpg_sequence")
        save_jpg(imgs, 0, path_save_jpg)
        return [get_pcd(imgs, pcd, 0)]


#wybierz co x plik pcd
def get_sequence(step, dir):
    imgs, pcd = get_list(dir)
    num_files = len(pcd)
    files = []
    if imgs and pcd:
        file_name = 0
        path_save_jpg = os.path.join(dir, "jpg_sequence")
        for i in range(0, num_files, step):
            save_jpg(imgs, i, path_save_jpg)
            pcd_file = get_pcd(imgs, pcd, i)
            files.append(pcd_file)
            file_name += 1
        return files