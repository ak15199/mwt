from setuptools import setup, find_packages

def readme():
    with open("README.md") as f:
        return f.read()

setup(name="mwt",
        version="0.9.1",
        description="Memoize with timeout",
        long_description=readme(),
        url="https://github.com/ak15199/mwt.git",
        packages=find_packages(),
        author="Alex King",
        author_email="alex_w_king@yahoo.com",
        license="MIT",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: BSD License",
            ],
        keywords="memoize cache python function decorator",
        )
