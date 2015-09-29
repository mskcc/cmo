PYENV_HOME=$WORKSPACE/.pyenv/
PYTHON_HOME=/opt/common/CentOS_6-dev/python/python-2.7.10/bin/
# Delete previously built virtualenv
if [ -d $PYENV_HOME ]; then
        rm -rf $PYENV_HOME
fi

    # Create virtualenv and install necessary packages
    $PYTHON_HOME/virtualenv --no-site-packages $PYENV_HOME
    . $PYENV_HOME/bin/activate
    $PYTHON_HOME/pip install --quiet nosexcover
    $PYTHON_HOME/pip install --quiet $WORKSPACE/  # where your setup.py lives
    nosetests --with-xunit
#    pylint -f parseable myapp/ | tee pylint.out
