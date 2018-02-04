from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name="mwt",
        version="1.0",
        description="Memoize with timeout",
        long_description=readme(),
        author="Alex King",
        author_email="alex_w_king@yahoo.com",
        license="MIT",
        packages=["mwt"],
        )
