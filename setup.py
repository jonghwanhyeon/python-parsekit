from setuptools import find_packages, setup

setup(
    name='python-parsekit',
    version='1.0.0',
    description='A parser combinator for Python',
    url='https://github.com/jonghwanhyeon/python-parsekit',
    author='Jonghwan Hyeon',
    author_email='hyeon0145@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords='parser combinator',
    packages=find_packages(),
    python_requires='>=3',
)
