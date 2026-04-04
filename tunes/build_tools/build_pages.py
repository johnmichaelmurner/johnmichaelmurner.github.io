from string import Template
from glob import glob
from pathlib import Path
from sjkabc import Parser
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
paths = [x for x in glob(abc_path_str)]
for abc in paths:
    dest_path = str(path.parent) + '/' + str(Path(abc).name).replace('.abc', '.html').replace("'", "")
    with open(abc, 'r') as f:
        abc_notation = f.read()
    try:
        for tune in Parser(abc_notation):
            temp = Template(tune_template)
            result = temp.substitute(abc=abc_notation,title=f"{tune.title[0]} {tune.key[0]} {tune.metre[0]}")
            with open(dest_path,'w') as f:
                f.write(result)
            files_names.append(str(Path(dest_path).name))
            tunes[str(Path(dest_path).name)] = tune
    except Exception as e:
        ValueError(f"Unable to parse {abc} {e}")

files_names.sort()
home_page_list = []
for f in files_names:
    anchor = Template(anchor_template)
    tune = tunes[f]
    result = anchor.substitute(file_name=f, tunename=str(tune.title[0]), tunekey=str(tune.key[0]), tunemeter=str(tune.metre[0]))
    home_page_list.append(result)

home = Template(home_template)
result = home.substitute(tunes="".join(home_page_list))
home_path = str(path.parent / 'index.html')
with open(home_path, 'w') as f:
    f.write(result)