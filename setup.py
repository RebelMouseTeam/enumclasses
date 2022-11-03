import setuptools


setuptools.setup(
    name='enumclasses',
    version='1.1.4',
    author='CordiS',
    author_email='cordis@rebelmouse.com',
    url='https://github.com/RebelMouseTeam/enumclasses',
    license='Apache 2.0',
    packages=['enumclasses'],
    test_suite='tests',
    install_requires=[
        'ply', 'decorator', 'six'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: Apache Software License',
    ],
)
