#!/usr/bin/env python
import glob

def main(to_file):
    fout = open(to_file, "w")
    for file_path in glob.glob('*/evaluation.result'):
        with open(file_path) as fin:
            line = fin.read()
            print line.strip()
            fout.write(line)

    fout.close()

if __name__ == '__main__':
    main("evaluation.result")