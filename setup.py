from setuptools import setup, find_packages

setup(
    name='ttm',
    version='1.0',
    author='Sammy Breen',
    author_email='s.breen@tum.de',
    packages=find_packages(),
    # scripts=['ttm', 'test.py'],
    # data_files=[('templatecase', ['*'])],
    include_package_data=True,
    install_requires=[
        'setuptools-git',
        'altair',
        'branca',
        'bs4',
        'geopy',
        'gpxpy',
        'folium',
        'matplotlib',
        'netCDF4',
        'numpy',
        'pandas',
        'PyFoam',
        'requests',
        'scipy',
        'tikzplotlib',
        'timezonefinder',
        'tzwhere'
      ],
    entry_points={
        'console_scripts': [
            'ttm=ttm.ttm:main',
        ]
    }
)