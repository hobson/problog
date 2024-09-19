# Magic_Words

In order to run the code for the paper [What's the Magic Word? A Control Theory of LLM Prompting](https://arxiv.org/abs/2310.04444) on a CPU-only PC (very slow), you will need make sure a global DEVICE variable is set to torch.device('cpu') and you do not attempt to use the `device_map` option for any of the Magic_Words Python modules.

Use virtualenv instead of venv if you want to save a bit of package download and build time:

```bash
# Must be run from a base Python 3.10 environment
python -m virtualenv .venv
source .venv/bin/activate

# run setup.py so that the magic_words/ packaged is added to your PYTHON_PATH
# --editable means when you edit magic_words/*.py you do not need to reinstall
pip install --editable .
pip install -r requirements.txt

# Install torch packages built for CPU-only inference (NO GPU support)
pip install --upgrade \
  torch==2.2.2+cpu \
  torchvision==0.17.2+cpu \
  -f https://download.pytorch.org/whl/torch_stable.html
```


## Examples

### 
Greedy back generation and greedy coordinate gradient (GCG) to find 
optimal control prompts (_magic words_). 

## Setup


## Example Script (Pointwise Control)

Run the script in `scripts/backoff_hack.py` for a demo of finding the **magic
words** (optimal control prompt) for a given question-answer pair using greedy
search and greedy coordinate gradient (GCG). It applies the same algorithms as
in the [LLM Control Theory](https://arxiv.org/abs/2310.04444) paper: 

```bash
python3 scripts/backoff_hack_demo.py
```
See the comments in the script for further details. [This issue
thread](https://github.com/amanb2000/Magic_Words/blob/1986861b51433fb7ad55ef39cde98afd1d76535c/scripts/backoff_hack_demo.py#L113)
is also a good resource for getting up and running.

## Example Script (Optimizing Prompts for Dataset)

Here we apply the GCG algorithm from the [LLM attacks
paper](https://arxiv.org/abs/2307.15043) to optimizing prompts on a dataset,
similar to the [AutoPrompt](https://arxiv.org/abs/2010.15980) paper. 

```bash
python3 scripts/sgcg.py \
    --dataset datasets/100_squad_train_v2.0.jsonl \
    --model meta-llama/Meta-Llama-3-8B-Instruct \
    --k 20 \
    --max_parallel 30 \
    --grad_batch_size 50 \
    --num_iters 30
    
```


## Open-Ended Exploration of the Reachable Set
```bash
python3 scripts/greedy_forward_single.py \
    --model meta-llama/Meta-Llama-3-8B \
    --x_0 "helloworld1" \
    --output_dir results/helloworld1 \
    --max_iters 100 \
    --max_parallel 100 \
    --pool_size 100 \
    --rand_pool \
    --push 0.1 \
    --pull 1.0 \
    --frac_ext 0.2 


```


## Testing
```
# run all tests: 
coverage run -m unittest discover

# get coverage report:
coverage report --include=prompt_landscapes/*

# run a specific test:
coverage run -m unittest tests/test_compute_score.py
``````




