from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="pathfinder_spell_crawler",
    version="0.0.1",
    python_requires=">=3.10",
    packages=['pathfinder_spell_crawler'],
    author="Guillaume C",
    long_description="",
    install_requires=requirements,
)
