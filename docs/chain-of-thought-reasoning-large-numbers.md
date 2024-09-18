# CoT reasoning project (problog webapp) 

## Draft paper

### Abstract

Early on in LLM development, the emergence of LLM reasoning ability at larger language model sizes was hypothesized and evaluated, without consensus among researchers at institutions responsible for the largest LLM providers. 
LLM reasoning ability has been shown to be error prone and math word problems (MWP) provide a useful benchmark for detecting these errors by evaluating the generation of step-by-step reasoning explanations.
However the limited numerical range, logic diversity, and range of difficulty (for human problem solvers) in MWP datasets, limit the conclusions that can be drawn from evaluation on MWP datasets 
We also found that some benchmark datasets, such as GSM8k, contain errors in their reasoning explanations that can cin both the training and 
several approaches have achieved significant improvements in MATH reasoning ability

### References
- [arXiv:2405.15092](https://arxiv.org/abs/2405.15092)
  - Dissociation of Faithful and Unfaithful Reasoning in LLMs
  - Authors: [Evelyn Yee](https://arxiv.org/search/?searchtype=author&query=Yee%2C+E), [Alice Li](https://arxiv.org/search/?searchtype=author&query=Li%2C+A), [Chenyu Tang](https://arxiv.org/search/?searchtype=author&query=Tang%2C+C), [Yeon Ho Jung](https://arxiv.org/search/?searchtype=author&query=Jung%2C+Y+H), [Ramamohan Paturi](https://arxiv.org/search/?searchtype=author&query=Paturi%2C+R), [Leon Bergen](https://arxiv.org/search/?searchtype=author&query=Bergen%2C+L)
  - Sep 2024
- [arXiv:2304.15004](https://arxiv.org/abs/2304.15004)
  - Are Emergent Abilities of Large Language Models a Mirage?
  - Authors: [Rylan Schaeffer](https://arxiv.org/search/?searchtype=author&query=Schaeffer%2C+R), [Brando Miranda](https://arxiv.org/search/?searchtype=author&query=Miranda%2C+B), [Sanmi Koyejo](https://arxiv.org/search/?searchtype=author&query=Koyejo%2C+S)
  - May 2023
- [arXiv:2409.03563](https://arxiv.org/pdf/2409.03563)
  - 100 instances is all you need: predicting the success of a new LLM on unseen data by testing on a few instances
  - Authors: [Lorenzo Pacchiardi](https://arxiv.org/search/?searchtype=author&query=Pacchiardi%2C+L), [Lucy G. Cheke](https://arxiv.org/search/?searchtype=author&query=Cheke%2C+L+G), [José Hernández-Orallo](https://arxiv.org/search/?searchtype=author&query=Hern%C3%A1ndez-Orallo%2C+J)
  - Sep 2024
- [arXiv:2409.06173](https://arxiv.org/abs/2409.06173)
  - Larger Language Models Don't Care How You Think: Why Chain-of-Thought Prompting Fails in Subjective Tasks
  - Authors: [Georgios Chochlakis](https://arxiv.org/search/?searchtype=author&query=Chochlakis%2C+G), [Niyantha Maruthu Pandiyan](https://arxiv.org/search/?searchtype=author&query=Pandiyan%2C+N+M), [Kristina Lerman](https://arxiv.org/search/?searchtype=author&query=Lerman%2C+K), [Shrikanth Narayanan](https://arxiv.org/search/?searchtype=author&query=Narayanan%2C+S)

### Contributions
- Parameterized GSM8k dataset
- evaluation of open source and proprietary LLMs on large number math word problems 
  - approx num of MWP in training set
  - diversity of MWPs in training set
- programmatic generation of MWPs with
  - parameterized numbers and formulae required to solve the problem (a.la Tiny-GSM)
  - arbitrarily large number word problems
  - arbitrary named entity references and pronouns
- programmatic generation of difficulty-scaled MWPs
  - number of words, characters, digits, sentences, numbers, BPE tokens (question and answer)
  - average character-length of sentences
  - number of parts of speech
  - reading grade level score
  - number of conjunctions and conditions and negations and other POS labels
  - scaled difficulty of numerical values
    - magnitude of numerical values
    - LLM accuracy rate weighted by size and how many MWPs in training set and whether finetuned for MWP
    - int vs rational number vs irrational numbers in question and/or answer
    - fractions utilized in MWP question
    - floating point or rational number values in MWP answer
  - familiarity and simplicity of numercial values:
      - divisible by 2
      - divisible by 10
      - divisible by 5
      - divisible by 3
      - divisible by 12 (specific to Western culture?)
      - cumsum([x // i == x / i for i in [2, 10, 100, 1000, 5, 3, 12, 9, 11, 7, 13])
      - cumsum([log(x, i) == int(log(x, i)) for i in [2, 10, 5, 3]]) # enumerate and 
      - number of integer digits in question and answer
  - minimum number of arithmetic operations required
    
  - bers
  - 
- MWP CoT reasoning evaluation metric
  - POS pattern similarity
  - numerical value similarity
  - ? logical pattern equivalence 
- programmatic generation of distractor noun and verb phrases for MWP training set data augmentation
- programmatic generation of culturally diverse proper nouns
- programmatic generation of culturally robust pronouns

### Meeting notes

See notes: [problog/docs/chain-of-thought-reasoning-large-numbers.md](https://github.com/hobson/problog/blob/main/docs/chain-of-thought-reasoning-large-numbers.md)

### References

#### longer math word problems (E-GSM)
- [arXiv:2405.14804](https://arxiv.org/abs/2405.14804)
  - Can LLMs Solve longer Math Word Problems Better?
  - Authors: [Xin Xu](https://arxiv.org/search/?searchtype=author&query=Xu%2C+X), [Tong Xiao](https://arxiv.org/search/?searchtype=author&query=Xiao%2C+T), [Zitong Chao](https://arxiv.org/search/?searchtype=author&query=Chao%2C+Z), [Zhenya Huang](https://arxiv.org/search/?searchtype=author&query=Huang%2C+Z), [Can Yang](https://arxiv.org/search/?searchtype=author&query=Yang%2C+C), [Yang Wang](https://arxiv.org/search/?searchtype=author&query=Wang%2C+Y)
  - notes
    Context Length Generalizability (CoLeG) metric for evaluating LLM ability to solve long MWPs
  questions
    - https://github.com/XinXU-USTC/CoLeG-Math (code is missing)
    - leakage? augmented dataset finetunes the LLM on long-context word problems
  contributions:
    - E-GSM dataset (longer GSM MWPs) - extension as an auxiliary task to fine-tune open source LLMs and release our fine-tuning dataset comprising 65K CoT data.
    - Experiment results for proprietary and open-source LLMs showing reasoning affected by context length
    - "Condition-Retrieving (CoRe) instructional prompt -- 'Let’s first understand the problem, then list all the known conditions which are formed by numbers or quantitative relationships along with their contexts from problem text, and identify the final goal of the problem. { Other prompting method }'"
      - notes
    - Related code: https://github.com/XinXU-USTC/R2PE
    - Repository missing:  
      - extended math word problem dataset used llms to extend context length
      - favorable results seem to rely on cheating (data leakage)
    - CoRe and extension have demonstrated their strong generalization on several MWP benchmarks.
    - LLM evaluation metric and benchmark dataset for solving long MWPs
    - instructional prompt for using proprietary LLMs to solve long MWPs
    - data augmentation task approach for long MWP
  - questions:
      - is there data is developed to improve CoLeG. Our comprehensive results demonstrate the effectiveness of our proposed methods, showing not only improved performance on E-GSM but also generalizability across several other MWP benchmarks. Our findings pave the way for future research in employing LLMs for complex, real-world applications, offering practical solutions to current limitations and opening avenues for further exploration of model generalizability and training methodologies. 
- [arXiv:2405.15092](https://arxiv.org/abs/2405.15092)
  - Dissociation of Faithful and Unfaithful Reasoning in LLMs
  - Authors: [Evelyn Yee](https://arxiv.org/search/?searchtype=author&query=Yee%2C+E), [Alice Li](https://arxiv.org/search/?searchtype=author&query=Li%2C+A), [Chenyu Tang](https://arxiv.org/search/?searchtype=author&query=Tang%2C+C), [Yeon Ho Jung](https://arxiv.org/search/?searchtype=author&query=Jung%2C+Y+H), [Ramamohan Paturi](https://arxiv.org/search/?searchtype=author&query=Paturi%2C+R), [Leon Bergen](https://arxiv.org/search/?searchtype=author&query=Bergen%2C+L)
  - Sep 2024
- [arXiv:2304.15004](https://arxiv.org/abs/2304.15004)
  - Are Emergent Abilities of Large Language Models a Mirage?
  - Authors: [Rylan Schaeffer](https://arxiv.org/search/?searchtype=author&query=Schaeffer%2C+R), [Brando Miranda](https://arxiv.org/search/?searchtype=author&query=Miranda%2C+B), [Sanmi Koyejo](https://arxiv.org/search/?searchtype=author&query=Koyejo%2C+S)
  - May 2023
- [arXiv:2409.03563](https://arxiv.org/pdf/2409.03563)
  - 100 instances is all you need: predicting the success of a new LLM on unseen data by testing on a few instances
  - Authors: [Lorenzo Pacchiardi](https://arxiv.org/search/?searchtype=author&query=Pacchiardi%2C+L), [Lucy G. Cheke](https://arxiv.org/search/?searchtype=author&query=Cheke%2C+L+G), [José Hernández-Orallo](https://arxiv.org/search/?searchtype=author&query=Hern%C3%A1ndez-Orallo%2C+J)
  - Sep 2024
- [arXiv:2409.06173](https://arxiv.org/abs/2409.06173)
  - Larger Language Models Don't Care How You Think: Why Chain-of-Thought Prompting Fails in Subjective Tasks
  - Authors: [Georgios Chochlakis](https://arxiv.org/search/?searchtype=author&query=Chochlakis%2C+G), [Niyantha Maruthu Pandiyan](https://arxiv.org/search/?searchtype=author&query=Pandiyan%2C+N+M), [Kristina Lerman](https://arxiv.org/search/?searchtype=author&query=Lerman%2C+K), [Shrikanth Narayanan](https://arxiv.org/search/?searchtype=author&query=Narayanan%2C+S)

## More papers to catalog

#### cumulative reasoning
https://arxiv.org/pdf/2308.04371

https://github.com/XinXU-USTC/cumulative-reasoning

https://github.com/XinXU-USTC/
- cumulative reasoning instead of cot claims 43% improvement on hard problems but these are selected Wikipedia FOL problems that cite their source, so problems llms trained on

- hs math problem dataset includes geometry problems and dot file format diagrams in answers

#### TinyGSM 

https://arxiv.org/pdf/2312.09241v1
12.3M math problem training set from gsm8k with Python solutions generated by gpt3.5 
Solutions verified (scored and then best selected) to get 81.5% accuracy (better than gpt 3.5) with 2.7B params for gsm8k (but overfit on it)
2 code examples in paper would be parametrizable and we should imitate their docstring problem statement format but as fstrings or jinja2 templates

#### Example parameterized GSM8k problem
```yaml
-
  N_00: 48
  question: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?
  question_template: Natalia sold clips to {N_00} of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?
  N_01_formula: 48/2
  N_01: 24
  answer: Natalia sold 48/2 = 24 clips in May. Natalia sold 48+24 = <<48+24=72>>72 clips altogether in April and May.
  answer_template: Natalia sold {N_00}/2 = {N_01} clips in May. Natalia sold 48+24 = <<48+24=72>>72 clips altogether in April and May.
  answer_numerical: 72
```

#### Datasets

- TinyGSM 
  - https://huggingface.co/datasets/TinyGSM/TinyGSM
  - can pair with gsm8k equivalents to parameterize python code
  - cross contamination only check 13 grams after removing punctuation,
    - should replace numbers with {number} before n-gram check
    - Should replace names with {name}
    - Should replace all tokens with POS 
    - replace named entities with named entity class
    - should resolve coreferences with SpaCy
    - calculate diversity of logic patterns
    - add python equation solving sym package code to solve
- GSM8k
  - Math word problem datasets GSM8K (Cobbe et al., 2021) 
  - https://paperswithcode.com/dataset/gsm8k
  - https://huggingface.co/datasets/openai/gsm8k
  - body+question answer+explanation+equation_annotation
  - answer contains math formula which can be evaluated in python
  - named entities (including pronouns) can be extracted and parameterized
  - nouns for objects can be parameterized as lists of possible alternatives
  - dereferencing of pronouns (coreference resolution) might be used to obfuscate the problem making it harder for machines
  - numbers in question can be paired with numbers in answer
- MAWPS (Koncel-Kedziorski et al.,
2016)
  - https://aclanthology.org/N16-1136.pdf
  - https://paperswithcode.com/dataset/mawps
  - https://github.com/sroy9/mawps (java)
  - https://huggingface.co/datasets/mwpt5/MAWPS/viewer
  - parameterized_question equation (N_00+N_01) answer (float) numbers (space delim floats)
- ASDiv (Miao et al., 2020)
  - https://huggingface.co/datasets/MU-NLPC/Calc-asdiv_a/viewer
  - data loader  https://huggingface.co/datasets/EleutherAI/asdiv/blob/main/asdiv.py
  - body+question equation answer grade-level
  - number words in question
  - grades 1-5
  - equation in HTML format chain of operations for calculator
- SVAMP (Patel et al., 2021) 
  - https://arxiv.org/pdf/2103.07191
  - https://huggingface.co/datasets/ChilleD/SVAMP/viewer
  - body, question, equation, answer (int)

#### Robustness Challenges
- irrelevant context - Shi et al. (2023a)
- new problems dissimilar to training set in wording (but not in math or logic)
- common sense knowledge
- numerical precision (robustness to large numbers)
- arithmetic complexity - number of steps for human to do arithmetic (1 digit vs 2 vs 3, powers of 10 vs 5 vs 2 vs 12 vs 6 vs 1 (prime numbers), addition vs multiplication, multiplication vs long division)
- https://huggingface.co/datasets/TinyGSM/TinyGSM
- 
#### Approaches
- verifier
- fine tuning
- tool use (calculator)