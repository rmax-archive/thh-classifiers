from setuptools import setup, find_packages

setup(
    name='dirbot',
    version='0.1',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = dirbot.settings']},
    package_data = {'dirbot': ['resources/*.xml',
                        'resources/*.txt',
                        'resources/*.json',
                        'splash/*.lua',
                        ]},
)
