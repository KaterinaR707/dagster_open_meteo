from setuptools import find_packages, setup

setup(
    name="weather_open_meteo",
    packages=find_packages(exclude=["weather_open_meteo_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
