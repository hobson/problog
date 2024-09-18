# Prob Log

Tools for probing the reasoning ability of LLMs and logging the problogs (log probabilties) of generated tokens as well as alternatives.

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
- [x] Faz: Fix problog webapp so that extraneous text isn't recorded or displayed. E.g. no "1 2 3 4 5 ..." at beginning of response
- [ ] Faz: Add logging of questions and responses and logprobabilities on backend (python) and save it to disk or in a database
   - [ ] use jsonlines format to persist conversaion JSON to disk
   - [ ] store json payloads sent to LLM
   - [ ] store json payloads received from LLMs
   - [ ] add timestamp if there isn't one in the json dictionary already
- [ ] Faz: Document all the steps required to install and run your React/Next/Flask app and put those steps in this README above 
- [ ] Hobs: Draft a "background" section and abstract for the academic paper
- [ ] Hobs: Draft slides for Oct 12 dinner seminar for Gary Cottrell and the UCSD RET project
- [ ] Hobs: Attempt to get async flask app working again by moving api.py functions back into app.py 
- [x] Vish: Parameterize one GSM8k problem using variable names N_00 ... N_99 to create a [yaml record](docs/chain-of-thought-reasoning-large-numbers.md#Example-parameterized-GSM8k-problem) for at least one problem
- [x] Vish: Create f-string template that can be used to generate multiple questions and answers
- [x] Vish: Create a function for that one word problem that can generate an infinite number of different word problems from one template

### Week 2.5
- [ ] Faz: push all code, docs and datasets to [GitHub repo](github.com:hobson/problog/)
- [x] Faz: Add logging of questions and responses and logprobabilities on backend (python) and save it to disk or in a database
   - [x] use jsonlines format to persist conversaion JSON to disk
   - [x] store json payloads sent to LLM
   - [x] store json payloads received from LLMs
   - [x] add timestamp if there isn't one in the json dictionary already
- [ ] Faz: Document all the steps required to install and run your React/Next/Flask app and put those steps in this README above 

- [x] Hobs: Draft a "background" section and abstract for the academic paper
- [ ] Hobs: Draft slides for Oct 12 dinner seminar for Gary Cottrell and the UCSD RET project
- [ ] Hobs: Attempt to get async flask app working again by moving api.py functions back into app.py 

### Week 3
- [ ] Faz: push all code, docs and datasets to [GitHub repo](github.com:hobson/problog/)
- [ ] Faz: Download gsm8k dataset from huggingface
- [ ] Faz: Predict the answer for each GSM8k question with GPT-3.5-turbo
   - use `gpt-3.5-turbo` with the rate limits specified for the free tier: https://www.google.com/search?client=ubuntu&channel=fs&q=openai+gpt-3.5+free+limit
   - `temperature=0`
   - `logprobs=True`
   - `top_logprobs=10` ( see the `generate_tokens()` function in `src/problog/llm.py` )
   - log all json payloads sent to OpenAI (GSM8kQuestions)
   - log all json responses (answers) received from OpenAI, including logprobs for each token
   - optional: log 10+ alternative tokens for each token that OpenAI generates
- [ ] Faz: While waiting for GPT-3.5-turbo (3 requests/min will take 2 days) try doing inference with reflection-70B: https://openrouter.ai/models/mattshumer/reflection-70b:free/api
- [ ] remove all `r'\<\<.*\>\>` tags from the answers
   - compute the edit distance for each gsm8k answer vs the predictions made by gpt-3.5\ 
- [ ] Faz: Document all the steps required to install and run your React/Next/Flask app and put those steps in this README above 

- [ ] Hobs: Draft a abstract for the academic paper
- [ ] Hobs: Draft a paper title
- [ ] Hobs: Draft a contributions summary
- [ ] Hobs: Draft a bibliography
- [ ] Hobs: Draft slides for Oct 12 dinner seminar for Gary Cottrell and the UCSD RET project

- [ ] Vish: push all code, docs and datasets to [GitHub repo](github.com:hobson/problog/) daily 
- [ ] Vish: Parameterize the word ten and subsitute the digits 10 for the baseline question
- [ ] Vish: Manually test 3 of the GSM Templates with 10 different numerical values
   - llama-2
   - llama-3
   - gpt-3.5
   - gpt-4
- [ ] Vish: Automate the testing and evaluation using all 10 templates

See [docs/chain-of-thought-reasoning-large-numbers.md](docs/chain-of-thought-reasoning-large-numbers.md) for notes on state of the art in math word problem solving with LLMs.
