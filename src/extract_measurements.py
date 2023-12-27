import numpy as np
import os
from pathlib import Path

DATA_DIR = str(Path(__file__).resolve().parents[1] / "smpl_models")
M_NUM = 11  # 19
M_STR = [
    "height",
    "waist",
    "belly",
    "chest",
    "wrist",
    "neck",
    "arm length",
    "thigh",
    "shoulder width",
    "hips",
    "ankle",
]


# read control  points(CP) from text file
def convert_cp():
    f = open(os.path.join(DATA_DIR, "customBodyPoints.txt"), "r")

    tmplist = []
    cp = []
    for line in f:
        if "#" in line:
            if len(tmplist) != 0:
                cp.append(tmplist)
                tmplist = []
        elif len(line.split()) == 1:
            continue
        else:
            tmplist.append(list(map(float, line.strip().split())))
    cp.append(tmplist)

    return cp


# calculate measure data from given vertex by control points
def calc_measure(cp, vertex, height):  # , facet):
    measure_list = []

    for measure in cp:
        #    print("#########################",measure)
        #    print("@@@@@@@@@@@@")

        length = 0.0
        p2 = vertex[int(measure[0][1]), :]

        for i in range(0, len(measure)):  # 1
            p1 = p2
            if measure[i][0] == 1:
                p2 = vertex[int(measure[i][1]), :]

            elif measure[i][0] == 2:
                p2 = (
                    vertex[int(measure[i][1]), :] * measure[i][3]
                    + vertex[int(measure[i][2]), :] * measure[i][4]
                )
            #        print("if 2 Measurement",int(measure[i][1]))

            else:
                p2 = (
                    vertex[int(measure[i][1]), :] * measure[i][4]
                    + vertex[int(measure[i][2]), :] * measure[i][5]
                    + vertex[int(measure[i][3]), :] * measure[i][6]
                )
            length += np.sqrt(np.sum((p1 - p2) ** 2.0))

        measure_list.append(length * 100)  # * 1000

    measure_list = float(height) * (measure_list / measure_list[0])
    #  print("measure list = ",float(height)*(measure_list/measure_list[0]))
    measure_list[8] = (
        measure_list[8] * 0.36
    )  # reducing the error in measurement added due to unarranged vertices
    measure_list[3] = measure_list[3] * 0.6927
    #  print("measure list = ",float(height)*(measure_list/measure_list[0]))
    #  measure_list = float(height)*(measure_list/measure_list[0])
    return np.array(measure_list).reshape(M_NUM, 1)


# added code: extract body measurements given a .obj model in data.
def extract_measurements(height, vertices):
    genders = ["male"]  # , "male"]
    measure = []
    for gender in genders:
        # generate and load control point from txt to npy file
        cp = convert_cp()

        #    vertex = obj2npy(gender)[0]
        # calculte + convert
        measure = calc_measure(cp, vertices, height)

        # give body measurements one by one
        for i in range(0, M_NUM):
            print("%s: %f" % (M_STR[i], measure[i]))


# if __name__ == "__main__":
#  extract_measurements()
