import os
import re

if not os.path.isdir("Sherlock"):
    os.mkdir("Sherlock")

modules: list[str] = []
for file in sorted(os.listdir("novels")):
    if file.endswith(".txt"):
        with open("novels/" + file) as f:
            title = f.readline().strip()
            [num, first_word, *rest] = file.split("_")
            safe_word = re.match(r"^[A-Za-z]+", first_word)
            if safe_word is None:
                raise Exception("Not a name: " + first_word)
            print(safe_word[0] + num + ": " + title)
            modules += [safe_word[0] + num]

            with open("Sherlock/" + safe_word[0] + num + ".lean", "w+") as out:
                out.writelines(
                    [
                        "import VersoManual\n",
                        "open Verso.Genre Manual\n\n",
                        f'#doc (Manual) "{title}" =>\n',
                        "%%%\n",
                        f'tag := "{safe_word[0] + num}"\n'
                        "%%%\n",
                    ]
                )
                has_parts = False
                for line in f.readlines():
                    part = re.match(r"^PART [0-9]+: (.*)", line)
                    if part:
                        has_parts = True
                        out.write("# " + part[1] + "\n")
                        continue
                    
                    chapter = re.match(r"^Chapter [0-9]+--(.*)", line)
                    if chapter:
                        out.write(("## " if has_parts else "# ") + chapter[1] + "\n")
                        continue

                    out.write(line.replace("[", "\\[").replace("]", "\\]").replace("--", "—"))


for file in sorted(os.listdir("stories")):
    if file.endswith(".txt"):
        with open("stories/" + file) as f:
            title = f.readline().strip()
            [num, _collection, _chapter, first_word, *rest] = file.split("_")
            safe_word = re.match(r"^[A-Za-z]+", first_word)
            if safe_word is None:
                raise Exception("Not a name: " + first_word)
            print(safe_word[0] + num + ": " + title)
            modules += [safe_word[0] + num]

            with open("Sherlock/" + safe_word[0] + num + ".lean", "w+") as out:
                out.writelines(
                    [
                        "import VersoManual\n",
                        "open Verso.Genre Manual\n\n",
                        f'#doc (Manual) "{title}" =>\n',
                        "%%%\n",
                        f'tag := "{safe_word[0] + num}"\n'
                        "%%%\n",
                    ]
                )
                for line in f.readlines():
                    out.write(line.replace("[", "\\[").replace("]", "\\]").replace("--", "—"))

if False:
    with open("Sherlock.lean", "w+") as out:
        out.write("import VersoManual\n")
        for module in modules:
            out.write(f"import Sherlock.{module}\n")
        out.writelines(
            [
                "open Verso.Genre Manual\n\n",
                '#doc (Manual) "The Sherlock Holmes Stories" =>\n',
                "By Arthur Conan Doyle\n\n"
            ]
        )
        for module in modules:
            out.write("{include Sherlock." + module + "}\n")
