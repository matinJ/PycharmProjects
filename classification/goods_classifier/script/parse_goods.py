'''
Created on 2015-1-19

@author: jinxueyu
'''
import sys
import os
prj_path = os.path.split(os.path.realpath(__file__))[0]+'/../../../'
sys.path.append(prj_path)

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

        cat_dict[cat_arr[0]] = cat_arr[2]

    cat_map_reader.close()

    return cat_dict


def parse():

    cat_dict = load_cat_map()

    classifier = CompositiveClassifier('/data/recommend/goods-classification/model/20150410/')
    parser = FeatureParser()
    pv_dict = {}
    reader = open('/data/recommend/goods-rank/data/goods.dat', 'r')
    writer = open('/data/recommend/goods-rank/data/goods.set', 'w')
    
    count = 0
    while True:
        line = reader.readline()

        if count % 10000 == 0:
            print '##########', count
            
        count += 1
        if not line:
            break

#        id,name,ourl,catid,cid,shopName,pv,price
#         ['id','channel_id','channel_name','goods_id','goods_name','goods_url','goods_img','goods_summy','goods_title','goods_price','update_time']

        arr = line.split('\t')
        if len(arr) < 10:
            print 'parse error', line
            continue
        g_id = arr[0]
        title = arr[4]
        url = arr[5]
        sale = arr[10]
        # print g_id,title,url

#        if url.find('taobao.com') > 0:
#            continue

        shop_name = arr[1]

        feat_doc = parser.parse_feature(title, url)
        if feat_doc is None:
            continue

        cat = classifier.classify(url, 'None', title)
        if cat is not None and cat in cat_dict:
            cat = cat_dict[cat]

        text = 'id\t' + g_id + '\t'
        for k, v in feat_doc.items():
            if k not in ['product', 'brand']:
                continue
            text += k+'\t'+','.join(v)+'\t'

        text += 'cat\t'+str(cat)+'\t'+'shop\t'+shop_name+'\t'

        text += 'sale\t'+sale
        writer.write(text)
        writer.write('\n')
                
    reader.close()
    writer.close()


if __name__ == '__main__':
    parse()