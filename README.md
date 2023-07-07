
# Wav2Vec ASR tool [RUSSIAN]

This app was created in research goals. Transcribes audifiles in Russian language. How it's work:

1) Check `config.yaml`
set your working directory for app and ouput directory:

```yaml
#YAML EXAMPLE
working_dir: D:\\WAV2VEC_ASR_WD\
output_dir: D:\\WAV2VEC_ASR_OUPUT\
```

2) Create venv and activate:
```code
python -m venv .venv
```
and install dependecies:
```code
pip install -r requirements.txt
```
3) start `main.py`
```code
python main.py
```
this will start necessary daemons. IMPORTANT -- closing main process kills daemons.

4) Paste audiofile into `working_dir` you set.

5) Wait for results in `output_dir` you set. 