============
CMO Wrappers
============
What's the point of this?
------------------------
The CMO python package provides a serious of lightweight python wrappers to common Bioinformatics tools to abstract away a few things that are annoying to everybody:

- it calls java for you with appropriate but overrideable java args
- it keeps track of reference sequences
- it allows you to select different versions of the same program with one argument, and keeps track
  of that version's binary location for you, no lookup required
- it standardizes to some extent the interfaces of different programs
- eventually, it will allow adhoc lsf workflows with a minimum of effort
- programs will all pass through the same command calling function that allows command start/stop time logging and nice redirection of STDOUT/STDERR on demand
- errors can be caught even for nonstandard exit codes and python can correct them,
  allowing LSF or the Shell to get the correct result
- poorly behaved programs like BWA can be automatically given a nicely behaved --output argument, instead of writing a bam/sam to STDOUT


