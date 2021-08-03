import numpy as np
from sklearn.preprocessing import MinMaxScaler, RobustScaler, PowerTransformer, StandardScaler


def read_iFeatures():
    file_feat = open("iFeatures_list", "r")
    set_iFeatures = set()
    for line in file_feat:
        set_iFeatures.add(line.strip())
    return set_iFeatures

def read_points_file(filename):
    pts = []
    prot_id_list = list()
    with open(filename, "r") as file_r:
        for line in file_r:
            if line[0] == "#":
                continue
            list_line = line.strip("\n").split()

            pt = list_line[1:]
            #print(pt)
            ls = [float(value) for value in pt]
            pts.append(ls)
    return prot_id_list, pts

def read_data_train(directory,loc, FVTYPE):
    pos_prot_id_list, pts_0 = read_points_file(directory + loc +"/iFeature_descriptors_results/"
                                + loc +"_trust_all_positive_" + FVTYPE + ".fv")

    neg_prot_id_list, pts_1 = read_points_file(directory + loc +"/iFeature_descriptors_results/"
                                + loc +"_trust_all_negative_" + FVTYPE + ".fv")

    x = pts_0 + pts_1

    x = np.array(x)
    #print(x.shape)
    return  x

def read_points_spmap(filename):
    pts = []
    prot_id_list = list()
    with open(filename, "r") as file_r:
        for line in file_r:
            list_line = line.strip("\n").split("\t")
            prot_id = list_line[0][1:].strip()
            prot_id_list.append(prot_id)
            pt = list_line[1:]
            #print(pt)
            ls = [float(value) for value in pt]
            pts.append(ls)
    return prot_id_list, pts
def read_spmap_features_train(directory,loc, FVTYPE):
    pos_prot_id_list, pts_0 = read_points_spmap(directory + loc + "/SPMAP_descriptor_results/"
                                               + loc + "_trust_all_positive_" + FVTYPE + ".fv")

    neg_prot_id_list, pts_1 = read_points_spmap(directory + loc + "/SPMAP_descriptor_results/"
                                               + loc + "_trust_all_negative_" + FVTYPE + ".fv")

    x = pts_0 + pts_1
    #labels = [0] * len(pts_0) + [1] * len(pts_1)
    x = np.array(x)
    #print(x.shape)
    return  x

def read_points_pssm(filename):
    pts = []

    with open(filename, "r") as file_r:
        count = 0
        for line in file_r:
            if count == 0:
                count += 1
                continue
            list_line = line.strip("\n").split(",")
            #print(list_line)

            pt = list_line
            ls = list()
            for value in pt:
                if value == "-inf":
                    value = "-9999999"
                elif value == "inf":
                    value = "9999999"

                ls.append(float(value))
            pts.append(ls)
    return pts
def read_pssm_features_train(directory,loc, FVTYPE):
    pts_0 = read_points_pssm(directory + loc +"/POSSUM_descriptors_results/"
                                + loc +"_trust_all_positive_" + FVTYPE + ".csv")
    pts_1 = read_points_pssm(directory + loc +"/POSSUM_descriptors_results/"
                                + loc +"_trust_all_negative_" + FVTYPE + ".csv")
    x = pts_0 + pts_1
    #print(x)
    #labels = [0] * len(pts_0) + [1] * len(pts_1)
    x = np.array(x)
    #print(x.shape)
    return x

