'''
Created on 2014-11-9

@author: mengzhejin
'''

### in fs file
ITEM_SEPERATOR = '--#####--'
PROPERTY_SEPRATOR = '--###--'
PROPERTY_WORD_SEPRATOR = '--==--'
WORD_SEPRATOR = '--||--'

# in smi file??LABEL_FEATURES_SEPRATOR = '\t'
FEATURE_BETWEEN_SEPRATOR = '--|||--'
FEATURE_COUNT_SEPRATOR = '--==--'

global int_cache
int_cache = None


def parse_int(s):
    global int_cache    
    if int_cache is None:
        int_cache = {}
    
    if not int_cache.has_key(s):
        int_cache[s] = int(s)
    return int_cache[s]

global float_cache
float_cache = None


def parse_float(s):
    global float_cache    
    if float_cache is None:
        float_cache = {}
    
    if not float_cache.has_key(s):
        float_cache[s] = float(s)
    return float_cache[s]


global str_cache
str_cache = None


def parse_str(s):
    global str_cache
    if str_cache is None:
        str_cache = {}
    
    if not str_cache.has_key(s):
        str_cache[s] = s
    
    return str_cache[s]


def join_feature_string(label, url, title, feat_doc):
    ss = label + ITEM_SEPERATOR + url + ITEM_SEPERATOR + title + ITEM_SEPERATOR
    is_first = True
    for f, wordlist in feat_doc.items():
        if is_first:
            s_temp = join_word_list(f, wordlist) 
            is_first = False
        else:
            s_temp = PROPERTY_SEPRATOR + join_word_list(f, wordlist)
        ss += s_temp
    return ss


def join_word_list(f, wordlist):
    word_list_string = f + PROPERTY_WORD_SEPRATOR
    is_first = True
    for word in wordlist:
        if is_first:
            word_list_string += word
            is_first = False
        else:
            word_list_string += WORD_SEPRATOR + word
    return word_list_string


def join_smi_string(label, feature_count_dict):
    result = label + LABEL_FEATURES_SEPRATOR
    is_first = True
    for feature, count in feature_count_dict.items():
        if is_first:
            result += feature + FEATURE_COUNT_SEPRATOR + str(count)
            is_first = False
        else:
            result += FEATURE_BETWEEN_SEPRATOR + feature + FEATURE_COUNT_SEPRATOR + str(count)
    return result

# transfer to result = {'label':'1234', 'features':[f1, f2...]}
def parse_label_and_features(complete_string):
        result = {}
        items = complete_string.split(ITEM_SEPERATOR)
        if len(items) != 4:
            return None
        label = parse_str(items[0])
        
        result['label'] = label
        result['features'] = set()
        feat_doc = items[3]
        feat_items = feat_doc.split(PROPERTY_SEPRATOR)
        for feat_item in feat_items:
            property_words = feat_item.split(PROPERTY_WORD_SEPRATOR)
            if len(property_words) != 2:
                continue
            wordsString = property_words[1]
            wordlist = wordsString.split(WORD_SEPRATOR)
            for word in wordlist:
                word = parse_str(word)
                result['features'].add(word)
            
        return result


# result = label, {property1:[f1, f2,...] , property2:[f3, f4,...]}
def parse_label_url_title_property_features(complete_string):
    items = complete_string.split(ITEM_SEPERATOR)
    if len(items) != 4:
        return None
    label = items[0]
    url = items[1]
    title = items[2]
    property_features_dict = {}
    
    property_features_string = items[3]
    property_features_items = property_features_string.split(PROPERTY_SEPRATOR)
    for property_features in property_features_items:
        property_feature_list = property_features.split(PROPERTY_WORD_SEPRATOR)
        if len(property_feature_list) != 2:
            continue
        property_field = property_feature_list[0]
        feature_list = property_feature_list[1].split(WORD_SEPRATOR)
        
        property_field = parse_str(property_field)
        
        tmp_feature_list = []
        for s in feature_list:
            s = parse_str(s)
            tmp_feature_list.append(s)                
        property_features_dict[property_field] = tmp_feature_list
    
    return label, url, title, property_features_dict


if __name__ == '__main__':
    pass