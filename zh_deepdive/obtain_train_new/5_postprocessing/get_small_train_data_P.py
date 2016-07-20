import codecs
import csv
import os


#[{'first_name': 'Baked', 'last_name': 'Beans'}, {'first_name': 'Lovely', 'last_name': 'Spam'}]
def read_dict_from_csv(in_file):
    if not os.path.exists(in_file):
        return []
    with codecs.open(in_file, "r") as csvfile:
        return list(csv.DictReader(csvfile))

def main(in_file, to_file):

    fout = open(to_file, "w")

    for d in read_dict_from_csv(in_file):
        P, positive, negative = d["P"], d["positive"], d["negative"]

        if int(positive) < 5000:
            fout.write(P + "\n")

    fout.close()


if __name__ == '__main__':
    main("SPO_train_data_for_deepdive_label.statistics.csv", "P_list")