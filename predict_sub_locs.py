from sklearn.preprocessing import MinMaxScaler, RobustScaler, PowerTransformer, StandardScaler

from load_saved_models import read_threshold_weights, form_dict_saved_models
from utils import read_spmap_features, read_pssm_features, read_iFeatures
from utils_train_data import read_data_train, read_spmap_features_train, read_pssm_features_train
from utils import read_data
import sys


def read_train_data(loc, feature_name):
    directory = "Trust_all_data/"
    set_iFeatures = read_iFeatures()
    #print(feature_name)
    if feature_name in set_iFeatures:
         X_train = \
            read_data_train(directory, loc, feature_name)
    elif feature_name == "SPMAP":
         X_train = \
            read_spmap_features_train(directory, loc, feature_name)
    else:
        X_train = read_pssm_features_train(directory,  loc, feature_name)
    #print(X_test.shape)
    return X_train
def read_test_data(feature_directory, file_name, loc, feature_name):
    test_prot_id_list = []
    set_iFeatures = read_iFeatures()
    if feature_name in set_iFeatures:
        test_prot_id_list, X_test = \
            read_data(feature_directory, file_name, feature_name)
    elif feature_name == "SPMAP":
        test_prot_id_list, X_test = \
            read_spmap_features(feature_directory, file_name, loc, feature_name)
    else:
        X_test = read_pssm_features(feature_directory,  file_name, feature_name)
    #print(X_test)
    return test_prot_id_list,  X_test
def normalize_and_predict(X_train, X_test, clf, norm):
    scaler = norm
    #print(X_train.shape, X_test.shape)
    scaler.fit(X_train)
    X_test = scaler.transform(X_test)
    predictions = clf.predict_proba(X_test)
    return predictions


def form_probabilistic_results(feature_directory, file_name, loc,  dict_feature_norm_models, dict_threshold_weights):
    all_preds = list()
    list_weights =list()
    test_prot_id_list = []
    for feature_norm in dict_feature_norm_models:
        len_fn = len(feature_norm)
        norm = feature_norm[len_fn-1]
        if norm == "M":
            norm = MinMaxScaler()
        elif norm == "R":
            norm = RobustScaler()
        elif norm == "P":
            norm = PowerTransformer()
        elif norm == "S":
            norm = StandardScaler()

        feature_name = feature_norm[0:len_fn-2]
        list_weights.append(dict_threshold_weights[feature_norm])
        clf = dict_feature_norm_models[feature_norm]
        X_train = read_train_data(loc, feature_name)
        test_prot_id_list, X_test = read_test_data(feature_directory, file_name, loc, feature_name)

        predictions = normalize_and_predict(X_train, X_test, clf, norm)
        all_preds.append(predictions)
    return all_preds, list_weights

def vote_predictions(all_preds, threshold, list_weights):
    final_pr = list()
    for i in range(len(all_preds[0])):
        sum_0, sum_1 = 0, 0
        for j in range(len(all_preds)):

            sum_0 += list_weights[j] * all_preds[j][i][0]
            sum_1 += list_weights[j] * all_preds[j][i][1]

        if sum_0/sum(list_weights) > threshold:
            final_pr.append(1)
        else:
            final_pr.append(0)
    return final_pr

def read_prot_id_from_fasta(file_name):
    test_prot_id_list = list()
    with open("input_files/fasta_files/{}.fasta".format(file_name), "r") as fp:
        for line in fp:
            if line[0] == ">":
                test_prot_id_list.append(line.strip()[1:])
    return test_prot_id_list

def predict_sub_locs(feature_directory, file_name):
    dict_locs_threshold_weights = read_threshold_weights()
    dict_locs_feature_norm_models = form_dict_saved_models()
    dict_prot_id_loc_predictions = dict()
    for loc in dict_locs_feature_norm_models:
        all_preds, list_weights = form_probabilistic_results(feature_directory, file_name, loc, dict_locs_feature_norm_models[loc], dict_locs_threshold_weights[loc])

        test_prot_id_list = read_prot_id_from_fasta(file_name)
        threshold = dict_locs_threshold_weights[loc]["threshold"]
        final_pr = vote_predictions(all_preds, threshold, list_weights)
        for prot_id, pred in zip(test_prot_id_list, final_pr):
            if prot_id not in dict_prot_id_loc_predictions:
                dict_prot_id_loc_predictions[prot_id] = dict()
            dict_prot_id_loc_predictions[prot_id][loc] = pred
    return dict_prot_id_loc_predictions
def write_predictions_to_a_file(file_name, dict_prot_id_loc_predictions):
    loc_list = ['CYT', 'MEM', 'NUC', 'MIT', 'GLG', 'ERE', 'LYS', 'EXC', 'PEX']
    with open("predictions/{}_predictions.csv".format(file_name),  "w") as fw:
        fw.write("Protein ID")
        for loc_name in loc_list:
            fw.write("," + loc_name)
        fw.write("\n")
        for prot_id in dict_prot_id_loc_predictions:
            fw.write(prot_id)
            for loc_name in loc_list:
                fw.write("," + str(dict_prot_id_loc_predictions[prot_id][loc_name]))
            fw.write("\n")
    fw.close()
    print ("You can retrieve the predictions from {}/{}_predictions.csv".format("predictions", file_name))





