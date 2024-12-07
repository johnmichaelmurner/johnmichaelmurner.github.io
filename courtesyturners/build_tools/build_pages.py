from string import Template
from glob import glob
from pathlib import Path
from pyabc.pyabc import Tune
path = Path(__file__).parent

with open(path / 'anchor.html', 'r') as f:
    anchor_template = f.read()

with open(path / 'index.html', 'r') as f:
    home_template = f.read()

with open(path / 'tune.html', 'r') as f:
    tune_template = f.read()

abc_path_str = str(path.parent / 'abc/*')

files_names = []
tunes = {}
for abc in glob(abc_path_str):
    dest_path = str(path.parent) + '/' + str(Path(abc).name).replace('.abc', '.html')
    with open(abc, 'r') as f:
        abc_notation = f.read()
    tune = Tune(abc=abc_notation)
    tune.meter = tune.header.get('meter')
    temp = Template(tune_template)
    result = temp.substitute(abc=abc_notation,title=f"{tune.title} {tune.key} {tune.meter}")
    
    with open(dest_path,'w') as f:
        f.write(result)
    files_names.append(str(Path(dest_path).name))
    tunes[str(Path(dest_path).name)] = tune

files_names.sort()
home_page_list = []
for f in files_names:
    anchor = Template(anchor_template)
    tune = tunes[f]
    result = anchor.substitute(file_name=f, tunename=str(tune.title), tunekey=str(tune.key), tunemeter=str(tune.meter))
    home_page_list.append(result)

home = Template(home_template)
result = home.substitute(tunes="".join(home_page_list))
home_path = str(path.parent / 'index.html')
with open(home_path, 'w') as f:
    f.write(result)