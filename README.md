## For users of the luna cluster at MSKCC CMO

Add this to your `~/.profile` to get access to the `cmo_*` and `cmoflow_*` tools:
```bash
# Set PATH to include MSKCC's bin of tools, if found
if [ -d "/opt/common/CentOS_6-dev/bin/current" ]; then
    PATH="/opt/common/CentOS_6-dev/bin/current:$PATH"
fi

# Set PATH to include MSKCC's bin of python tools, if found
if [ -d "/opt/common/CentOS_6-dev/python/python-2.7.10/bin" ]; then
    PATH="/opt/common/CentOS_6-dev/python/python-2.7.10/bin:$PATH"
fi
```

Documentation [lives here](http://plvcbiocmo2.mskcc.org), and running workflows can be [tracked here](https://haystack.mskcc.org/workflows).

## For external users

Here is how to install these tools without sudo rights:
```bash
curl -LO https://github.com/mskcc/cmo/archive/master.zip
unzip master.zip
cd cmo-master
python setup.py install --user
```

Add this to your `~/.profile` to get access to the `cmo_*` and `cmoflow_*` tools:
```bash
# Set PATH to include local python bin if found
if [ -d "$HOME/.local/bin" ]; then
    PATH="$HOME/.local/bin:$PATH"
fi
```

## For all other users
![Data Yes!](http://33.media.tumblr.com/560c6bd597ab217cec337b24e66ddf5e/tumblr_nsjtulCu5G1s391qwo1_400.gif)
