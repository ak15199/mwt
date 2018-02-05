# Memoize with Timeout

Function decorator and anciliary tooling to "memoize", or cache return values from a function call. Timeouts are important to ensure that the cache doesn't grow indefinitely, and has the advantage of culling on length since it is less subject to thrashing.

## Getting Started

### Installing

MWT can be installed using pip:

    $ pip install mwt

If you want to run the latest version of the code, you can install from git:

    $ pip install -U git+git://github.com/...

### Using MWT

At its simplest, simply decorate your method with MWT:

    import timeit
    from mwt import mwt

    @mwt()
    def fibonacci(n):
        a,b = 1,1

        for i in range(n-1):
            a,b = b,a+b

        return a

    def test():
        fibonacci(5)

    for i in range(5):
        print timeit.timeit("fibonacci(50000)", "from __main__ import fibonacci", number=1)

    pi@pi:/tmp $ python fib.py
    0.470113992691
    4.10079956055e-05
    3.50475311279e-05
    3.88622283936e-05
    2.59876251221e-05


### A Note of Caution

Just because you can do something, it doesn't mean that you should.

The MWT decorator is a quick and easy way to resduce extended time in
calculation, but it is by definition not perfect: there are overheads to
the memoization and garbage collection process implicit in memoization,
and caution in its use is presented.

In particular, watch out for the overall time executed, and secondly
the cache hit ratio: if the percentage of hits is small, then the net
effect is to add overhead, not reduce it.

There are two things that can be done to evaluate performance. The first
and most obvious is to profile timings and see whether time overall has
been saved with the addition of the decorator.

The other is to analyze cache statistics after the containing code has been
running for a while. MWT provides a stats interface to assist with this,
and it can be utilized like this:

    fmt = "%-15s %8s %8s %8s %8s %8s %8s"
    print(fmt%("Cache", "Length", "Hits", "Misses", "Purged",
            "Timeouts", "HWM"))
    stats = mwt.stats()
    for stat in stats:
        print(fmt%(stat["cache"], stat["length"], stat["hits"],
                stat["misses"], stat["purged"], stat["timeouts"],
                stat["hwm"]))

Which will produce output like this which will allow you to see how
effective the memoization process is for each of the functions that are
decorated:

    Cache               Length    Hits   Misses   Purged Timeouts      HWM
    opc.hue:rgbToHsv         0       0        0        0        0        0
    opc.hue:hue              0       0        0        0        0        0
    opc.hue:hsvToRgb     27167   32785      270     5103        0    27183

A high hit:miss ratio indicates that the cache is performing well.

If the ratio is poor, though, then don't give up straight away: it's
possible that matters may be improved by tweaking the target method's
calling parameters (for example, bounding a float to perhaps a couple of
digits of precision).

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Alex King** - *Initial work* - [ak15199](https://github.com/ak15199)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Based on inspiration from [MEMOIZE DECORATOR WITH TIMEOUT (PYTHON RECIPE)](http://code.activestate.com/recipes/325905-memoize-decorator-with-timeout/)

