'''
Created on 2014-12-8

@author: jinxueyu
'''
import sys
import time

from classification.goods_classifier.classifier import MIClassifier, dict_key_add
from classification.goods_classifier.training.feature_util import parse_label_url_title_property_features


if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print 'Usage: python classifier.py [smi_file] [test_fs_file]'
        sys.exit()
    smi_file_path = sys.argv[1]
    test_fs_file_path = sys.argv[2]
    fc_file_path = smi_file_path + '.fc'
    lc_file_path = smi_file_path + '.lc'
    statistic_file = test_fs_file_path + '.statistic'
    statistic_error_file = test_fs_file_path + '.classify_error'
    print time.localtime()
    classifier = MIClassifier(fc_file_path, lc_file_path, smi_file_path)
    print 'finish load MIClassifier'
    print time.localtime()
    
    reader = open(test_fs_file_path, 'r')
    statistic_writer = open(statistic_file, 'w')
    error_writer = open(statistic_error_file, 'w')
    label_totalcount_dict = {}
    label_correctcount_dict = {}
    error_lines = []
    
    LINE_SIZE = 1000000
    while True:
        # # read as more as 10w lines
        print 'start to read as more as ' + str(LINE_SIZE) + ' lines'
        print time.localtime()
        line_list = []
        while True:
            line = reader.readline()
            if not line:
                break
            line_list.append(line)
            if len(line_list) == LINE_SIZE:
                break
        print 'start to classify ' + str(LINE_SIZE) + ' lines'
        print time.localtime()
        # # classify 10w lines
        if len(line_list) > 0:
            for line in line_list:
                label, url, title, property_features = parse_label_url_title_property_features(line)
                result = classifier.classify_by_feature_doc(property_features)
                if str(label) == str(result):
                    dict_key_add(label_totalcount_dict, label)
                    dict_key_add(label_correctcount_dict, label)
                else:
                    error_lines.append(str(label) + '\t' + str(result) + '\t' + title + '\t' + url)
                    dict_key_add(label_totalcount_dict, label)       
        else:
            break
    # ## write error-statistic file
    for error_line in error_lines:
        error_writer.write(error_line + '\n')
    error_writer.flush()
    error_writer.close()
    # ## write statistic file
    statistic_writer.write('label\t' + 'total_count\t' + 'correct_count\t' + 'accuracy\n')
    all_count = 0
    all_correct = 0
    for label, total_count in label_totalcount_dict.items():
        correct_count = 0
        if label_correctcount_dict.has_key(label):
            correct_count = label_correctcount_dict[label]
        accuracy = 1.0 * correct_count / total_count
        statistic_writer.write(str(label) + '\t' + str(total_count) + '\t' + str(correct_count) + '\t' + str(accuracy) + '\n')
        
        all_count += total_count
        all_correct += correct_count
    
    all_accuracy = 1.0 * all_correct / all_count
    statistic_writer.write(str(all_count) + '\t' + str(all_correct) + '\t' + str(all_accuracy))
    statistic_writer.flush()
    statistic_writer.close()
    
    print time.localtime()
    print 'finish~'