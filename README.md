# Prob Log

Tools for probing the reasoning ability of LLMs.

## Install

```bash
git clone git@github.com:hobson/problog/
cd problog
pip install virtualenv
python -m virtualenv .venv
source .venv/bin/activate
pip install -e .
python src/logprob/app.py
```

This should open a browser tab where you can enter your prompt/message into the text box and view the logprobability for each token of the generated response.