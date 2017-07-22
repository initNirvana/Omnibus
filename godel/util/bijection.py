import collections


class Bijection:
  def __init__(self, mapping):
    inverse = {}
    for k, v in mapping.items():
      if v in inverse:
        raise ValueError("duplicate key '{0}' found".format(v))
      inverse[v] = k
    self._mapping = dict(mapping)
    self._inverse = inverse

  def __len__(self):
    return len(self.mapping)

  @property
  def mapping(self):
    return self._mapping

  @property
  def inverse(self):
    return self._inverse
