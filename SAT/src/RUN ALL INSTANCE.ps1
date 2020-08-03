$out = "D:\University\PROJECTS\COP2\Dicosola - PWP Project\SAT\out"
Get-ChildItem "D:\University\PROJECTS\COP2\Dicosola - PWP Project\Instances" | 
    ForEach-Object {
        pipenv run python main.py --instance $_.FullName --out_dir $out
    }