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
>>> nltk.app.rdparser()
[('under',)]
[('with',)]
[('in',)]
[('under',), ('with',)]
[('ate',)]
[('saw',)]
[('dog',)]
[('telescope',)]
[('park',)]
[('dog',), ('telescope',)]
[('man',)]
[('park',), ('dog',), ('telescope',)]
[('the',)]
[('a',)]
[(V, NP)]
[(V,)]
[(V, NP, PP)]
[(V, NP), (V,)]
[(Det, N, PP)]
[(Det, N)]
S [(NP, VP)]
NP [(Det, N, PP), (Det, N)]
VP [(V, NP, PP), (V, NP), (V,)]
PP [(P, NP)]
NP [('I',)]
Det [('the',), ('a',)]
N [('man',), ('park',), ('dog',), ('telescope',)]
V [('ate',), ('saw',)]
P [('in',), ('under',), ('with',)]

Warning (from warnings module):
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/nltk/draw/cfg.py", line 355
    elif match.group() in ('->', self.ARROW): tag = 'arrow'
UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal

Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    nltk.app.rdparser()
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/nltk/app/rdparser_app.py", line 887, in app
    RecursiveDescentApp(grammar, sent).mainloop()
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/nltk/app/rdparser_app.py", line 615, in mainloop
    self._top.mainloop(*args, **kwargs)
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/lib-tk/Tkinter.py", line 1017, in mainloop
    self.tk.mainloop(n)
KeyboardInterrupt



>>> nltk.app.srparser
<function app at 0x103fb8758>
>>> nltk.app.srparser()

Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    nltk.app.srparser()
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/nltk/app/srparser_app.py", line 804, in app
    ShiftReduceApp(grammar, sent).mainloop()
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/nltk/app/srparser_app.py", line 519, in mainloop
    self._top.mainloop(*args, **kwargs)
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/lib-tk/Tkinter.py", line 1017, in mainloop
    self.tk.mainloop(n)
KeyboardInterrupt
>>> nltk.app.chankparser()

Traceback (most recent call last):
  File "<pyshell#4>", line 1, in <module>
    nltk.app.chankparser()
AttributeError: 'module' object has no attribute 'chankparser'
>>> nltk.app.chunkparser()

Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    nltk.app.chunkparser()
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/nltk/app/chunkparser_app.py", line 1253, in app
    RegexpChunkApp().mainloop()
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/nltk/app/chunkparser_app.py", line 1250, in mainloop
    self.top.mainloop(*args, **kwargs)
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/lib-tk/Tkinter.py", line 1017, in mainloop
    self.tk.mainloop(n)
KeyboardInterrupt
>>> gmr = """
<IN><NN.*>|<IN><PRP.*>
"""
>>> p = nltk.RegexpParser(gmr)

Traceback (most recent call last):
  File "<pyshell#9>", line 1, in <module>
    p = nltk.RegexpParser(gmr)
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/nltk/chunk/regexp.py", line 1111, in __init__
    self._parse_grammar(grammar, top_node, trace)
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/nltk/chunk/regexp.py", line 1147, in _parse_grammar
    rules.append(RegexpChunkRule.parse(line))
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/nltk/chunk/regexp.py", line 378, in parse
    raise ValueError('Illegal chunk pattern: %s' % rule)
ValueError: Illegal chunk pattern: <IN><NN.*>|<IN><PRP.*>
>>> gmr = """
CP : <IN><NN.*>|<IN><PRP.*>
"""
>>> 
>>> p = nltk.RegexpParser(gmr)

Traceback (most recent call last):
  File "<pyshell#12>", line 1, in <module>
    p = nltk.RegexpParser(gmr)
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/nltk/chunk/regexp.py", line 1111, in __init__
    self._parse_grammar(grammar, top_node, trace)
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/nltk/chunk/regexp.py", line 1147, in _parse_grammar
    rules.append(RegexpChunkRule.parse(line))
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/nltk/chunk/regexp.py", line 378, in parse
    raise ValueError('Illegal chunk pattern: %s' % rule)
ValueError: Illegal chunk pattern: <IN><NN.*>|<IN><PRP.*>
>>> gmr
'\nCP : <IN><NN.*>|<IN><PRP.*>\n'
>>> gmr = """
CP: {<IN><NN.*>|<IN><PRP.*>}
"""
>>> gmr
'\nCP: {<IN><NN.*>|<IN><PRP.*>}\n'
>>> p = nltk.RegexpParser(gmr)
>>> s = "A lion lives 15 years in captivity"
>>> ptg = nltk.pos_tag(nltk.word_tokenize(s))
>>> ptg
[('A', 'DT'), ('lion', 'NN'), ('lives', 'VBZ'), ('15', 'CD'), ('years', 'NNS'), ('in', 'IN'), ('captivity', 'NN')]
>>> tt = p.parse(ptg)
>>> tt
Tree('S', [('A', 'DT'), ('lion', 'NN'), ('lives', 'VBZ'), ('15', 'CD'), ('years', 'NNS'), Tree('CP', [('in', 'IN'), ('captivity', 'NN')])])
>>> 
