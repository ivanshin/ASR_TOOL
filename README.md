
# Wav2Vec ASR tool [RUSSIAN]

## V0.2 Every main and child process now logs to SQLite DB or a console!

This app was created in research goals. Transcribes audifiles in Russian language. How it's works:

1) Check `config.yaml`
set your working directory for app and ouput directory:

```yaml
#YAML EXAMPLE
# [directories settings]
working_dir: /media/ivan/Диск/WAV2VEC_WD
output_dir: /media/ivan/Диск/WAV2VEC_OUTPUT

# [transcriber settings]
model: #large-v2 # 'tiny' by default if blank (Whisper model settings)

# [multiple GPU support]
devices:
  - cpu
  # set your cuda devices:  #- cuda:0
                            #- cuda:1 
  # OR
  #set blank if CPU (set same device multiple times to spawn more workers:   #- cpu
                                                                             #- cpu)

# [logging settings]
logs_to_db: True # False
logs_db_path: /media/ivan/Диск/WAV2VEC_DB # set path where to store SQLite DB if logs_to_db = True| else None
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

## Additions:

[Example of SQLite DB](docs/db_example.png)
