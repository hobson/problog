# 2024-07-03 problog logprobs RET project abstract Leon Bergen

## Magic Words paper

Magic word prompting is when you are trying to control the next token generated, e.g. "Roger Fedderer is the ____" where you want the LLM to generate "greatest". You are allowed to prefix the ""
State of the art for "magic word" generation is GCG algorithm from the Autoprompt paper:

- [Autoprompt paper](https://arxiv.org/abs/2010.15980)
- [Greedy Coordinate Gradient (GCG) attack algorithm paper](https://arxiv.org/abs/2307.15043)
- [Prefix tuning: Optimizing Continuous Prompts for Generation](https://arxiv.org/pdf/2101.00190) -- By prefixing a prompt with a word embedding or two you can easily steer the conversation or "jailbreak". But it's much harder when the embeddings need to be replaced with discrete token IDs.
- Another paper by Meta to do OCR+language models on large PDF documents using small transformers like BART/GPT-2 and LSTMs, if you prompt with a sentence that has a little noise in it, the model will do fine for one sentence or so, but then fall off the edge of the manifold and start generating noise with high confidence. Danlu feels this shows that Trasformers and language models do not generalize to reasoning patterns outside of their training set. 


- [Magic Word code](https://arxiv.org/pdf/2310.04444)
- [GCG attack and Magic Word code](https://github.com/amanb2000/Magic_Words)

Here's a quickstart script. The `requirements.txt` and the Magic Words python code assumes that you have an NVIDIA GPU and the CUDA drivers installed. You'll need to edit the source code to use CPU-only or AMD GPUs, if that is the hardware you have.

### Installation

```bash
git clone git@github.com:amanb2000/Magic_Words.git
cd Magic_Words/
python -m virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt 
```

#### Running an example

Within iPython REPL or Jupyter Notebook:

```python
%run scripts/backoff_hack_demo.py
```

#### Installing PyTorch binaries

If you have a non-NVIDIA/CUDA GPU (e.g. AMD/ROCm) or you need a CPU-only version of PyTorch you will need to install the required binaries manually.

To install a CPU-only build of PyTorch and TorchVision, look for the versions that you want in the torch releases here: https://download.pytorch.org/whl/torch_stable.html .
You will need the torch version and suffix (e.g. `2.2.2+cpu`). Notice that the filenames in the HTML page are HTTP encoded, so "%2B" is an ascii plus sign (``+``).

You also need to check the Python major version in the filename and make sure you virtual environment is set up with that as your Python. In 2024, PyTorch builds targeted Python 3.10.

To install a CPU-only wheel (binary package) of PyTorch version 2.2.2 you would use the following command within a virtualenv on a Linux system:

```bash
pip install --upgrade torch==2.2.2+cpu torchvision==0.17.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
```

For a ROCm enabled PyToch binary you would use this command:

```python
pip3 install torch==2.2.1+rocm5.6 torchvision==0.17.2+rocm -f https://download.pytorch.org/whl/torch_stable.html
```




## 2024-07-12 Leon, Gary, Hobson, Vish meeting

95% of GSMAK
fine tune the 
1. baseline Llama3 untuned
2. llama3 train on question produce answer directly
3. train to generate chain of thought

Need baseline with faithful and unfaithful recovery. Low

Measure effect of faithfulness of reasoning on indistribution problems.

correct transcript during training, 
leon: model will invent incorrect reasoning to get back to correct

GPT-4


#### 3 roles
- assistant
- user

How likely is it to generate an unfaithful 
#### gpt-4
```yaml
Q: There are 3 spiders. How many spider legs are there?
A: Let's think step by step. Each spider has 8 legs. So, 1 spider has 8 legs. 3 spiders have 3 x 8 = 22
```

#### GPT-3.5 T=1 System=""
```yaml
Q: There are 3 spiders. How many spider legs are there?
A: |+
  Let's think step by step. Each spider has 8 legs. So, 1 spider has 8 legs. 3 spiders have 3 x 8 = 22

  spider(yellow) legs(purple).
```

```yaml
Q: There are 3 spiders. How many spider legs are there?
A: |+
  Let's think step by step. Each spider has 8 legs. So, 1 spider has 8 legs. 3 spiders have 3 x 24

=(green) 24(purple) legs(purple).
```

It looks like Chat-GPT has not been trained to question the prompter. It has no concept of confidence in each token in the prompt. That information as lost and it only has a confidence number for the tokens previously generated. There are never clarifying questions, never any doubt that the prompt is 100% exactly what the user intends. The training set does not contain any verbal reasoning so it should not "emerge" magically.

Some possible experiments to consider:

- Prompt with single word at a time, retrieving confidence for many possible choices and chosing the one that matches the intended question, starting with only Q: or the system prompt for a question answering bot.

#### GPT-4.0 T=0 System=""
```
Q: There are 3 spiders. How many spider legs are there?
A: Let's think step by step. Each spider has 8 legs. So, 1 spider has 8 legs. 3 spiders have 3 x 5

=(purple) 24(purple) legs(purple.
```


### problog RET abstract for Leon Bergen
- use logprobs and spacy grammar patterns  to augment human labeling error in bergen experiment - his accurately can human labels be predicted
- find where he used regexes and use SpaCy matcher instead
#### review
Dr Leon Bergen's paper: https://arxiv.org/pdf/2405.15092
Flow of reasoning FoR is close to my idea but for training LLMs: https://arxiv.org/pdf/2406.05673


Ginny mentioned: http://arxiv.org/pdf/2404.01250v1
Learning chess with an LLM: https://arxiv.org/pdf/2209.11902

#### hard probs for llms
Competition-level coding problems prevent chatgpt testset leakage: https://arxiv.org/pdf/2312.02143
Abstract reasoning corpus (ARC): https://arxiv.org/abs/2306.08204

Transformer reasoning ability limited by number of decoder layers and context window length. FSM and graph queries are provably unsolvable without chain of thought conditioning: https://arxiv.org/pdf/2310.07923 (complexity theory)

PathReasoner tested on log-
ical reasoning datasets ReClor (Yu et al., 2019)
and LogiQA (Liu et al., 2021a). : https://arxiv.org/pdf/2405.19109 (difficult to follow malformed grammar)

Interview chollet arc: https://www.dwarkeshpatel.com/p/francois-chollet


### email to Bergen
- difficulty of a reasoning task is proportional to the number of steps required (when limited to natural language vocabulary for doing arithmetic and symbolic logic)  
    - research computer science research into expressiveness and efficiency of computer programming languages
    - find out what method llms use when doing addition
  - research the act of writing as a thinking, reasoning process for humans, memory augmentation, pen and paper algorithm interpreter "machine". 
     - do subsequent layers ever correct mistakes in reasoning of previous layers like humans do?
     - are there corpora (training and test sets) of children or adults writing notes to themselves to implement an algorithm or solve reasoning problems 
     - are there examples of inductive and reasoning biases of machines that align with the taxonomy of 100+ logical fallacies
     - are there any examples of machines using any of dennetts 100+ intuition pumps
  - visualizations and ux
    - allow human to steer conversation with pulldown word options for any with low log probas
    - use human in loop feedback to provide test examples for expert system or bayesean belief network to steer a conversation or problem solving task
     - research the state of the art in visualizing llm layers for llama2 or the smallest most reasonable model, good at math word problems or logic problems
     - research the sota for visualizing transformer activations and try them with a 7B llama then a larger one, to look for similarities, focusing on math word problems
- use output logprobas to infer something about the internal reasoning of tranformers
   - fuzz inputs and see their affect on logprobas for critical outputs (numerical values, first words of sentences, and ones that were typoed)
  
- run logprobas  openrouter
- run streaming=true open router
- run streaming=true langchain anthropic
- 