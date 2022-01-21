import os
import glob


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


def get_first(CONST_DIR):
    imgs, pcd = get_list(CONST_DIR)

    if imgs and pcd:
        return [get_pcd(imgs, pcd, 0)]

#wybierz co x plik pcd
def get_sequence(step, dir):
    imgs, pcd = get_list(dir)
    num_files = len(pcd)
    files = []
    if imgs and pcd:
        for i in range(0, num_files, step):

            pcd_file = get_pcd(imgs, pcd, i)
            files.append(pcd_file)
        return files