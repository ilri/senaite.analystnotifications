from setuptools import setup, find_packages

setup(
    name="senaite.analystnotifications",
    version="1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["senaite"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "z3c.autoinclude",
    ],
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)