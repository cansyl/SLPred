from run_psi_blast import *


def form_folders(filename):
    path1 = "features"
    if os.path.isdir(path1) == False:
        os.mkdir(path1)
    path2 = "{}/{}".format(path1, filename)
    if os.path.isdir(path2) == False:
        os.mkdir(path2)
    return path2

def iFeature_feature_extracter(filename, path2):
    iFeature_descriptor_list = ["AAC", "PAAC", "APAAC", "DPC", "GAAC", "CKSAAP", "CKSAAGP", "GDPC", "Moran", "Geary",
                                "NMBroto", "CTDC", "CTDD", "CTDT", "CTriad", "KSCTriad", "SOCNumber", "QSOrder"]

    if os.path.isdir("{}/iFeature_descriptors_results".format(path2))== False:
        os.mkdir("{}/iFeature_descriptors_results".format(path2))

    for descr in iFeature_descriptor_list:
        os.system("python3 iFeature/iFeature.py --file input_files/fasta_files/{}.fasta --type {}" \
                  " --out {}/iFeature_descriptors_results/{}_{}.txt".format(filename, descr, path2, filename, descr))
def POSSUM_feature_extracter(filename, path2):

    POSSUM_descriptor_list = ["aac_pssm", "d_fpssm", "smoothed_pssm", "ab_pssm", "pssm_composition", "rpm_pssm",
                              "s_fpssm", "dpc_pssm", "k_separated_bigrams_pssm", "tri_gram_pssm", "eedp", "tpc",
                              "edp", "rpssm", "pse_pssm", "dp_pssm", "pssm_ac", "pssm_cc", "aadp_pssm", "aatp", "medp"]
    if os.path.isdir("{}/POSSUM_descriptors_results".format(path2))== False:
        os.mkdir("{}/POSSUM_descriptors_results".format(path2))
    for possum_descr in POSSUM_descriptor_list:
        print("POSSUM extracting {} features".format(possum_descr))
        os.system("python3 POSSUM_Standalone_Toolkit/src/possum.py -i input_files/fasta_files/{}.fasta"\
                  " -o {}/POSSUM_descriptors_results/{}_{}.txt -t {} -p input_files/pssm_files".format(filename,path2, filename, possum_descr, possum_descr))

def SpMap_feature_extracter(filename, path2):
    profile_list = ["CYT", "MEM", "NUC", "MIT", "GLG", "ERE", "LYS", "EXC", "PEX"]
    if os.path.isdir("{}/SPMAP_descriptors_results".format(path2))== False:
        os.mkdir("{}/SPMAP_descriptors_results".format(path2))
    for profilename in profile_list:
        print("SPMAP {} features extracting...".format(profilename))
        os.system("python3 SPMAP/spmap_features_generator.py -i input_files/fasta_files/{}.fasta -p SPMAP/profiles/{}.profile" \
                  " -o  {}/SPMAP_descriptors_results/{}_{}_spmap.txt".format(filename, profilename, path2, filename, profilename))
