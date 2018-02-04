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

    from mwt import mwt

    @mwt()
    def fibonacci():
        a,b = 1,1

        for i in range(n-1):
            a,b = b,a+b

        return a

    print(fibonacci(500))
    print(fibonacci(500))

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

