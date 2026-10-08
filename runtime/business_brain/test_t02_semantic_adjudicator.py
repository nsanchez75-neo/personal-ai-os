import json
from runtime.business_brain.t02_semantic_adjudicator import adjudicate_payload
def payload(d): return {"results":[{"metadata":{"context_integrity":{"status":"CLEAR"},"generation_gate":{"status":"COMPLETE"},"json_gate":{"status":"VALID"}},"raw_output":json.dumps(d)}]}
def base():
    return {"uncertainties":[{"id":x,"decision_impact":"x","current_evidence":"x"} for x in "ABCDE"],"priority":{"status":"Indeterminate","selected":None,"reason":"Available information is insufficient to establish a unique priority."},"experiment":{"tests":"Offer a free diagnostic or trial.","observable_behavior":"Customers engage, give feedback, or express continued interest."}}
def test_voi_partial(): assert adjudicate_payload(payload(base()))["semantic_adjudication"]["voi"]["status"]=="PARTIAL"
def test_alignment_partial(): assert adjudicate_payload(payload(base()))["semantic_adjudication"]["experiment_alignment"]["status"]=="PARTIAL"
def test_aligned_pass():
    d=base(); d["priority"]={"selected":"B","reason":"Compare decision impact, information cost, reversibility and dependencies; B has the highest decision-changing value."}; d["experiment"]={"tests":"Present a concrete paid offer and observe payment or rejection.","observable_behavior":"Payment or rejection."}; assert adjudicate_payload(payload(d))["status"]=="PASS"
