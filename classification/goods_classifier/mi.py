'''
Created on 2013-7-22

@author: jinxueyu
'''


from common.base import StringBuilder
from common.io import FileWriter, FileReader


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

    def parse_feat(self, line):
        s = {}
        arr = line.split('\t')
        s['label'] = arr[2]
        features = arr[1].split(';')

        s['features'] = set()

        # print line
        for v in features:
            if len(v) == 0:
                continue

            # print v

            v = v.split(',')
            s['features'].add(v[1])

            if v[0] == 'product':
                s['product'] = v[1]
        return s

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
        
    def run(self):
        for line in self.__reader:
            if line.startswith('#'):
                continue
            feat = self.parse_feat(line)
            self.handle(feat, label_field=self.__field)

            if self.__total % 10000 == 0:
                print self.__total
#            break

        self.__total *= 1.0
        
        label_feature_mi = {}
        for (l, fc) in self.__label_feature_count.items():            
            label_count = self.__label_count[l]        

            for f, f_c in fc.items():                                                
                co_occurrence = f_c
                try:
                    if not label_feature_mi.has_key(l):
                        label_feature_mi[l] = {}                    
                    label_feature_mi[l][f] = co_occurrence
                except Exception, e:
                    print co_occurrence, self.__total, label_count, '\n', e
        
        print 'write feature mi...'
        for item in label_feature_mi.items():
            cat = item[0]
            values = item[1]
            sb = StringBuilder(cat)
            sb.append('\t')
            l = len(values)
            c = 0
            for key, value in values.items():
                c += 1
                sb.append(key).append(':').append(value)
                if l > c:
                    sb.append(';')

            self.__writer.write(sb.to_string())
        
        for i in self.__featue_count.items():
            self.__fc_writer.write(i[0] + ',' + str(i[1]))
        
        self.__label_count['__total_count__'] = self.__total
        for i in self.__label_count.items():
            self.__lc_writer.write(i[0] + ',' + str(int(i[1])))
            
        self.close()            
        
    def close(self):
        self.__reader.close()
        self.__writer.close()
        self.__fc_writer.close()
        self.__lc_writer.close()

if __name__ == '__main__':
    i = '/data/recommend/goods-classification/train.set'
    o = i + '.smi'
    task = StatisticsTask(i, o, 'label')
    task.run()
