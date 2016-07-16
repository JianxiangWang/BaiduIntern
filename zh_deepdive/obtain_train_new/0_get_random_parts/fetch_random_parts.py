import random, os

INPUT_DIR = "/app/ps/spider/kg-value/lihe08/SPOMining/trainData_prepare/dataSourcePage_layer_1_2_depparser"
OUTPUT_DIR = "/app/ps/spider/kg-value/wangjianxiang01/data/SPO_train_data_depparser"

# mkdir
cwd = "hadoop fs -rmr %s" % (OUTPUT_DIR)
os.system(cwd)
cwd = "hadoop fs -mkdir %s" % (OUTPUT_DIR)
os.system(cwd)

# sample 100 parts
wanted = random.sample(range(0, 1000), 100)

for i, idx in enumerate(wanted):
    part_address = "%s/part-%05d.gz" % (INPUT_DIR, idx)
    # copy
    cmd = "hadoop fs -cp %s %s/" % (part_address, OUTPUT_DIR)
    print "%d: %s" % (i, cmd)
    os.system(cmd)
