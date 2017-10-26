from click.types import ParamType, FloatParamType, CompositeParamType
from scipy.stats import skewnorm

# Available click>6.7 - backporting here until released
class FloatRange(FloatParamType):
    """A parameter that works similar to :data:`click.FLOAT` but restricts
    the value to fit into a range.  The default behavior is to fail if the
    value falls outside the range, but it can also be silently clamped
    between the two edges.
    See :ref:`ranges` for an example.
    """
    name = 'float range'

    def __init__(self, min=None, max=None, clamp=False):
        self.min = min
        self.max = max
        self.clamp = clamp

    def convert(self, value, param, ctx):
        rv = FloatParamType.convert(self, value, param, ctx)
        if self.clamp:
            if self.min is not None and rv < self.min:
                return self.min
            if self.max is not None and rv > self.max:
                return self.max
        if self.min is not None and rv < self.min or \
           self.max is not None and rv > self.max:
            if self.min is None:
                self.fail('%s is bigger than the maximum valid value '
                          '%s.' % (rv, self.max), param, ctx)
            elif self.max is None:
                self.fail('%s is smaller than the minimum valid value '
                          '%s.' % (rv, self.min), param, ctx)
            else:
                self.fail('%s is not in the valid range of %s to %s.'
                          % (rv, self.min, self.max), param, ctx)
        return rv

    def __repr__(self):
        return 'FloatRange(%r, %r)' % (self.min, self.max)



class Distribution(object):
    """"Wrap a skewnormal distribuiton so it's rvs method is callable"""
    def __init__(self, delay=0, std=0, skew=0):
        self.distribution = skewnorm(skew, delay, std)

    def __call__(self):
        return max(0.0, self.distribution.rvs())

def distribution(ctx, param, value):
    if len(value) > 3:
        raise RuntimeError(
            "Distributions take no more than 3 arguments, delay, stdev, skew")
    return Distribution(*value)
