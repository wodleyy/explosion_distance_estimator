from setuptools import setup, find_packages

setup(
    name='explosion_distance_estimator',
    version='1.0.1',
    author='wodleyy',
    description='Estimate the distance to an explosion from video and audio analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'librosa',
        'matplotlib',
        'numpy',
        'opencv-python',
        'python-dateutil',
        'requests',
        'soundfile'
    ],
    entry_points={
        'console_scripts': [
            'explosion-distance-estimator=explosion_distance_estimator.explosion_distance_estimator:main'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
