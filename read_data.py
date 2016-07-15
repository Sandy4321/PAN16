import csv
import codecs
import os
import json

# this code will be used to read data from each of the problem based on json file and store it as csv file


def open_text(path):
    opened_file = codecs.open(path, 'r')
    text = opened_file.read()
    return text


def file_info(path):
    info_path = open(path)
    data = json.load(info_path)
    info_path.close()

    dict_file = {}
    for i in xrange(len(data)):
        dict_file[data[i][str("folder")]] = data[i][str("language")]
    return dict_file


def convert_to_csv(all_problem_path, csv_path, dict_info):
    for k, v in dict_info.iteritems():
        problem_path = all_problem_path + "/" + k
        all_data = [["id", "article"]]
        for subdir, dirs, files in os.walk(problem_path):
            all_data = [["id", "article"]]
            for file_ in files:
                each_file = []
                file_path = subdir + os.path.sep + file_
                file_id = file_.split(".")[0]
                file_text = open_text(file_path)
                # file_text = unicode(file_text).encode('utf-8', errors='ignore')
                each_file.append(file_id)
                each_file.append(file_text)
                all_data.append(each_file)
        pro_path = problem_path.split("/")
        file_name = csv_path + "/" + pro_path[-1] + "." + dict_info[k] + ".csv"
        with codecs.open(file_name, 'wb') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL, dialect='excel')
            writer.writerows(all_data)
