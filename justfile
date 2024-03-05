# Justfile

# load environment variables
set dotenv-load

# aliases
alias fmt := format
alias pres := presentation
alias plan := planning
alias project := planning
alias marvin-docs := docs-marvin
alias docs-preview := preview

# list justfile recipes
default:
    just --list

# ipy
ipy *args:
    birdbrain ipy {{ args }}

# install
install:
    @uv pip install -e '.'

# setup
setup:
    @pip install uv
    @uv pip install -r dev-requirements.txt
    just install

# build
build:
    just clean
    @python -m build

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
    @streamlit run src/ibis_birdbrain/app.py

# format
format:
    ruff format .

# smoke-test
smoke-test:
    black --check .

# clean
clean:
    @rm -rf dist || True
    @rm -rf *.ddb* || True
    @rm -rf data/*.parquet || True

# open docs
docs:
    @open https://ibis-project.github.io/ibis-birdbrain/

docs-marvin:
    @open https://www.askmarvin.ai/welcome/what_is_marvin/

# open repo
repo:
    @open https://github.com/ibis-project/ibis-birdbrain

# presentation
presentation:
    @quarto preview presentation/index.qmd

# planning
planning:
    @open https://github.com/orgs/ibis-project/projects/2/views/1
