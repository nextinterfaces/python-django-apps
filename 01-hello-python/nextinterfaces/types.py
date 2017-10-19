
# Tuple immutable type
tu = (23, 'abc' , 4.56, (2,3), 'def')
# String immutable type
st = 'Hi Next Interfaces'
# List mutable type
ls = ['a', 'b', 1]

print tu
print st
print ls

print tu[1]
print st[1]
print ls[1]

# tu[1] = 'AAA' # TypeError: 'tuple' object does not support item assignment
# st[1] = 'AAA' # TypeError: 'str' object does not support item assignment
ls[1] = 'AAA'

print ls

dictionary = {'key1':'next', 'key2':'interfaces'}

print 'dictionary is: ' + dictionary['key1'] + ' ' + dictionary['key2']

def sample_function(x,y):
  return x*y

sample_function(1,2)


def sample_function2(a, b, c=30, d=400):
  print a, b, c, d

sample_function2(1,2)