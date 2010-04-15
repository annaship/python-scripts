Python 2.6.4 (r264:75706, Jan 19 2010, 11:48:04) 
[GCC 4.2.1 (Apple Inc. build 5646)] on darwin
Type "copyright", "credits" or "license()" for more information.

    ****************************************************************
    Personal firewall software may warn about the connection IDLE
    makes to its subprocess using this computer's internal loopback
    interface.  This connection is not visible on any external
    interface and no data is sent to or received from the Internet.
    ****************************************************************
    
IDLE 2.6.4      
>>> import nltk
>>> a = ["an", 'apple', "on", 'a', 'plate']
>>> nltk.pos_tag(a)
[('an', 'DT'), ('apple', 'NN'), ('on', 'IN'), ('a', 'DT'), ('plate', 'NN')]

>>> from random import randint
>>> b = randint(1,24)
>>> import random
>>> a
['an', 'apple', 'on', 'a', 'plate']
>>> b = random.choice(a)
>>> b
'a'
>>> b = random.choice(a)
>>> b
'apple'
>>> len(a)
5
>>> while found < len_a:
	try:
		a_word = random.choice(a);
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1

>>> for x in words:
	print x;

an
on
a
apple
plate

>>> arr = []
>>> while found < len_a:
	try:
		a_word = random.choice(a);
		arr.append(a_word);
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1

>>> while found < len_a:
	a_word = random.choice(a);
	arr.append(a_word);
	if not words.index(a_word):
		words.append(a_word);
		found += 1

>>> while i < 10:
	aa = random.choice(a);
	print aa;
	i += 1

apple
an
on
on
a
apple
a
plate
on
a
>>> while found < len_a:
	try:
		a_word = random.choice(a);
		print a_word;
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1

>>> while found < len_a:
	a_word = random.choice(a);
	print a_word;
	if not words.index(a_word):
		words.append(a_word);
		found += 1

>>> found = 0
>>> words = []
>>> a
['an', 'apple', 'on', 'a', 'plate']
>>> while found < len_a:
	try:
		a_word = random.choice(a);
		print a_word;
		words.index(a_word);
	except ValueError:
		words.append(a_word);
		found += 1

apple
apple
0
plate
apple
0
on
apple
0
an
an
3
apple
0
a
>>> for x in words:
	print x;

apple
plate
on
an
a
>>> in_file = open("/Users/anna/work/texts/shell_index/clean_index/1/clean_index-uniq-ok1.txt", "r")
>>> text = in_file.read()
>>> in_file.close()
>>> print text
Abra
Abra aequalis
...

>>> names_list = open("/Users/anna/work/texts/shell_index/clean_index/1/clean_index-uniq-ok1.txt", "r")
>>> my_set = set(names_list)
>>> my_set
set(['Volsella demissa\n', 'Solenidae\n', 'Trophonopsis lasius\n', 'Tachyrhynchus reticulatum\n', 'Glaucus marina\n'])
>>> 


 def my_random_list(my_list):
	name = ""
	found = 0
	random_names = []
	while len(random_names) < len(my_list):
		try:
			name = random.choice(my_list);
			random_names.index(name);
		except ValueError:
			random_names.append(name);
			found += 1
	return random_names

>>> my_r_list = my_random_list(my_list)
>>> len(my_r_list)
2848
>>> out_file = open('/Users/anna/work/random_names.txt', 'w')
>>> my_string = "".join(my_r_list)
>>> out_file.write(my_string)
>>>

aa = list(my_set)
-------

>>> tf_diff_man = open("/Users/anna/work/texts/diff/new-tf-diff-man.txt", "r")
>>> tf_diff_man_set = set(tf_diff_man)
>>> len(tf_diff_man_set)
361
>>> utf_diff_man = open("/Users/anna/work/texts/diff/utf-diff-man-list.txt", "r")
>>> utf_diff_man_set = set(utf_diff_man)
>>> len(utf_diff_man_set)
323
>>> utf_minus_tf = utf_diff_man_set.difference(tf_diff_man_set)
>>> len(utf_minus_tf)
