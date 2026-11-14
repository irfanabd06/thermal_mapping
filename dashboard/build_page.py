import json, sys
survey = {}
for line in open("survey.txt"):
    k, v = line.split(); survey[k] = float(v)
assert len(survey) == 57 and list(survey) == [f"T{i}" for i in range(1, 58)]
html = open("template.html").read()
html = html.replace("__MODEL__", open("out/model.json").read()).replace("__SURVEY__", json.dumps(survey, separators=(",", ":")))
open("out/index.html", "w").write(html)
v = list(survey.values())
print("n", len(v), "mean", round(sum(v)/len(v), 3), "max", max(v), "min", min(v), "hot>=39", sum(x >= 39 for x in v))
main = [survey[f"T{i}"] for i in range(1, 37)]; wing = [survey[f"T{i}"] for i in range(40, 58)]
print("main mean", round(sum(main)/36, 3), "wing mean", round(sum(wing)/18, 3))
for r in (1, 2, 3):
    m = [survey[f"T{3*k+r}"] for k in range(12)]; print("main row", r, round(sum(m)/12, 3))
print("bytes", len(html))
