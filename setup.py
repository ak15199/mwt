from setuptools import setup, find_packages

def readme():
    with open("README.md") as f:
        return f.read()

setup(name="mwt",
        version="0.9.0b1",
        description="Memoize with timeout",
        long_description=readme(),
        url="https://github.com/ak15199/mwt.git",
        packages=find_packages(),
        author="Alex King",
        author_email="alex_w_king@yahoo.com",
        license="MIT",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Build Tools",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            ],
        keywords="memoize cache python function decorator",
        )
