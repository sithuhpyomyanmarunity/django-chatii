# Table of Contents <!-- omit in toc -->
- [Dependency](#dependency)
- [Setting up](#setting-up)
- [Running the server](#running-the-server)
  - [Run the Soketi (a.k.a pusher)](#run-the-soketi-aka-pusher)
  - [Run the django app](#run-the-django-app)
- [Appendix](#appendix)
  - [How to activate virtual environment for python](#how-to-activate-virtual-environment-for-python)

<br>

## Dependency

**Need to install**
- Python 3.8 
- NodeJS
- Postgres (14 optional version)

**Rely on**
- [Django 4.1](https://www.djangoproject.com/)
- [Django rest framework](https://www.django-rest-framework.org/)
- [Soketi](https://docs.soketi.app/)
- [Tailwindcss](https://tailwindcss.com/docs/installation)

<br>

## Setting up

**Before setting up make sure all required dependency are install. Especially postgers please check out [here](https://www.psycopg.org/docs/install.html#build-prerequisites)**

1. Creating postgres user and database 
```sql
-- connect to you postgres and run following sql

-- creating user
CREATE USER foreg WITH PASSWORD 'secret' CREATEDB;

-- creating database
CREATE DATABASE chatii OWNER forge;
```

2. Installing node modules by following command.
```bash
npm install
```

3. Create virtual environment for python using following command.

```bash
python3 -m venv .venv
```

4. Activating python virtual environment.

```bash
# for window powershell
venv\Scripts\Activate.ps1

# for linux/mac
source .venv/bin/activate
```

5. Installing python packages using following command. (**note: make sure python virtual environment is activated please check previous step.**)

```bash
pip install -r requirements.txt
```

5. Copy [.env.example](./env.example) file and name it as `.env`

6. Editing `.env` file from previous step to match your machine. e.g. for `database` which have been create at `step 1`

```diff
-DATABASE_NAME=
-DATABASE_USER=
-DATABASE_PASSWORD=

+DATABASE_NAME=chatii
+DATABASE_USER=forge
+DATABASE_PASSWORD=secret
```

<br>

## Running the server

### Run the Soketi (a.k.a pusher)

Start soketi server using following command

```bash
npm run soketi:start
```

### Run the django app

Start django server

(**note: make sure python virtual environment is activated please check [here](#how-to-activate-virtual-environment-for-python) for how to activate**)

```bash
python manage.py runserver
```

## Appendix

### How to activate virtual environment for python

```bash
# for window powershell
venv\Scripts\Activate.ps1

# for linux/mac
source .venv/bin/activate
```