$out = "D:\University\PROJECTS\COP2\Dicosola - PWP Project\CP\out"
Get-ChildItem "D:\University\PROJECTS\COP2\Dicosola - PWP Project\Instances" | 
    ForEach-Object {
        pipenv run python model1.py --solver chuffed --model model1.mzn --instance $_.FullName --out_dir $out
    }