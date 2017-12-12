#WORKSPACE=/home/nikhil/cmo
PYENV_HOME=$WORKSPACE/.pyenv/
PYTHON_HOME=/opt/common/CentOS_6-dev/python/python-2.7.10/bin/
export CMO_RESOURCE_CONFIG=/ifs/work/pi/testdata/cmo_resources.json
source /ifs/work/pi/roslin-core/1.0.0/config/settings.sh
source /ifs/work/pi/roslin-core/1.0.0/config/variant/1.3.5/settings.sh
export PATH=$PATH:/ifs/work/pi/roslin-core/1.0.0/bin/sing/
export TMPDIR="/scratch"
export TMP="/scratch"
#export PATH=$PATH:/opt/common/CentOS_6-dev/bin/current/
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib64/
#export CMO_RESOURCE_CONFIG=/ifs/work/pi/testdata/cmo_resources.json
#source $WORKSPACE/test/settings.sh
#source $WORKSPACE/test/sing.sh
# Delete previously built virtualenv
if [ -d $PYENV_HOME ]; then
        rm -rf $PYENV_HOME
fi
    
    # Create virtualenv and install necessary packages
   $PYTHON_HOME/virtualenv --no-site-packages $PYENV_HOME
    . $PYENV_HOME/bin/activate
    #export TMPDIR="/srv/scratch"
    #export PATH=$PATH:/opt/common/CentOS_6-dev/bin/current/
    #export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib64/
    #export CMO_RESOURCE_CONFIG=/ifs/work/pi/testdata/cmo_resources.json
    #source $WORKSPACE/test/settings.sh
    #source $WORKSPACE/test/sing.sh
    pip install --quiet nosexcover
# sed -i "s/\/ifs\/depot\/assemblies\/H.sapiens\/b37\/b37.fasta/\/ifs\/work\/pi\/testdata\/assemblies\/b37.fasta/g" $WORKSPACE/cmo/data/cmo_resources.json
#    sed -i "s/\/ifs\/depot\/assemblies\/H.sapiens\/b37\/index\/bwa\/0.7.12\/b37.fasta/\/ifs\/work\/pi\/testdata\/assemblies\/bwa\/0.7.12\/b37.fasta/g" $WORKSPACE/cmo/data/cmo_resources.json
    python $WORKSPACE/setup.py install  # where your setup.py lives
    nosetests --with-xunit
#cmo_picard --version 1.96 --cmd FixMateInformation --I /ifs/work/pi/testdata/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam --O /scratch/tmp45ApHY/output
#cmo_picard --version 1.96 --cmd FixMateInformation --I /ifs/work/pi/testdata/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam --O /scratch/tmp45ApHY/output
#    pylint -f parseable myapp/ | tee pylint.out
