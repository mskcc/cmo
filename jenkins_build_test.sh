PYENV_HOME=$WORKSPACE/.pyenv/
PYTHON_HOME=/opt/common/CentOS_6-dev/python/python-2.7.10/bin/
export CMO_RESOURCE_CONFIG=/ifs/work/pi/testdata/cmo_resources.json
source /ifs/work/pi/roslin-core/1.0.0/config/settings.sh
source /ifs/work/pi/roslin-core/1.0.0/config/variant/1.3.5/settings.sh
export PATH=$PATH:/ifs/work/pi/roslin-core/1.0.0/bin/sing/
export TMPDIR="/scratch"
export TMP="/scratch"
# Delete previously built virtualenv
if [ -d $PYENV_HOME ]; then
        rm -rf $PYENV_HOME
fi
    
    # Create virtualenv and install necessary packages
   $PYTHON_HOME/virtualenv --no-site-packages $PYENV_HOME
    . $PYENV_HOME/bin/activate
    pip install --quiet nosexcover
    python $WORKSPACE/setup.py install  # where your setup.py lives
    nosetests --with-xunit
