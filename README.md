# Prob Log

Tools for probing the reasoning ability of LLMs.

- web interface to interact with multiple free LLMs at different LLM providers (open router, OpenAI, anyscale?)
- display probabilities of individual tokens using color scale
- record all prompts and responses from the LLM along with metadata such as probabilities of each token
- record all alternative lower probability tokens that were not generated along with each LLM response (to see if correct answer was among lower probability tokens)

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

## TODO

### Week 1
- [x] Faz: Get problog webapp working
- [x] Faz: Improve color scale labeling low=>0.0, under=>0.5, above=>1.0
- [x] Hobs: research state of the art for word problems
- [x] Hobs: try to find research into large number math word problems and LLMs
- [x] Hobs: review word problem datasets to see what parameterization has already been accomplished 
- [ ] Vish: Parameterize one GSM8k problem using variable names N_00 ... N_99 to create a [yaml record](docs/chain-of-thought-reasoning-large-numbers.md#Example-parameterized-GSM8k-problem) for at least one problem
- [ ] Vish: Create f-string template that can be used to generate multiple questions and answers
- [ ] Vish: Create a function for that one word problem that can generate an infinite number of different word problems from one template

### Week 2
- [ ] Faz: Fix problog webapp so that extraneous text isn't recorded or displayed. E.g. no "1 2 3 4 5 ..." at beginning of response
- [ ] Faz: Add logging of questions and responses and logprobabilities on backend (python) and save it to disk or in a database
- [ ] Faz: Document all the steps required to install and run your React/Next/Flask app and put those steps in this README above 
- [ ] Hobs: Draft a "background" section and abstract for the academic paper
- [ ] Hobs: Draft slides for Oct 12 dinner seminar for Gary Cottrell and the UCSD RET project
- [ ] Hobs: Attempt to get async flask app working again by moving api.py functions back into app.py 
- [ ] Vish: Parameterize one GSM8k problem using variable names N_00 ... N_99 to create a [yaml record](docs/chain-of-thought-reasoning-large-numbers.md#Example-parameterized-GSM8k-problem) for at least one problem
- [ ] Vish: Create f-string template that can be used to generate multiple questions and answers
- [ ] Vish: Create a function for that one word problem that can generate an infinite number of different word problems from one template

See [docs/chain-of-thought-reasoning-large-numbers.md](docs/chain-of-thought-reasoning-large-numbers.md) for notes on state of the art in math word problem solving with LLMs.