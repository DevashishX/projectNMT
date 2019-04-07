import subprocess

def post_process(text=""):
    new_text = text.replace("&apos; ", "'").replace("@@", "")
    return new_text

def trans_process(text=""):
    new_text = text.replace(".", " ").replace(",", " ")
    return new_text

def driver(src_lang = "en", tgt_lang = "de", input_str = "How are you ?"):
    foldername = "{}_{}".format(src_lang, tgt_lang)
    transfilename = "totranslate.txt"
    command = "python3 interactive_modified.py --path ./{}/model.pt ./{}/ -s {} -t {} --input {}".format(foldername, foldername, src_lang, tgt_lang, transfilename)
    
    input_str = trans_process(input_str)

    fd = open(transfilename, "w")
    fd.write(input_str)
    fd.close()

    transtext = subprocess.check_output(command, shell=True, universal_newlines=True)
    return post_process(transtext)

if __name__ == "__main__":
    print(driver())