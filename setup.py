from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='hey_whisper',
    version='1.0.0',
    author='Victor Rodriguez-Fernandez',
    author_email='victor.rfernandez@upm.es',
    description='Command-line tool for audio transcription using OpenAI Whisper AI',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'hey_whisper=hey_whisper.main:run_transcription',
        ]
    },
    url='https://github.com/vrodriguezf/hey_whisper', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)