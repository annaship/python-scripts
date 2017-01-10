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

inters_0 = collect_hits_0(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
inters_1 = collect_hits_1(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)
inters_2 = collect_hits_2(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)

print(timeit.timeit("collect_hits_0(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_0, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))

print(timeit.timeit("collect_hits_2(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)", setup="from __main__ import collect_hits_2, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))


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
    
    
    for i in xrange(1000000):    
        start = time.time()
        Process(target=collect_hits_01, args=(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position, return_dict)).start()
        Process(target=collect_hits_02, args=(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position, return_dict)).start()
        dur = time.time() - start
        durs.append(dur)
    print "average time {} us".format(sum(durs) / len(durs) * 1000000)


    for i in xrange(1000000):    
        start = time.time()
        collect_hits_2(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position)``
        durs.append(dur)
    print "average time {} us".format(sum(durs) / len(durs) * 1000000)
    


    
    a = []
    a.append(sample_name + "," + str(return_dict['allelic_count']) + "," + str(return_dict['non_allelic_count']))
    a


print(timeit.timeit("Process(target=collect_hits_01, args=(Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position, return_dict)).start()", setup="from __main__ import collect_hits_0, Av_T0, pairs_dict, sample_name, coverage_dict, min_cov_value, table_position", number=10000000))
