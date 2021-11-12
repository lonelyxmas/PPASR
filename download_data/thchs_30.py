import argparse
import os
import functools
from utility import download, unpack
from utility import add_arguments, print_arguments

DATA_URL = 'https://openslr.magicdatatech.com/resources/18/data_thchs30.tgz'
MD5_DATA = '2d2252bde5c8429929e1841d4cb95e90'

parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)
parser.add_argument("--target_dir",
                    default="../dataset/audio/",
                    type=str,
                    help="存放音频文件的目录 (默认: %(default)s)")
parser.add_argument("--annotation_text",
                    default="../dataset/annotation/",
                    type=str,
                    help="存放音频标注文件的目录 (默认: %(default)s)")
args = parser.parse_args()


def create_annotation_text(data_dir, annotation_path):
    if not os.path.exists(annotation_path):
        os.makedirs(annotation_path)
    print('Create THCHS-30 annotation text ...')
    f_train = open(os.path.join(annotation_path, 'thchs_30.txt'), 'w', encoding='utf-8')
    if not os.path.exists(os.path.join(annotation_path, 'test.txt')):
        f_test = open(os.path.join(annotation_path, 'test.txt'), 'w', encoding='utf-8')
    else:
        f_test = open(os.path.join(annotation_path, 'test.txt'), 'a', encoding='utf-8')
    data_types = ['train', 'dev']
    for type in data_types:
        for file in os.listdir(os.path.join(data_dir, type)):
            if '.trn' in file:
                file = os.path.join(data_dir, type, file)
                with open(file, 'r', encoding='utf-8') as f:
                    line = f.readline()
                    line = ''.join(line.split())
                with open(os.path.join(data_dir, type, line), 'r', encoding='utf-8') as f:
                    line = f.readline()
                    line = ''.join(line.split())
                f_train.write(file[3:-4] + '\t' + line + '\n')
    for file in os.listdir(os.path.join(data_dir, 'test')):
        if '.trn' in file:
            file = os.path.join(data_dir, 'test', file)
            with open(file, 'r', encoding='utf-8') as f:
                line = f.readline()
                line = ''.join(line.split())
            with open(os.path.join(data_dir, 'test', line), 'r', encoding='utf-8') as f:
                line = f.readline()
                line = ''.join(line.split())
            f_test.write(file[3:-4] + '\t' + line + '\n')
    f_train.close()


def prepare_dataset(url, md5sum, target_dir, annotation_path):
    """Download, unpack and create manifest file."""
    data_dir = os.path.join(target_dir, 'data_thchs30')
    if not os.path.exists(data_dir):
        filepath = download(url, md5sum, target_dir)
        unpack(filepath, target_dir)
        os.remove(filepath)
    else:
        print("Skip downloading and unpacking. THCHS-30 data already exists in %s." % target_dir)
    create_annotation_text(data_dir, annotation_path)


def main():
    print_arguments(args)
    if args.target_dir.startswith('~'):
        args.target_dir = os.path.expanduser(args.target_dir)

    prepare_dataset(url=DATA_URL,
                    md5sum=MD5_DATA,
                    target_dir=args.target_dir,
                    annotation_path=args.annotation_text)


if __name__ == '__main__':
    main()
