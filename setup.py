"""
BigchainDB TYMLEZ Consensus Plugin
"""
from setuptools import setup

tests_require = [
    'pytest',
    'pep8',
    'pylint',
    'pytest',
]

dev_require = [
    'ipdb',
    'ipython',
]

docs_require = [
]

setup(
    name='BigchainDB TYMLEZ Consensus Plugin',
    version='0.0.2',
    description='BigchainDB TYMLEZ Consensus Plugin',
    long_description=__doc__,
    url='https://github.com/tymlez/consensus',
    zip_safe=False,

    classifiers=[
        'Development Status :: 3 - Alpha'
    ],

    packages=[
        'consensus_template'
    ],

    entry_points={
        'bigchaindb.consensus': [
            'tymlezconsensus=consensus_template.consensus:ConsensusRulesTemplate'
        ]
    },

    install_requires=[
        'bigchaindb==0.10.0.dev'
    ],
    setup_requires=['pytest-runner'],
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
        'dev':  dev_require + tests_require + docs_require,
        'docs':  docs_require,
    },
)
