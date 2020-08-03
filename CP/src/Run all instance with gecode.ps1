$out = "D:\University\PROJECTS\COP2\Dicosola - PWP Project\CP\out-gecode"
Get-ChildItem "D:\University\PROJECTS\COP2\Dicosola - PWP Project\Instances" | 
    ForEach-Object {
        pipenv run python main.py --solver gecode --model model1.mzn --instance $_.FullName --out_dir $out
    }