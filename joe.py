# Hi Peeps,
# I have a python function that looks through millions of key value relationships in a dictionary and tries to find matching keys/values in other dicts.  If it finds a mat,, it will add 1 to a counter..  It looks like this.
# 

Av_T0 = {'key1':'1', 'key2':'20', 'key3':'300'}
pairs_dict = {'key1':'1', 'key4':'4000', 'key3':'300'}
sample_name = 'Av11_pair_one'
coverage_dict = {'key1':['1', '10'], 'key3':['300', '3'], 'key5':'50000'}
min_cov_value = 10
table_position = 0

def collect_hits_0(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
    for key in pairs_dict.keys():
        if coverage_dict.has_key(key) and Av_T0.has_key(key) and int(coverage_dict[key][table_position]) > min_cov_value:
            allelic_count += 1
    for key in coverage_dict.keys():
        if key not in pairs_dict.keys() and Av_T0.has_key(key) and int(coverage_dict[key][table_position]) > min_cov_value:
            non_allelic_count += 1
    
    a.append(sample_name + "," + str(allelic_count) + "," + str(non_allelic_count))
    return a

def collect_hits_01(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    for key in pairs_dict.keys():
        if coverage_dict.has_key(key) and Av_T0.has_key(key) and int(coverage_dict[key][table_position]) > min_cov_value:
            allelic_count += 1
    return allelic_count

def collect_hits_02(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    non_allelic_count = 0
    for key in coverage_dict.keys():
        if key not in pairs_dict.keys() and Av_T0.has_key(key) and int(coverage_dict[key][table_position]) > min_cov_value:
            non_allelic_count += 1
    return non_allelic_count

a = []



def collect_hits_1(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
    for key in pairs_dict.keys():
        if coverage_dict.has_key(key) and Av_T0.has_key(key):
            allelic_count += 1
    for key in coverage_dict.keys():
        if key not in pairs_dict.keys() and Av_T0.has_key(key):
            non_allelic_count += 1
    
    a.append(sample_name + "," + str(allelic_count) + "," + str(non_allelic_count))
    return a


# Could you give me an idea of how I might parallelize this function??
# Thanks,
# Joe

def collect_hits_2(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
    
    pairs_dict_keys    = set(pairs_dict.keys())
    coverage_dict_keys = set(coverage_dict.keys())
    Av_T0_keys         = set(Av_T0.keys())
    
    allelic = set(pairs_dict_keys).intersection(coverage_dict_keys).intersection(Av_T0_keys)
    
    allelic_count =  [k for k in allelic if (int(coverage_dict[k][table_position]) > min_cov_value)]
    
    
    # print allelic
    # for k in allelic:
    #     print k
    #     print coverage_dict[k][table_position]
    #     print int(coverage_dict[k][table_position]) > min_cov_value
    
    
    # allelic_count = len(allelic)
    a.append(sample_name + "," + str(len(allelic_count)) + "," + str(non_allelic_count))
    
    # return a    
    return a

inters_0 = collect_hits_0(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
inters_1 = collect_hits_1(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
inters_2 = collect_hits_2(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)

print(timeit.timeit("collect_hits_0(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_0, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))

print(timeit.timeit("collect_hits_2(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_2, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))


from multiprocessing import Pool
pool = Pool()
result1 = pool.apply_async(solve1, [A])    # evaluate "solve1(A)" asynchronously
result2 = pool.apply_async(solve2, [B])    # evaluate "solve2(B)" asynchronously
answer1 = result1.get(timeout=10)
answer2 = result2.get(timeout=10)