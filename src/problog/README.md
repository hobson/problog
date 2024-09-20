## Running Backend code (FLASK BACKEND)

## Creating a Python Virtual Environment

## This completes the steps to create and manage Python virtual environments in both Linux and Windows.

## Linux

### Step 1: Install `pip`
To start, install `pip` using the following command:

```bash
$ sudo apt-get install python-pip
```

### Step 2: Install `virtualenv`
Once `pip` is installed, install `virtualenv`:

```bash
$ pip install virtualenv
```

### Step 3: Check `virtualenv` Installation
Verify that `virtualenv` was installed correctly:

```bash
$ virtualenv --version
```

### Step 4: Create a Virtual Environment
To create a virtual environment, use the following command:

```bash
$ virtualenv virtualenv_name
```

This will create a folder named `virtualenv_name`. You can replace `virtualenv_name` with any name you'd like.

#### Creating Virtual Environment for Specific Python Versions
To create a virtual environment with a specific version of Python:

For Python 3:
```bash
$ virtualenv -p /usr/bin/python3 virtualenv_name
```

For Python 2.7:
```bash
$ virtualenv -p /usr/bin/python2.7 virtualenv_name
```

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