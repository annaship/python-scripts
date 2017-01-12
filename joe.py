# Hi Peeps,
# I have a python function that looks through millions of key value relationships in a dictionary and tries to find matching keys/values in other dicts.  If it finds a mat,, it will add 1 to a counter..  It looks like this.
# 
---
Av_T0 = {'key1':'1', 'key2':'20', 'key3':'300'}
pairs_dict = {'key1':'1', 'key4':'4000', 'key3':'300'}
sample_name = 'Av11_pair_one'
coverage_dict = {'key1':['1', '10'], 'key3':['300', '3'], 'key5':'50000'}
min_cov_value = 10
table_position = 0

---
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
    
def collect_hits_0a(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
    for key in pairs_dict.keys():
        if key in coverage_dict.keys() and key in Av_T0.keys() and int(coverage_dict[key][table_position]) > min_cov_value:
            allelic_count += 1
    for key in coverage_dict.keys():
        if key not in pairs_dict.keys() and key in Av_T0.keys() and int(coverage_dict[key][table_position]) > min_cov_value:
            non_allelic_count += 1
    
    a.append(sample_name + "," + str(allelic_count) + "," + str(non_allelic_count))
    return a

def collect_hits_01(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position, return_dict):
    allelic_count = 0
    for key in pairs_dict.keys():
        if coverage_dict.has_key(key) and Av_T0.has_key(key) and int(coverage_dict[key][table_position]) > min_cov_value:
            allelic_count += 1
    return_dict['allelic_count'] = allelic_count    
    return allelic_count

def collect_hits_02(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position, return_dict):
    non_allelic_count = 0
    for key in coverage_dict.keys():
        if key not in pairs_dict.keys() and Av_T0.has_key(key) and int(coverage_dict[key][table_position]) > min_cov_value:
            non_allelic_count += 1
    return_dict['non_allelic_count'] = non_allelic_count
    return non_allelic_count

a = []
a.append(sample_name + "," + str(collect_hits_01(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)) + "," + str(collect_hits_02(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)))
a

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
    
def collect_hits_2a(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
    
    pairs_dict_keys    = set(pairs_dict.keys())
    coverage_dict_keys = set(coverage_dict.keys())
    Av_T0_keys         = set(Av_T0.keys())
    coverage_dict_ok_keys = [k for k, v in coverage_dict.items() for x in v if int(x) > int(min_cov_value)]
    
    allelic = set(pairs_dict_keys).intersection(coverage_dict_keys).intersection(Av_T0_keys).intersection(coverage_dict_ok_keys)
    print "allelic = "
    print allelic
    allelic_count =  len(allelic)
    
    non_allelic_count = 0 
    #TODO: not in! set(pairs_dict_keys).intersection(coverage_dict_keys).intersection(Av_T0_keys).intersection(coverage_dict_ok_keys)
    
    """
    for key in pairs_dict.keys():
        if coverage_dict.has_key(key) and Av_T0.has_key(key) and int(coverage_dict[key][table_position]) > min_cov_value:
            allelic_count += 1
    for key in coverage_dict.keys():
        if key not in pairs_dict.keys() and Av_T0.has_key(key) and int(coverage_dict[key][table_position]) > min_cov_value:
    """
    a.append(sample_name + "," + str(len(allelic_count)) + "," + str(non_allelic_count))
    
    # return a    
    return a
        
def collect_hits_3(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
    for key in pairs_dict.keys():
        if key in coverage_dict.keys() and key in Av_T0.keys() and int(coverage_dict[key][table_position]) > min_cov_value:
            allelic_count += 1
    for key in coverage_dict.keys():
        if key not in pairs_dict.keys() and key in Av_T0.keys() and int(coverage_dict[key][table_position]) > min_cov_value:
            non_allelic_count += 1
    
    a.append(sample_name + "," + str(allelic_count) + "," + str(non_allelic_count))
    
    return a

def collect_hits_4(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
    allelic_count_l = [key for key in pairs_dict.keys() if key in coverage_dict.keys() and key in Av_T0.keys() and int(coverage_dict[key][table_position]) > min_cov_value]
    allelic_count = len(allelic_count_l)
    
    non_allelic_count_l = [key for key in coverage_dict.keys() if key not in pairs_dict.keys() and key in Av_T0.keys() and int(coverage_dict[key][table_position]) > min_cov_value]
    non_allelic_count = len(non_allelic_count_l)
    
    a.append(sample_name + "," + str(allelic_count) + "," + str(non_allelic_count))
    
    return a

*) todo create subdict first by int(coverage_dict[key][table_position]) > min_cov_value

    # coverage_dict_ok = {k: coverage_dict[k] for k in coverage_dict.keys() if }
    # dictionary['C1'] = [x+1 for x in dictionary['C1']]
    #
    # coverage_dict_ok = {k: v for k, v in coverage_dict.items() for x in v if int(x) > int(min_cov_value)}
    # >>> for k, v in coverage_dict.items():
    # ...     for x in v:
    # ...             if int(x) > int(min_cov_value):
    # ...                     print "URA"
    # ...                     print x
    # -----
    
    coverage_dict_ok_keys = []
    """
    for tag in tags:
        for entry in entries:
            if tag in entry:
                result.extend(entry)
    
    [entry for tag in tags for entry in entries if tag in entry]
    for k, v in coverage_dict.items():
        for x in v:
                if int(x) > int(min_cov_value):
                        coverage_dict_ok_keys.append(k)
    
    """
    
def collect_hits_5(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
                   
    coverage_dict_ok_keys = [k for k, v in coverage_dict.items() for x in v if int(x) > int(min_cov_value)]
    # allelic_count_l = [key for key in pairs_dict.keys() if key in coverage_dict.keys() and key in Av_T0.keys() and key in coverage_dict_ok_keys]
    # allelic_count = len(allelic_count_l)
    
    allelic = set(pairs_dict_keys).intersection(coverage_dict_keys).intersection(Av_T0_keys).intersection(coverage_dict_ok_keys)
    # print "allelic = "
    # print allelic
    allelic_count =  len(allelic)
    
    non_allelic_count_l = [key for key in coverage_dict.keys() if key not in pairs_dict.keys() and key in Av_T0.keys() and key in coverage_dict_ok_keys]
    non_allelic_count = len(non_allelic_count_l)
    
    a.append(sample_name + "," + str(allelic_count) + "," + str(non_allelic_count))
    return a

def collect_hits_6(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position):
    allelic_count = 0
    a = []
    non_allelic_count = 0
    
    coverage_dict_ok_keys = [k for k, v in coverage_dict.items() for x in v if int(x) > int(min_cov_value)]
    pairs_dict_keys    = set(pairs_dict.keys())
    coverage_dict_keys = set(coverage_dict.keys())
    Av_T0_keys         = set(Av_T0.keys())
    
    for key in set(coverage_dict_ok_keys).intersection(Av_T0_keys).intersection(coverage_dict_keys):
        if key in pairs_dict_keys:
            allelic_count += 1
        if key not in pairs_dict_keys: 
            non_allelic_count += 1
            
    a.append(sample_name + "," + str(allelic_count) + "," + str(non_allelic_count))
    return a


inters_0 = collect_hits_0(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
inters_1 = collect_hits_1(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
inters_2 = collect_hits_2(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
inters_3 = collect_hits_3(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
inters_4 = collect_hits_4(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
inters_5 = collect_hits_5(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)

print(timeit.timeit("collect_hits_0(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_0, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
48.6235201359
64.53489995
58.5784578323
51.895152092
54.4317700863

print(timeit.timeit("collect_hits_0a(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_0a, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
66.6070878506
63.4970169067
62.4234759808
64.34131217

print(timeit.timeit("collect_hits_2(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_2, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
53.0215709209
54.4635019302

print(timeit.timeit("collect_hits_3(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_3, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
64.663351059

print(timeit.timeit("collect_hits_4(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_4, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
64.3443729877

print(timeit.timeit("collect_hits_5(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_5, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
158.822649956

print(timeit.timeit("collect_hits_6(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_6, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
219.051295996


from multiprocessing import Pool
pool = Pool()
result1 = pool.apply_async(collect_hits_01(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position))    # evaluate "solve1(A)" asynchronously
result2 = pool.apply_async(collect_hits_02(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position))    # evaluate "solve2(B)" asynchronously
answer1 = result1.get(timeout=10)
answer2 = result2.get(timeout=10)

args = (Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
results = pool.map(collect_hits_01(), args)
from multiprocessing import Process


if __name__ == '__main__':
    Process(target=collect_hits_01(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)).start()
    Process(target=collect_hits_02(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)).start()


if __name__ == '__main__':
    info('main line')
    p = Process(target=collect_hits_0(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position))
    p.start()
    p.join()


from multiprocessing import Process

def f(name, text):
    print 'hello', name, text

if __name__ == '__main__':
    p = Process(target=f, args=('bob', 'UUUU',))
    p.start()
    p.join()


if __name__ == '__main__':
    p = Process(target=collect_hits_01, args=(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position,))
    p.start()
    p.join()

from multiprocessing import Process, Manager
import time

if __name__ == '__main__':
    manager = Manager()
    return_dict = manager.dict()
    durs = []
    
    for i in xrange(1000):    
        start = time.time()
        Process(target=collect_hits_01, args=(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position, return_dict)).start()
        Process(target=collect_hits_02, args=(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position, return_dict)).start()
        dur = time.time() - start
        durs.append(dur)
    print "average time {} us".format(sum(durs) / len(durs) * 1000000)
    
    for i in xrange(1000):    
        start = time.time()
        collect_hits_0(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
        dur = time.time() - start
        durs.append(dur)
    print "average time {} us".format(sum(durs) / len(durs) * 1000000)
    
    
    
    a = []
    a.append(sample_name + "," + str(return_dict['allelic_count']) + "," + str(return_dict['non_allelic_count']))
    a


print(timeit.timeit("Process(target=collect_hits_01, args=(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position, return_dict)).start()", setup="from __main__ import collect_hits_0, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
=====


pairs_dict = {'GSADVT00027351001_1894': ['1894', 'T', 'A'], 'GSADVT00027990001_479': ['479', 'C', 'T'], 'GSADVT00005150001_2582': ['2582', 'SNV', '1', 'T', 'G', '', 'Heterozygous', '46', '109', '42.2018348624', '0.4565217391', '37.7173913043'], 'GSADVT00041852001_2043': ['2043', 'SNV', '1', 'G', 'A', '', 'Heterozygous', '4', '14', '28.5714285714', '0.25', '37.5']}
Av_T0 = { 'GSADVT00005150001_2582': ['2582', 'SNV', '1', 'T', 'G', '', 'Heterozygous', '46', '109', '42.2018348624', '0.4565217391', '37.7173913043'], 'GSADVT00041852001_2043': ['2043', 'SNV', '1', 'G', 'A', '', 'Heterozygous', '4', '14', '28.5714285714', '0.25', '37.5']}
'Av11_pair_one' = text that I append to output
coverage_dict = {'GSADVT00000104001_410': ['15', '8', '6', '3', '2', '6', '1', '0', '2', '14', '14', '3'], 'GSADVT00000102001_2178': ['0', '1', '0', '1', '0', '3', '1', '0', '0', '4', '1', '4'], 'GSADVT00005150001_2582': ['2582', 'SNV', '1', 'T', 'G', '', 'Heterozygous', '46', '109', '42.2018348624', '0.4565217391', '37.7173913043'], 'GSADVT00041852001_2043': ['2043', 'SNV', '1', 'G', 'A', '', 'Heterozygous', '4', '14', '28.5714285714', '0.25', '37.5']}


===
multi 01 & 02
average time 6805.69720268 us
average time 6511.41142845 us
0
average time 3262.75098324 us
