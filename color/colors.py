#!/usr/bin/env python

codes = [
    (3,0), 'black',
    (3,1), 'red',
    (3,2), 'green',
    (3,3), 'yellow',
    (3,4), 'blue',
    (3,5), 'magenta',
    (3,6), 'cyan',
    (3,7), 'white',
    (3,9), 'default',
    (4,0), 'black',
    (4,1), 'red',
    (4,2), 'green',
    (4,3), 'yellow',
    (4,4), 'blue',
    (4,5), 'magenta',
    (4,6), 'cyan',
    (4,7), 'white',
    (4,9), 'default'
]

#####################################
# Display them!
#####################################

print len(codes)

for i in range(len(codes)//2):
    k = codes[2*i]; v = codes[2*i+1]
    print '\x1b[%s%sm %s'%(k[0],k[1],v)
