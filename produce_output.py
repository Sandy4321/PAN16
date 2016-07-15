import os
import json


# create clustering.json and ranking.json for each folder

def create_output_folder_problem(output_folder, dict_file):
    for k, v in dict_file.iteritems():
        output_each_problem = output_folder + "/" + k
        if not os.path.exists(output_each_problem):
            os.makedirs(output_each_problem)


def write_cluster(dict_output, out_folder):
    list_all = []
    list_val = []
    for v in dict_output.values():
        list_val.append(v)
    set_val = set(list_val)

    for val in set_val:
        list_per_cluster = []
        for k, v in dict_output.iteritems():
            if val == v:
                list_per_cluster.append(k)
        list_all.append(list_per_cluster)

    list_all_output = []
    for i in xrange(len(list_all)):
        list_cluster = []
        for j in xrange(len(list_all[i])):
            dict_per_doc = {}
            dict_per_doc["document"] = list_all[i][j] + ".txt"
            list_cluster.append(dict_per_doc)
        list_all_output.append(list_cluster)

    out_path = out_folder + "/clustering.json"
    out_file = open(out_path, "w")

    json.dump(list_all_output, out_file, indent=4)
    return list_all_output


def write_ranking(comb_list, all_sim, out_folder):
    list_all_output = []
    for i in xrange(len(comb_list)):
        dict_sim_perpair = {}
        dict_sim_perpair["document1"] = comb_list[i][0]
        dict_sim_perpair["document2"] = comb_list[i][1]
        dict_sim_perpair["score"] = round(all_sim[i][0][0],6)
        list_all_output.append(dict_sim_perpair)
    out_path = out_folder + "/ranking.json"
    out_file = open(out_path, "w")

    json.dump(list_all_output, out_file, indent=4)
    return list_all_output
