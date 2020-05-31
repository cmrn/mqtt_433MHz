from collections import Sequence, Iterable
from functools import reduce

class Topic(Sequence):
  def __init__(self, *argv):
    if len(argv) > 1:
      items = tuple(reduce((lambda a, b: Topic(a) + Topic(b)), argv))

    arg = argv[0]
    if isinstance(arg, Topic):
      items = arg.data
    elif isinstance(arg, basestring):
      items = str(arg).split('/')
    elif isinstance(arg, Iterable):
      items = arg
    else:
      raise TypeError("Can't convert %s to Topic" % arg.__class__.__name__)

    self.data = tuple(item for item in items if item)

  def split(self, *argv):
    return str(self).split(*argv)

  def __str__(self):
      return '/'.join(self.data)

  def __repr__(self):
    return "%s (%r)" % (self.__class__, self.__str__())

  def __add__(self, other):
    return Topic(self.data + Topic(other).data)

  def __getitem__(self, idx):
    return self.data[idx]

  def __len__(self):
    return len(self.data)
