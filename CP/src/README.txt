** REQUIREMENTS **
pipenv install minizinc

** USAGE **
+ pipenv run python model[1|2].py --solver (gecode|chuffed) --model model[1|2].mzn --instance [absolute path of the instance] --out_dir [ABSOLUTE PATH of the output dir]
- For model1.mzn it's important to comment constants used for testing and uncomment the right search strategy for the right solver.

NOTE: Some problems are inserted inside the *.mzn file if is not possibile to use pipenv