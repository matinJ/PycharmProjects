'''
Created on 2015-1-19

@author: jinxueyu
'''
import sys
import os
sys.path.append('/data/recommend/classify/src/main/py')

from classification.goods_classifier.classifier import CompositiveClassifier
from classification.goods_classifier.training.generate_fs import FeatureParser


def load_cat_map():

    cat_dict = {}
    cat_map_reader = open(os.path.split(os.path.realpath(__file__))[0]+'/../../data/tag_map', 'r')
    while True:
        cat_line = cat_map_reader.readline()

        if not cat_line:
            break

        cat_line = cat_line.rstrip('\n')
        cat_arr = cat_line.split('\t')

        cat_dict[cat_arr[0]] = cat_arr[1]

    cat_map_reader.close()

    return cat_dict

if __name__ == '__main__':

    cat_dict = load_cat_map()

    classifier = CompositiveClassifier()
    parser = FeatureParser()
    pv_dict = {}
    reader = open('/data/recommend/classify/goods-rank/part-r-00001', 'r')
    writer = open('/data/recommend/classify/goods-rank/training_set', 'w')
    
    count = 0
    while True:
        
        if count % 10000 == 0:
            print '##########', count
            
        count += 1
            
        line = reader.readline()
        if not line:
            break
        
#        id,name,ourl,catid,cid,shopName,pv,price
        arr = line.split('\t')
        gid = arr[0]
        title = arr[1]
        url = arr[2]
        
#        if url.find('taobao.com') > 0:
#            continue
        
        shop_name = arr[5]
        pv = int(arr[6])
        
        feat_doc = parser.parse_feature(title, url)  
        if feat_doc is None:
            continue      
        
        if not pv_dict.has_key(pv):
            pv_dict[pv] = [0,url]
        
        pv_dict[pv][0] += 1
        cat = classifier.classify(url, 'None', title)

        if cat is not None and cat in cat_dict:
            cat = cat_dict[cat]
        
        text = ''
        for k, v in feat_doc.items():
            if k not in ['product', 'brand']:
                continue
            text += k+'\t'+','.join(v)+'\t'
                
        text += 'cat\t'+str(cat)+'\t'+'shop\t'+shop_name+'\tpv\t'+str(pv)
        writer.write(text)
        writer.write('\n')
                
    reader.close()
    writer.close()
    
    for k, v in pv_dict.items():
        print k, v[0], v[1]