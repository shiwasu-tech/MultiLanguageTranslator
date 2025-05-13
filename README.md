This is a web application for translation.
This can translate every language into Mostly-Used language.

## setup
1. install uv
2. clone this repo
3. get Service Account Key (.json) from Google Cloud Console
4. add the json file into environmental PATH with command below
   ```
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
   ```

## How to use (only for debuging or localy use) 
1. run command below to setup
  ```
  uv init
  uv sync
  ```
2. run command below to launch localhost server
  ```
  uv run app.py
  ```
3. access ```http://127.0.0.1//256000```
