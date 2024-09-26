# Running Backend code (FLASK BACKEND)

## 1. Create Python Virtual Environment

This completes the steps to create and manage Python virtual environments in both Linux and Windows.

### Linux

#### 1. Install `pip`
Install Python and `pip`:

```bash
$ sudo apt-get install python-pip
```

#### 2. Install `virtualenv`
Once `pip` is installed, install `virtualenv`:

```bash
$ pip install virtualenv
```

#### 3. Check `virtualenv` installation
Verify that `virtualenv` was installed correctly:

```bash
$ virtualenv --version
```

#### 4. Create and activate a Virtual environment
To create a virtual environment, use the following command:

```bash
virtualenv .venv
source .venv/bin/activate
which python
```
```text
/home/hobs/code/hobson/problog/.venv/bin/python
```
This will create a folder named `.venv` and make it your default install path for all pip install commands.
Your Python path should now be inside the bin directory of `.venv/`


### Step 5: Activate the Virtual Environment
Activate the virtual environment using the command:

```bash
$ source virtualenv_name/bin/activate
```

Once activated, you are in a Python virtual environment. 

### Step 6: Deactivate the Virtual Environment
To deactivate and exit the virtual environment, use:

```bash
$ deactivate
```

---

## Windows

### Step 1: Install `virtualenv`
If Python is already installed, you can install `virtualenv` using `pip`:

```bash
> pip install virtualenv
```

### Step 2: Create a Virtual Environment
Create a virtual environment in the current directory by running:

```bash
> python -m venv myenv
```

You can replace `myenv` with any name of your choice.

### Step 3: Activate the Virtual Environment
To activate the virtual environment, run:

```bash
> myenv\Scripts\activate
```

You can also specify the full path to the virtual environment if you're not in the same directory.

### Step 4: Deactivate the Virtual Environment
To deactivate the virtual environment, run:

```bash
$ deactivate
```



## Installing everyting

```bash
$ pip install -r requirements.txt
```

## Running the backend code!
### Make sure that env is active before running the app.py 

```bash
$ flask --app app.py --debug run
```

### You may have problem with .env file, at that time please ask me .env file, I will share it with you. I did not put it here because of security concerns!