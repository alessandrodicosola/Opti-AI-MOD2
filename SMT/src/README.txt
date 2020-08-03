** REQUIREMENTS **
pipenv install z3_solver

** USAGE **
pipenv run python main.py --instance [ABSOLUTE PATH OF INSTANCE] --out_dir [ABSOLUTE PATH OF OUTPUT DIR] [--rot] [--same_size]
OPTIONAL:
 --rot: Allow rotation
 --same_size: Allow lex_lesseq constraint