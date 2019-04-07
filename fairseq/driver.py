import subprocess

def driver(src_lang = "en", tgt_lang="de", input_str="Good Morning"):
    transfilename = "{}_{}_translate.txt".format(src_lang, tgt_lang)
    transfilefd = open(transfilename, "rw")
    transfilefd.write(input_str)
    transfilefd.close()
    transop = ""

    if(src_lang=="en" and tgt_lang=="de"):
        transop = subprocess.check_output("python3 interactive_modified.py --path ../wmt16.en-de.joined-dict.transformer/model.pt ../wmt16.en-de.joined-dict.transformer --beam 5 --source-lang en --target-lang de",
        shell=True, universal_newlines=True, encoding='utf-8')