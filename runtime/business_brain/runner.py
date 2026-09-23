import argparse,json,re
from pathlib import Path
from runtime.business_brain.adapters.base import load_system_prompt
from runtime.business_brain.adapters.fixture import FixtureAdapter
from runtime.business_brain.models import Scenario
from runtime.business_brain.evaluator import evaluate_scenario

def load_scenarios(path):
    text=Path(path).read_text(encoding="utf-8")
    chunks=re.split(r"(?=^## (?:Scenario|X))",text,flags=re.M)
    out=[]
    for chunk in chunks:
        m=re.match(r"^## (Scenario|X)(?: |)(\\d+)? ?— ?(.+)$",chunk,re.M)
        if not m: continue
        kind,num,title=m.groups(); sid=("X"+num if kind=="X" else num)
        im=re.search(r"\\*\\*Input:\\*\\* (.+?)(?=\\n\\n|\\n##|$)",chunk,re.S)
        assertions=re.findall(r"^- (.+)$",chunk,re.M)
        if not assertions: continue
        input_text=im.group(1).strip() if im else ""
        fixture=input_text+"\n\nASSERTIONS_FOR_HARNESS:\n"+"\n".join(assertions)
        out.append(Scenario(sid,title,fixture,assertions,kind=="X"))
    return out

def run(system_prompt_path,scenario_path,output_path):
    system=load_system_prompt(system_prompt_path); scenarios=load_scenarios(scenario_path); adapter=FixtureAdapter(); results=[]
    for s in scenarios: results.append(evaluate_scenario(s,adapter.generate(system,s.input_text)))
    payload={"validation_mode":"HARNESS_VALIDATION","provider":"fixture","scenario_count":len(results),"results":[{"scenario_id":r.scenario_id,"title":r.title,"status":r.status,"provider":r.provider,"assertions":[a.__dict__ for a in r.assertion_results],"metadata":r.metadata} for r in results]}
    Path(output_path).parent.mkdir(parents=True,exist_ok=True); Path(output_path).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8"); return payload

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--system-prompt",default="brains/business/BUSINESS-BRAIN-SYSTEM-PROMPT.md"); p.add_argument("--scenarios",default="evaluations/BUSINESS-BRAIN-v0.1-SCENARIOS.md"); p.add_argument("--output",default="evaluations/results/BUSINESS-BRAIN-v0.1-HARNESS-RESULTS.json"); a=p.parse_args(); x=run(a.system_prompt,a.scenarios,a.output); c={}
    for r in x["results"]: c[r["status"]]=c.get(r["status"],0)+1
    print(json.dumps({"validation_mode":x["validation_mode"],"scenario_count":x["scenario_count"],"counts":c}))
