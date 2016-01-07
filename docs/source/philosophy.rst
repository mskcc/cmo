===========
Motivations
===========

- Pipelines
  - There is a constant in bioinformatics in that there are very little constants: What is the standard today will not be tomorrow.
    - allow these changes to occur as rapidly as possible
    - calcify them into production only when needed
    - focus on the ad-hoc pipeline - constantly being used
    - select the production pipeline from among the ad-hocs and freeze it and record important metrics about it in a datbase
  - Focus on standardized formats
    - BAM, VCF, MAF(is this standardized?)
    - Pipelines that output standardized things can be combined in unanticipated ways later with minimal difficulty
    - Spend some effort normalizing non-standard output of programs that don't play well with others
-  Sample Tracking
  - Iterative improvement
    - this is a team effort, it won't happen overnight
    - take concrete and easily actionable steps that improve usability
    - reduce human time per sample correctly processed
    - end goal - full automation and automatic rerunnability of 90%+ of samples
-  QC
  - What can be automated?
    - remove humans from the loop if the QC process is computer decideable in >50% of cases
      - begin by presenting humans with PASS/MAYBE/FAIL, and ask them to rerun
      - eventually, automatically re-run fail
- Improved Interactivity
  - websites and weblinks should drive decisions
  - websites should be source of truth, not emails or spreadsheets

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

