import collections


class BaseSequence(object):
    def gen(self, model):
        raise NotImplementedError('Please use a subclass instead.')


class IncrementalSequence(BaseSequence):
    def __init__(self, value, increment_by=1):
        self.value = value
        self.counter = increment_by
        self.increment_by = increment_by

    def get_inc(self, model):
        if not model.objects.count():
            self.counter = self.increment_by
        i = self.counter
        self.counter += self.increment_by
        return i

    def gen(self, model):
        inc = self.get_inc(model)
        return self.value + type(self.value)(inc)

incr = IncrementalSequence


class IterableSequence(BaseSequence):
    def __init__(self, values):
        self.values = values
        self._counter = 0

    def gen(self, model):
        if self._counter >= len(self.values):
            self._counter = 0
        self._counter += 1
        return self.values[self._counter-1]

itera = IterableSequence


class Sequence(BaseSequence):
    def __init__(self, value, *args, **kwargs):
        if not isinstance(value, basestring) and isinstance(value, collections.Iterable):
            self.seq = itera(value, *args, **kwargs)
        else:
            self.seq = incr(value, *args, **kwargs)

    def gen(self, model):
        return self.seq.gen(model)
