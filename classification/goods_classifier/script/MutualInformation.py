'''
Created on 2013-7-22

@author: jinxueyu
'''
'''
Created on 2013-6-24

@author: jinxueyu
'''
import sys
sys.path.append('D:\\workspace-py\\gouwudai-recommend')
sys.path.append('/data/recommend/script/gouwudai-recommend/src')

from com.gouwudai.recommend.base import json
from com.gouwudai.recommend.base.reader import FileReader
from com.gouwudai.recommend.base.writer import FileWriter
import math

class StatisticsTask():
    def __init__(self, input_path, out_path, field):
        self.__reader = FileReader(input_path)
        self.__writer = FileWriter(out_path)
        self.__fc_writer = FileWriter(out_path + '.fc')
        self.__lc_writer = FileWriter(out_path + '.lc')
        self.__field = field 
    
    __featue_count = {}    
    __label_count = {}        
    __label_feature_count = {}
    __reader = None
    __total = 0
    
    def __add_dict(self, key, _dict):
        if not _dict.has_key(key):
            _dict[key] = 1
        else:
            _dict[key] += 1
    
    def handle(self, feat, label_field='label', feature_field='features'):
        features = feat[feature_field]
        if feat.has_key(label_field):
            labels = feat[label_field]
        else:
            return
        
        if isinstance(labels, str):
            label = labels
            labels = [label]
            
        for label in labels:
            if label == '-1' or label == 'NA':
                return
            
            self.__add_dict(label, self.__label_count)
            
            if not self.__label_feature_count.has_key(label):
                self.__label_feature_count[label] = {}                
            label_feature_dict = self.__label_feature_count[label]
        
            for f in features:                            
                self.__add_dict(f, label_feature_dict)
                
        for f in features:                
            self.__add_dict(f, self.__featue_count)
        
        self.__total += 1
        
    def parse_feat(self, line):
        s = None
        try:
            s = json.read(line)
        except Exception, e:
            return None
        
        feature = s['feature']
        s['features'] = set()
        
        for v in feature.values():            
            for f in v:
                s['features'].add(f)
        
        if s['feature'].has_key('product'):
            s['product'] = s['feature']['product']        
        return s
        
    def run(self):        
        while self.__reader.hasNext():
            lines = self.__reader.next()
            
            for line in lines:
                feat = self.parse_feat(line)
                self.handle(feat, label_field=self.__field)                            
                
                if self.__total % 10000 == 0:
                    print self.__total
#            break
        
        print self.__total 
        self.__total *= 1.0
        
        label_feature_mi = {}
        for (l, fc) in self.__label_feature_count.items():            
            label_count = self.__label_count[l]        

            for f, f_c in fc.items():                                                
                co_occurrence = f_c
                               
#                featue_count = self.__featue_count[f]
#                p = co_occurrence / self.__total 
                 
                try:
                    if not label_feature_mi.has_key(l):
                        label_feature_mi[l] = {}                    
                    label_feature_mi[l][f] = co_occurrence
# + " " + l + ' ' + str(label_count) + ' ' + f + ' ' + str(featue_count) + ' ' + str(count)
                except Exception, e:
                    print co_occurrence , self.__total , label_count , '\n', e                
        
        print 'write feature mi...'
        for i in label_feature_mi.items():
            s = json.write(i)
            self.__writer.write(s)
        
        for i in self.__featue_count.items():
            t = (i[0], i[1])
            s = json.write(t)
            self.__fc_writer.write(s)                    
        
        self.__label_count['__total_count__'] = self.__total
        for i in self.__label_count.items():
            t = (i[0], i[1])
            s = json.write(t)
            self.__lc_writer.write(s)
            
        self.close()            
        
    def close(self):
        self.__reader.close()
        self.__writer.close()
        self.__fc_writer.close()
        self.__lc_writer.close()

if __name__ == '__main__':
    i = '/data/recommend/classify/tmall_train_set.fs'
    o = i + '.smi'
    task = StatisticsTask(i, o, 'label')
    task.run()
 
    
#    i = '/data/recommend/classify/tmall_train_set.fs'
#    o = i + '.product.mi'
#    task = MutualInformationTask(i, o, 'product')
#    task.run()
