import setuptools


setuptools.setup(
    name='enumclasses',
    version='1.1.3',
    author='Tomas Aparicio',
    author_email='tomas@aparicio.me',
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
