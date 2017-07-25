'''
Created on 2014-12-4

@author: jinxueyu
'''

import sys
import time

sys.path.append('/data/recommend/classify/src/main/py')

from classification.goods_classifier.training.generate_fs import FeatureParser
from classification.goods_classifier.training.mutual_info import MultualInfoTask

if __name__ == '__main__':
    
    if len(sys.argv) != 3:
        print 'Usage: python generate_ts.py [b2c_train_set.ts] [b2c_train_set.smi]'
        sys.exit()
        
    in_data = sys.argv[1]
    smi_output_file = sys.argv[2]
    
    ts_file_path = in_data #+'.ts'    
#    generate_train_set(in_data, ts_file_path)
#    print 'generate_ts OK'
    
    fs_file_path = in_data+'.fs' 
    
    print time.localtime()
    parser = FeatureParser()
    f = parser.parse_feature_set(ts_file_path, fs_file_path)
    print time.localtime()
    print 'generate_fs OK'
    
    print time.localtime()
    task = MultualInfoTask(fs_file_path, smi_output_file)
    task.run_task()
    print time.localtime()
    print 'finish MultualInfoTask~'