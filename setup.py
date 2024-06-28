from setuptools import find_packages, setup

setup(
    name="space_x_project",
    packages=find_packages(exclude=["space_x_project_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
