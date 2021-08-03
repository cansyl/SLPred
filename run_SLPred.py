from feature_extraction_module import *
from predict_sub_locs import predict_sub_locs, write_predictions_to_a_file
import sys
import argparse
file_name = sys.argv[1]
parser = argparse.ArgumentParser(description='SLPred arguments')
parser.add_argument(
    '--file',
    type=str,
    default="input",
    help='fasta file name which is before .fasta')
if __name__ == "__main__":
    args = parser.parse_args()
    file_name = args.file
    print ("Preprocessing module is running...")
    form_single_fasta_files(file_name)
    print ("Position-specific-scoring matrices are being generated...")
    form_pssm_files(file_name)
    print ("Feature extraction module is running...")
    path2 = form_folders(file_name)
    iFeature_feature_extracter(file_name, path2)
    SpMap_feature_extracter(file_name, path2)
    POSSUM_feature_extracter(file_name,path2)
    feature_directory = "features/{}".format(file_name)
    print ("Prediction module is running...")
    dict_prot_id_loc_predictions = predict_sub_locs(feature_directory, file_name)
    write_predictions_to_a_file(file_name, dict_prot_id_loc_predictions)
