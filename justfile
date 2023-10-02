# Justfile

# load environment variables
set dotenv-load

# aliases
alias fmt := format

# list justfile recipes
default:
    just --list

# ipy
ipy *args:
    birdbrain ipy {{ args }}

# setup
setup:
    @pip install -r dev-requirements.txt

# build
build:
    just clean
    @python -m build

# install
install:
    @pip install -e '.'

# uninstall
uninstall:
    @pip uninstall ibis-birdbrain -y

# publish-test
release-test:
    just build
    @twine upload --repository testpypi dist/* -u __token__ -p ${PYPI_TEST_KEY}

# publish
release:
    just build
    @twine upload dist/* -u __token__ -p ${PYPI_KEY}

# quarto stuff
preview:
    @quarto preview docs

# streamlit stuff
app:
    @streamlit run app.py

# format
format:
    black .

# smoke-test
smoke-test:
    black --check .

# clean
clean:
    @rm -rf dist || True

