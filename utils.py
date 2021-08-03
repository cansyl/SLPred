import numpy as np
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
            list_line = line.strip("\n").split("\t")
            prot_id = list_line[0][1:].strip()
            prot_id_list.append(prot_id)
            pt = list_line[1:]
            #print(pt)
            ls = [float(value) for value in pt]
            pts.append(ls)
    return prot_id_list, pts

def read_data(directory,file_name, FVTYPE):
    prot_id_list, x = read_points_file("{}/iFeature_descriptors_results/{}_{}.txt".format(directory, file_name, FVTYPE))
    x = np.array(x)
    #print(FVTYPE, x.shape)
    return prot_id_list, x

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
def read_spmap_features(directory, file_name, loc, FVTYPE):
    prot_id_list, x = read_points_spmap("{}/SPMAP_descriptors_results/{}_{}_spmap.txt"\
                                        .format(directory,file_name, loc))


    x = np.array(x)
    #print(FVTYPE, x.shape)
    return prot_id_list, x

def read_points_pssm(filename):
    pts = []

    with open(filename, "r") as file_r:

        for line in file_r:

            list_line = line.strip("\n").split(",")

            pt = list_line

            #print(pt)
            ls = list()
            for value in pt:
                if value == "-inf":
                    value = "-9999999"
                elif value == "inf":
                    value = "9999999"

                ls.append(float(value))
            pts.append(ls)
    return pts
def read_pssm_features(directory,file_name, FVTYPE):
    x = read_points_pssm("{}/POSSUM_descriptors_results/{}_{}.txt".format(directory, file_name, FVTYPE))



    x = np.array(x)
    #print(FVTYPE, x.shape)
    return x