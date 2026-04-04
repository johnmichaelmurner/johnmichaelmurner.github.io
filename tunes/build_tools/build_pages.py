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
chords_path = path.parent.parent / 'chords'

chords_index_template = Template(
        """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="../style.css"/>
    <script src="../nav.js" type="text/javascript"></script>
    <title>Chords</title>
    <script>
        function myFunction() {
            var input, filter, table, tr, td, i, txtValue;
            input = document.getElementById("myInput");
            filter = input.value.toUpperCase();
            table = document.getElementById("myTable");
            tr = table.getElementsByTagName("tr");
            for (i = 0; i < tr.length; i++) {
                td = tr[i].getElementsByTagName("td")[0];
                if (td) {
                    txtValue = td.textContent || td.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        tr[i].style.display = "";
                    } else {
                        tr[i].style.display = "none";
                    }
                }
            }
        }
    </script>
</head>
<body>
    <header class="site-header">
        <a class="site-brand" href="../index.html">johnmichaelmurner.com</a>
        <button class="nav-toggle" type="button" aria-label="Toggle navigation" aria-expanded="false">
            <span class="hamburger-icon" aria-hidden="true"><span></span><span></span><span></span></span>
        </button>
        <nav class="site-nav" aria-label="Main navigation">
            <a href="../tunes/index.html">Tunes</a>
            <a href="index.html">Chords</a>
            <a href="../lexingtionopencontraband/index.html">Open Band Tunes</a>
        </nav>
    </header>
    <div class="container">
        <input type="text" id="myInput" onkeyup="myFunction()" placeholder="Search chords.." title="Type in a chord name">
        <table id="myTable">
            $chords
        </table>
    </div>
</body>
</html>
"""
)

chords_anchor_template = Template(
        """<tr>
        <td><a href="$file_name">$chord_name</a></td>
</tr>
"""
)

chord_page_template = Template(
        """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="../style.css"/>
    <script src="../nav.js" type="text/javascript"></script>
    <title>$title</title>
    <style>
        .chord-image {
            display: block;
            width: 100%;
            height: auto;
            max-width: 100%;
            max-height: calc(100vh - 140px);
            object-fit: contain;
            background: #ffffff;
            padding: 10px;
            border-radius: 4px;
        }
        @media (orientation: landscape) {
            .container {
                max-width: 100%;
            }
            .chord-image {
                max-height: calc(100vh - 110px);
            }
        }
    </style>
</head>
<body>
    <header class="site-header">
        <a class="site-brand" href="../index.html">johnmichaelmurner.com</a>
        <button class="nav-toggle" type="button" aria-label="Toggle navigation" aria-expanded="false">
            <span class="hamburger-icon" aria-hidden="true"><span></span><span></span><span></span></span>
        </button>
        <nav class="site-nav" aria-label="Main navigation">
            <a href="../tunes/index.html">Tunes</a>
            <a href="index.html">Chords</a>
            <a href="../lexingtionopencontraband/index.html">Open Band Tunes</a>
        </nav>
    </header>
    <div class="container">
        <h1>$title</h1>
        <img class="chord-image" src="$svg_name" alt="$title" />
    </div>
</body>
</html>
"""
)

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


chord_files = sorted(glob(str(chords_path / '*.svg')))
chord_rows = []

for chord in chord_files:
    chord_name = Path(chord).stem.replace('_', ' ')
    chord_file_name = Path(chord).name
    dest_name = chord_file_name.replace('.svg', '.html').replace("'", '')
    dest_path = chords_path / dest_name

    chord_page = chord_page_template.substitute(title=chord_name, svg_name=chord_file_name)
    with open(dest_path, 'w') as f:
        f.write(chord_page)

    row = chords_anchor_template.substitute(file_name=dest_name, chord_name=chord_name)
    chord_rows.append(row)

chords_index = chords_index_template.substitute(chords=''.join(chord_rows))
with open(chords_path / 'index.html', 'w') as f:
    f.write(chords_index)