# Language Translation using Recurrent Neural Networks

### Created by
### Devashish Gaikwad 111608023
### Atharva Jadhav 111608031
### COEP Third Year Information Technology

*Make sure these requirements are satisfied:*
1. Make sure your python version is 3.6 and has installed the libraries mentioned in `requirements.txt`\
 You can use `pip3 install -r requirements.txt`
2. `rest_server.py` has executable permissions - `chmod +x rest_server.py`
3. First line in rest_server.py is set to path of python3.6 executable from home directory\
 for example : `#!/home/path/to/interpreter/python`
4. Make sure you create two folders `en_de` and `en_fr` at this directory level\
 Add fairseq model files (only files - generally 4 per model) for \
 English to German to en_de\
 English to French to en_fr

*How to use:*
1. REST server runs on `localhost:5000/translate`
2. Use the following JSON object to send translation requests to rest server:\
```javascript

{
    "src_lang" : "en",
    "tgt_lang" : "de" or "fr",
    "text" : "text to translate"
}

```
3. The response for the request will take about 10s to arrive, it will arrive in the following form:
```javascript

{
    "text" : "translated text",
    "err_no" : error number,
    "err" : "error descr"
}

```
