# import os
from pathlib import Path
import re
from datetime import datetime

import numpy as np
import panel as pn
import tastymap as tm
from dotenv import load_dotenv
from treelib import Tree  # , Node
from jsonlines import jsonlines as jsl
import json

# import numpy as np
# from matplotlib import pyplot as plt
# from tastymap import cook_tmap, pair_tbar

from problog import api

# colorbar = cook_tmap(
#     tmap,
#     bounds=[0, 50, 100],
#     labels=["0.00", "0.50", "1.00"],
#     uniform_spacing=True,
# )


load_dotenv()

MODEL = 'gpt-3.5-turbo'
PRIVATE_DIR = Path(api.__file__).resolve().parent.parent.parent / 'data' / 'private'
PRIVATE_DIR.mkdir(exist_ok=True, parents=True)
assert PRIVATE_DIR.is_dir()

SYSTEM_PROMPT = """You are an smart AI assistant that knows math and does not halucenate.""".strip()


TMAP = tm.cook_tmap(
    ["red", "purple", "blue", "black"],
    reverse=False,
    num_colors=11,
    name='Token probability',
    hue=1,
    saturation=1,
    bad='',
    under='',
    over='',
    value=1)
# TMAP._repr_html_()
# <div style="vertical-align: middle;"><strong>Token probability</strong> </div>\
# <div class="cmap"><img alt="Token probability colormap" title="Token probability" style="border: 1px solid #555;"\
#       src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAgAAAABACAYAAABs"...\
# width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #000000ff;"></div></div>
COLORS = TMAP.to_model("hex")  # noqa
# array(['#ff0600', '#d90425', '#b3024b', '#8d0170', '#680097', '#4300be',
#        '#1e00e5', '#0500e5', '#040099', '#02004c', '#000000'], dtype='<U7')


aclient = api.get_aclient()
print('app.aclient:', aclient)
print('app.aclient.base_url:', aclient.base_url)
print('app.aclient.api-key:', aclient.api_key[:3], '...', aclient.api_key[-3:])


def color_by_logprob(text, log_prob, colors=COLORS):
    """ Add <span style='color: {color_hex}'> around text based on log probability < 0 and list of 100 colors"""
    # select index based on probability
    color_hex = colors[int(np.exp(log_prob) * (len(colors) - 1))]
    # Generate HTML output with the chosen color
    text.replace('"', '&quot;')
    # quote = '\'"'[int("'" in text)]  # use the quote symbol not already used within the text
    return f'<span style="color:{color_hex};">{text}</span>'


def color_by_prob(text, prob, colors=COLORS):
    """ Add <span style='color: {color_hex}'> around text based on linear 0 < probability < 1 and list of 100 colors

    >>> color_by_prob("hello", 1.0)
    "<span style='color: 0xFFFFFF;'>hello</span>"
    """
    if prob < 0:
        prob = np.exp(prob)
    if 0 < prob < 1:
        prob = np.round(prob * 100, 2)
    # select index based on probability
    # FIXME: vectorize this operation so that it works on an array of texts and probs np.astype(int) or similar
    color = colors[int(prob // (100 / (len(colors) - 1)))]
    quote = '\'"'[int("'" in text)]  # use the quote symbol not already used within the text
    return f'<span style={quote}color: {color};{quote}>{text}</span>'


def custom_serializer(content):
    """ Strip <span> tags?

    >>> custom_serializer("<span style='color: 0xFFFFFF;'>{text}</span>)
    """
    pattern = r"<span.*?>(.*?)</span>"
    # TODO: `try: return next(re.finditer(pattern, content))`
    matches = re.findall(pattern, content, re.DOTALL)
    if not matches:
        return content
    return ''.join(matches)


def choices_html_table(token_prob_hist):
    s = ''
    s += '<table>\n'
    s += '<tr>'
    for t in token_prob_hist:
        s += '<td>' + t[0] + '</td>'
    s += '</tr>\n'
    # chosen token is not always the first (most probable) one in num_top_logprobs
    s += '<tr>'
    for t in token_prob_hist:
        s += '<td>' + next(x for x in t[-1]) + '</td>'
    s += '</tr>\n'
    s += '<tr>'
    for t in token_prob_hist:
        s += '<td>' + next(x for x in t[-1] if x != t[0]) + '</td>'
    s += '</tr>\n'
    s += '</table>\n'
    return s


# tree = Tree()
# tree.create_node("Harry", identifier=0, parent=None)  # No parent means its the root node
# tree.create_node("Jane", identifier=1, parent=0)


# #       [tok0, tok1, tok2...]
# nodes = []
# #       [(srcid, destid, prob)]
# edges = []
# srcid = None


class Graph():
    def __init__(self, nodes=None, edges=None, token_tree=None, srcid=None):
        self.nodes = []
        self.edges = []
        if token_tree is not None:
            self.from_token_tree(token_tree)
        elif nodes is not None and edges is not None:
            self.nodes = list(nodes).copy()
            self.edges = list(edges).copy()

    def from_token_tree(self, token_tree):
        self.nodes = ['']
        self.edges = []
        srcid = 0
        for choices in token_tree:
            destid = len(self.nodes)
            token_probs = list(choices.items())
            for i, (tok, prob) in enumerate(token_probs):
                self.nodes.append(tok)
                self.edges.append((srcid, destid + i, prob))
            srcid = destid

    def ascii_tree(self):
        self.tree = Tree()
        self.tree.create_node(
            tag="<SOS>", identifier=0, parent=None,
            data=dict(prob=1, space='', chunk='', token='')
        )
        # parentid = -1
        previous_srcid = -1
        for srcid, destid, prob in self.edges:
            # if parentid == srcid:
            #     continue
            # parentid = srcid
            chunk = self.nodes[destid]
            space = ' ' * int(chunk.startswith(' '))
            desttok = tag = chunk[len(space):]
            if previous_srcid != srcid:
                tag = f'**{desttok}**'
                previous_srcid = srcid
            self.tree.create_node(
                tag=tag,
                identifier=destid,
                parent=srcid,
                data=dict(prob=prob, space=space, chunk=chunk, token=desttok)
            )
        # parentid = -1
        # for srcid, destid, prob in self.edges:
        #     if parentid != srcid:
        #         continue
        #     parentid = srcid
        #     chunk = self.nodes[destid]
        #     space = ' ' * int(chunk.startswith(' '))
        #     desttok = chunk[len(space):]
        #     self.tree.create_node(
        #         tag=desttok,
        #         identifier=destid,
        #         parent=srcid,
        #         data=dict(prob=prob, space=space, chunk=chunk, token=desttok)
        #     )
        return self.tree

    # def add_node(self, token_probs={}):
    #     self.srcid = self.srcid or 0  # <SOS> token, id = '', 0
    #     print('=' * 80)
    #     token_probs = list(token_probs.items())
    #     token = token_probs[0][0]
    #     print(token + '\n', token_probs)
    #     self.nodes[self.srcid] = token
    #     next_srcid = self.srcid + 1  # self.srcid is the last destid for the previous token chosen by LLM
    #     for i, (token, prob) in enumerate(token_probs):
    #         destid = next_srcid + i
    #         print(self.srcid, '->', prob, '->', destid, token)
    #         self.nodes[destid] = token
    #         self.edges[self.srcid] = (destid, prob)
    #     self.srcid = next_srcid
    #     return self

    def __str__(self):
        self.tree = None
        if len(self.nodes) and len(self.edges):
            self.tree = self.ascii_tree()
        return str(self.tree)

    def __repr__(self):
        return json.dumps(
            dict(
                nodes=self.nodes,
                edges=self.edges,
                tree=str(self)
            ), indent=4
        )


async def generate_tokens(
        prompt: str,
        model: str = MODEL,
        role: str = 'user',
        top_logprobs: int = 5,
        stream: bool = True,
        temperature: float = 0.,
):
    """ Send prompt to LLM API and parse the response into a dict of {token: prob,..} (chosen one first)"""
    logprobs = bool(top_logprobs)
    data = dict(
        model=model,
        role=role,
        prompt=prompt,
        stream=stream,
        logprobs=logprobs or top_logprobs,
        top_logprobs=top_logprobs,
        temperature=temperature,
        requested=datetime.now().isoformat(),
        responded=[])
    response = await aclient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": role, "content": prompt}],
        stream=stream,
        logprobs=logprobs,
        top_logprobs=top_logprobs,
        temperature=temperature
    )
    chosen_tokens = []
    chosen_token_logprobs = []
    data['token_tree'] = []  # [{'The': .7, 'I': .3}, {'President': .9, 'president': .1}, ...]

    async for chunk in response:
        data['responded'].append(datetime.now().isoformat())
        choice = chunk.choices[0]
        chosen_token = str(choice.delta.content)
        if not choice.delta.content:
            continue
        chosen_tokens.append(chosen_token)
        logprobs = choice.logprobs
        token_probs = {}
        chosen_token_logprobs.append(logprobs.content[0].logprob)
        token_probs[chosen_token] = np.exp(chosen_token_logprobs[-1])
        if logprobs and len(logprobs.content):
            for lp in logprobs.content[0].top_logprobs:
                # to ensure chosen token remains first in the dict even if it is not most likely
                if lp.token not in token_probs:
                    token_probs[lp.token] = np.exp(lp.logprob)
        data['token_tree'].append(token_probs)
        # probs = parse_token_probs(choice.logprobs)
        """ ChoiceLogprobs(content=[ChatCompletionTokenLogprob(
                token='.', bytes=[46], logprob=-0.000528607, top_logprobs=[
                    TopLogprob(token='.', logprob=-0.000528607),
                    TopLogprob(token=' in', logprob=-7.758082),
                    TopLogprob(token=',', logprob=-9.996801),
                    TopLogprob(token='.\n\n', logprob=-10.169836),
                    TopLogprob(token='.\n', logprob=-12.029373),
                    TopLogprob(token=' and', logprob=-12.782852),
                    TopLogprob(token=' for', logprob=-12.989118),
                    TopLogprob(token=' (', logprob=-13.350204),
                    TopLogprob(token="'s", logprob=-14.024787),
                    TopLogprob(token=' as', logprob=-14.482371),
                    TopLogprob(token=' to', logprob=-14.907305), ...,
                    TopLogprob(token='.The', logprob=-16.181864)])])
        """
    data['chosen_chunks'] = chosen_tokens
    data['chosen_chunks_html'] = [color_by_logprob(ct, lp) for (ct, lp) in zip(chosen_tokens, chosen_token_logprobs)]
    data['response'] = ''.join(chosen_tokens)
    data['response_html'] = ''.join(data['chosen_chunks_html'])
    # data['chosen_tokens'] = [t.strip(' ') for t in chosen_tokens]
    return data

    # tokens_with_probs.append(token_probs)


def parse_token_probs(logprobs):
    """
    [ChatCompletionTokenLogprob(
        token='As',
        bytes=[65, 115],
        logprob=-0.45121273,
        top_logprobs=[
            TopLogprob(
                token='As',
                bytes=[65, 115],
                logprob=-0.45121273),
            TopLogprob(
                token='I', bytes=[73], logprob=-1.2444047),
            TopLogprob(token='The', bytes=[84, 104, 101], logprob=-2.737067),
            TopLogprob(token='It', bytes=[73, 116], logprob=-5.0746527),
            TopLogprob(token='There', bytes=[84, 104, 101, 114, 101], logprob=-6.687793),
            TopLogprob(token='Joe', bytes=[74, 111, 101], logprob=-7.3963213),
            TopLogprob(token='Sorry', bytes=[83, 111, 114, 114, 121], logprob=-7.7406054),
            TopLogprob(token='This', bytes=[84, 104, 105, 115], logprob=-7.792281),
                TopLogprob(token='Currently', bytes=[67, 117, 114, 114, 101, 110, 116, 108, 121], logprob=-7.8929625),
                TopLogprob(token='My', bytes=[77, 121], logprob=-8.469665),
                TopLogprob(token='Please', bytes=[80, 108, 101, 97, 115, 101], logprob=-8.489194),
                TopLogprob(token='In', bytes=[73, 110], logprob=-9.22366),
                TopLogprob(token='At', bytes=[65, 116], logprob=-9.364764),
                TopLogprob(token='Since', bytes=[83, 105, 110, 99, 101], logprob=-9.518352),
                TopLogprob(token='That', bytes=[84, 104, 97, 116], logprob=-10.680621),
                TopLogprob(token='Donald', bytes=[68, 111, 110, 97, 108, 100], logprob=-10.718347),
                TopLogprob(token='President', bytes=[80, 114, 101, 115, 105, 100, 101, 110, 116], logprob=-10.904269),
                TopLogprob(token='Unfortunately', bytes=[85, ... 121], logprob=-10.986873),
                TopLogprob(token='K', bytes=[75], logprob=-11.12283),
                TopLogprob(token='For', bytes=[70, 111, 114], logprob=-11.195319)])]
    """
    # [[vars(c) for c in chunk.choices[0].logprobs.content] for chunk in response]]
    if hasattr(logprobs, 'choices'):
        return parse_token_probs(logprobs.choices[0])
    if hasattr(logprobs, 'logprobs'):
        return parse_token_probs(logprobs.logprobs)
    if isinstance(logprobs, list):
        return parse_token_probs(logprobs[0])
    if hasattr(logprobs, 'top_logprobs'):
        return {x.token: np.exp(x.logprob) for x in getattr(logprobs.top_logprobs.content, 'top_logprobs', [])}
    raise NotImplementedError
    return logprobs


async def chat(
        prompt="Which chatbot won the Loebniz prize?",
        model=MODEL,
        history_path=PRIVATE_DIR / 'chat_history.jsonlines',
        top_logprobs=2,
        temperature=0,
):
    data = await generate_tokens(
        prompt=prompt, model=model,
        top_logprobs=top_logprobs, temperature=temperature)
    with jsl.open(history_path, 'a') as fout:
        fout.write(data)
    return data


def app():
    async def respond_to_input(
            contents: str,
            user: str,
            instance: pn.chat.ChatInterface
    ):
        # TODO: pulldown for model_name
        # TODO: pulldown for LLM API URL
        # TODO: orange or red for lowest logprob, dark blue for highest logprob

        if api_key_input.value:
            aclient.api_key = api_key_input.value
        elif not getattr(aclient, 'api_key', None):
            instance.send("Please provide an LLM API key", respond=False, user="ChatGPT")
        # add system prompt
        messages = []
        if system_prompt_widget.value:
            messages.append({"role": "system", "content": system_prompt_widget.value})
        # gather messages for memory
        if memory_toggle.value:
            messages += instance.serialize(custom_serializer=custom_serializer)
        else:
            messages.append({"role": "user", "content": contents})
        # call API
        response = await aclient.chat.completions.create(
            model=model_selector.value,
            messages=messages,
            stream=True,
            logprobs=True,
            temperature=temperature_input.value,
            max_tokens=max_tokens_input.value,
            seed=seed_input.value,
        )
        # stream response
        message = ""
        async for chunk in response:
            choice = chunk.choices[0]
            content = choice.delta.content
            log_probs = choice.logprobs
            if content and log_probs:
                log_prob = log_probs.content[0].logprob
                message += color_by_logprob(content, log_prob)
                yield message

    pn.extension()
    provider_pulldown = pn.widgets.Select(
        name="Provider",
        options=list(api.endpoints.keys()),
        width=100,
    )
    api_key_input = pn.widgets.PasswordInput(
        name="API Key",
        placeholder="sk-...",
        width=80,
    )

    system_prompt_widget = pn.widgets.TextAreaInput(
        name="System Prompt",
        placeholder="You are an AI assistant ...",
        value=SYSTEM_PROMPT,
        cols=3,
        rows=4,
        resizable='height',
        min_width=256,
        max_width=512,
        auto_grow=True,  # grow in height to match input text
    )
    model_selector = pn.widgets.Select(
        name="Model",
        options=["gpt-3.5-turbo", "gpt-4"],
        width=150,
    )
    temperature_input = pn.widgets.FloatInput(
        name="Temperature", start=0, end=2, step=0.01, value=1, width=100
    )
    max_tokens_input = pn.widgets.IntInput(name="Max Tokens", start=0, value=256, width=100)
    seed_input = pn.widgets.IntInput(name="Seed", start=0, end=100, value=0, width=100)
    memory_toggle = pn.widgets.Toggle(
        name="Include Memory", value=False, width=100, margin=(22, 5)
    )
    chat_interface = pn.chat.ChatInterface(
        callback=respond_to_input,
        callback_user="ChatGPT",
        callback_exception="verbose",
    )
    page = pn.Column(
        pn.Row(
            provider_pulldown,
            api_key_input,
            model_selector,
            temperature_input,
            max_tokens_input,
            seed_input,
            memory_toggle,
            align="start",
        ),
        pn.Row(
            system_prompt_widget,
            TMAP._repr_html_(),
            align="start"
        ),
        chat_interface,
    )
    return page


if __name__ == '__main__':
    page = app()
    page.show()
    # ans = input('Launch a flask app (Y/[N]) ? ') + ' '
    # if (ans or ' ')[0].lower() == 'y':
    #     page.show()
