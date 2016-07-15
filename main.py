import read_data
import os
import produce_output
import pandas as pd
import csv
import cluster
import gensim
import word2vec_average
import logging
import sys
import getopt


def main(argv):
    evaluation_dir = ''
    output_dir = ''

    if len(sys.argv) == 5:
        try:
            opts, args = getopt.getopt(argv, "hc:o:", ["cfile=", "ofile="])
        except getopt.GetoptError:
            print 'error'
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print 'main.py -c /path/to/evaluation/directory -o path/to/output/directory'
                sys.exit()
            elif opt in ("-c", "--cfile"):
                evaluation_dir = arg
            elif opt in ("-o", "--ofile"):
                output_dir = arg

    filelog = "Log.out"
    logging.basicConfig(filename=filelog, filemode='a', level=logging.DEBUG)

    info_path = os.path.join(evaluation_dir, "info.json")
    problem_folder = evaluation_dir
    dict_file = read_data.file_info(info_path)
    print dict_file
    # create folder to store csv file
    csv_folder = r"./csv"
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)
    print "convert to csv.."
    # convert to csv
    read_data.convert_to_csv(problem_folder, csv_folder, dict_file)

    # create folder to store output file
    output_folder = output_dir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    produce_output.create_output_folder_problem(output_folder, dict_file)

    print "processing each file.."
    # read each csv file and input to clustering algorithm
    for k, v in dict_file.iteritems():
        csv_path = "./csv/" + k + "." + v + ".csv"
        print csv_path
        out_path = os.path.join(output_folder, k)
        print out_path
        text = pd.read_csv(csv_path, header=0, quoting=csv.QUOTE_MINIMAL)
        labels = []
        vec_features = []
        dict_output = {}
        dict_features = {}

        if v == 'en':
            model = gensim.models.word2vec.Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
            vec_features = word2vec_average.getAvgFeatureVecs(word2vec_average.getCleanReviews(text, v), model, 300)
            labels = cluster.clustering_word2vec(vec_features)
        elif v == "nl":
            model = gensim.models.word2vec.Word2Vec.load('nl-word2vec-model-300-word.bin')
            vec_features = word2vec_average.getAvgFeatureVecs(word2vec_average.getCleanReviews(text, v), model, 300)
            labels = cluster.clustering_word2vec(vec_features)
        elif v == 'gr':
            all_sent = []
            for article in text['article']:
                all_sent.append(article)
                vec_features, labels = cluster.clustering(all_sent, dict_file[k])
        i = 0
        for id in text["id"]:
            dict_output[id] = labels[i]
            dict_features[id] = vec_features[i]
            i += 1
        list_all = produce_output.write_cluster(dict_output, out_path)

        # similarity between documents
        list_comb, all_sim = cluster.similarity_score(list_all, dict_features)
        list_sim = produce_output.write_ranking(list_comb, all_sim, out_path)

if __name__ == "__main__":
   main(sys.argv[1:])
