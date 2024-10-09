#!/usr/bin/env bash

source ../../.venv/bin/activate
which python
# npm install -g reveal-md
themes='beige blood moon simple white-contrast black-contrast dracula night sky white black league serif solarized'

python -c "themes='${themes}'.split();themess='\n'.join(themes); print(input(f'Choose a theme:\n{themess}\n[{themes[0].strip()}]: ').strip().lower() or themes[0])"
theme=beige
if [[ -n "$1" ]] ; then
    theme=$1
fi
reveal-md RET_Effectively_Unreasonable_LLMs.md --theme=$theme
