Creating a Python package that can be installed with `pip` and automatically handles dependencies involves several steps, including setting up the directory structure, writing the code, defining dependencies, and making the package installable. Here, I'll guide you through the process using `click` for creating a simple command-line interface (CLI) application.

### Step 1: Setup Your Package Structure
First, you'll need to set up the correct directory structure. Here’s a basic setup:

```
your_package/
│
├── your_package/
│   ├── __init__.py
│   └── cli.py
│
├── setup.py
└── README.md
```

- `your_package/` (outer) is your source directory.
- `your_package/` (inner) is your actual Python package.
- `cli.py` will contain your `click` CLI code.
- `setup.py` is the setup script for installing the package.
- `README.md` is a markdown file containing the information about your package.

### Step 2: Write Your CLI Application using Click
In `your_package/cli.py`, you can create a simple CLI using `click`. Here’s an example:

```python
import click

@click.command()
@click.option('--name', prompt='Your name', help='The person to greet.')
def greet(name):
    click.echo(f"Hello {name}!")

if __name__ == '__main__':
    greet()
```

### Step 3: Create the `setup.py` File
The `setup.py` file is essential for making your package installable via `pip`. Here's how you can write it:

```python
from setuptools import setup, find_packages

setup(
    name='your_package',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',  # Add other dependencies here
    ],
    entry_points='''
        [console_scripts]
        your-command=your_package.cli:greet
    ''',
)
```

- `name`: the name of your package (this is how users will install it using `pip`).
- `version`: the current version of your package.
- `packages`: this discovers all packages and sub-packages.
- `install_requires`: a list of dependencies needed to run the package. Here, `click` is listed as a dependency.
- `entry_points`: defines the command line scripts provided by your package.

### Step 4: README.md
Provide a simple description of your package in `README.md`. For example:

```markdown
# Your Package

This is a simple CLI application using Click to demonstrate how to build Python packages.
```

### Step 5: Installing Your Package Locally
Navigate to your package directory (where `setup.py` is located) and run:

```bash
pip install .
```

This command will install your package locally. Alternatively, you can use:

```bash
pip install -e .
```

This will install the package in editable mode, which is useful for development since changes to the source files will immediately affect the installed package without needing a reinstall.

### Step 6: Usage
Once installed, you can run your CLI command (`your-command`) from anywhere in your terminal:

```bash
your-command
```

### Step 7: Distributing Your Package
If you want to distribute your package so others can install it using `pip`, consider publishing it on PyPI. You’ll need to register with PyPI and use tools like `twine` to upload your package.

This guide should help you get started with creating a basic CLI application packaged for easy installation with pip and automatic handling of dependencies.