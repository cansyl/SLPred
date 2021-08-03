import os, joblib
directory = "saved_models/"
location_list = ["CYT", "MEM", "NUC", "MIT", "GLG", "ERE", "LYS", "EXC", "PEX"]
def read_threshold_weights():

    dict_locs_threshold_weights = dict()
    for loc in location_list:
        dict_locs_threshold_weights[loc] = dict()
        #print(loc)
        with open(directory+loc+"_saved_models/"+loc+"_threshold_model_weights.txt", "r") as fp:
            for line in fp:
                line_list = line.strip().split(":")
                if line_list[0].strip() == "Threshold":
                    threshold = float(line_list[1].strip())
                    dict_locs_threshold_weights[loc]["threshold"] = threshold
                    #print(threshold)
                else:
                    weight = float(line_list[1].strip())
                    line_sep = line_list[0].split("-")
                    feature_name, norm_method = line_sep[0].strip(), line_sep[1].strip()[0]
                    dict_locs_threshold_weights[loc][feature_name+"_"+norm_method] = weight
                    #print(feature_name+"_"+norm_method, weight)
    return dict_locs_threshold_weights
def form_dict_saved_models():
    dict_loc_feature_norm_models = dict()
    for loc in location_list:
        dict_loc_feature_norm_models[loc] = dict()
        for file_name in os.listdir(directory+loc+"_saved_models/"):
            if "threshold" in file_name:
                continue
            loaded_model = joblib.load(directory+loc+"_saved_models/"+file_name)
            feature_norm = file_name.split(".")[0][10:]
            dict_loc_feature_norm_models[loc][feature_norm] = loaded_model
    return dict_loc_feature_norm_models





