# Andmebaaside_Projekt_Beta

## In `/frontend` folder:

> To install all required dependencies, run this command:
>
> ```bash
> npm i package.json
> ```
>
> And to start frontend server, run this command:
>
> ```bash
> npm start
> ```

## In `/backend` folder:

> Create `data.py` file
>
> ```python
> DBusername = 'root'
> DBpassword = 'password'
> DBhost = 'localhost'
> DBport = '3306'
> DBdatabase = 'hotel'
>
> #To create secret key run this in terminal: openssl rand -hex 32
> SECRET_KEY = 'verysecretkeygoesherenlawdlanwldalwdbaljfbljnsxlkvnbodsjrvnf'
> ```
>
> To install all required packages, run this command:
>
> ```bash
> pip install -r requirements.txt
> ```
>
> And to run server, run this:
>
> ```bash
> uvicorn main:app --reload
> ```
