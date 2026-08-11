## Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

## Install New Packages

Example:

```bash
python -m pip install pillow
```

Update `requirements.txt` after installing new packages:

```bash
python -m pip freeze > requirements.txt
```

---

## Run

Launch the application:

```bash
PYTHONPATH=src python -m email_tool.main
```

Select a tool from the interactive menu.

---