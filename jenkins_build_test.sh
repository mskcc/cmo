PYENV_HOME=$WORKSPACE/.pyenv/

# Delete previously built virtualenv
if [ -d $PYENV_HOME ]; then
        rm -rf $PYENV_HOME
fi

    # Create virtualenv and install necessary packages
    virtualenv --no-site-packages $PYENV_HOME
    . $PYENV_HOME/bin/activate
    pip install --quiet nosexcover
    pip install --quiet pylint
    pip install --quiet $WORKSPACE/  # where your setup.py lives
    nosetests --with-xcoverage --with-xunit --cover-package=myapp --cover-erase
#    pylint -f parseable myapp/ | tee pylint.out
