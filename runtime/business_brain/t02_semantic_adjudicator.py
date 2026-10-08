from __future__ import annotations
import argparse, json, re
from pathlib import Path
STATUS_ORDER={"PASS":0,"PARTIAL":1,"FAIL":2}
FACTORS={"decision_impact":(r"decision impact",r"impacto.*decisi[oó]n"),"information_cost":(r"information cost",r"coste.*informaci[oó]n",r"cost.*obtain"),"reversibility":(r"reversib",),"decision_change":(r"decision[- ]changing",r"change.*decision"),"dependencies":(r"dependenc",r"prerequis",r"bloquea"),"comparative":(r"compar",r"versus",r"vs\.",r"trade.?off")}
INDET=(r"indeterminate",r"indeterminado",r"insufficient information",r"informaci[oó]n insuficiente",r"cannot establish",r"no permite establecer")
PAY=(r"payment",r"pago",r"pay",r"pag[ao]",r"purchase",r"compra",r"paid")
LOW=(r"free",r"gratis",r"trial",r"prueba",r"low[- ]commitment",r"bajo compromiso",r"engagement",r"feedback")
WTP=(r"willingness to pay",r"disposici[oó]n.*pagar",r"willing.*pay",r"WTP")
def text(v):
    if isinstance(v,str): return v
    if isinstance(v,list): return " ".join(text(x) for x in v)
    if isinstance(v,dict): return " ".join(f"{k} {text(x)}" for k,x in v.items())
    return str(v)
def has(s,p): return any(re.search(x,s,re.I) for x in p)
def gate(p):
    r=p.get("results")
    if not isinstance(r,list) or len(r)!=1:return "INVALID_EXECUTION","expected exactly one result"
    m=r[0].get("metadata") or {}
    for k,w in (("context_integrity","CLEAR"),("generation_gate","COMPLETE"),("json_gate","VALID")):
        got=(m.get(k) or {}).get("status")
        if got!=w:return "INVALID_EXECUTION",f"{k} is {got}"
    return "CLEAR",""
def voi(d):
    p=d.get("priority") or {}; s=text(p); hits=[n for n,pats in FACTORS.items() if has(s,pats)]
    ind=has(s,INDET); sel=str(p.get("selected","")).upper(); status="PASS" if len(hits)>=4 else "PARTIAL"
    if sel in {"B","D"} and len(hits)<2: status="FAIL"
    return {"status":status,"factors_detected":hits,"selected":sel,"indeterminate_detected":ind,"reason":"Detected VoI factors: "+(", ".join(hits) if hits else "none")}
def alignment(d):
    e=text(d.get("experiment") or {}); alltext=text(d); sel=str((d.get("priority") or {}).get("selected","")).upper()
    if not e.strip(): return {"status":"FAIL","selected":sel,"reason":"Experiment is empty."}
    pay=has(e,PAY); low=has(e,LOW); wtp=has(alltext,WTP); status="PASS"; reasons=[]
    if sel not in set("ABCDE"): status="PARTIAL"; reasons.append("No single uncertainty is selected.")
    if wtp and low and not pay: status="PARTIAL"; reasons.append("WTP is discussed but the experiment uses free/low-commitment engagement instead of economic commitment.")
    if sel=="B" and not pay: status="PARTIAL" if low else "FAIL"; reasons.append("B is willingness to pay but no direct payment/economic commitment is observable.")
    if sel=="D" and pay and not has(e,(r"cost",r"coste",r"margin",r"economics")): status="PARTIAL"; reasons.append("Payment informs demand but does not directly observe delivery economics for D.")
    if not reasons: reasons.append("Observable behavior is aligned with the selected uncertainty.")
    return {"status":status,"selected":sel,"payment_behavior_detected":pay,"low_commitment_signal_detected":low,"reason":" ".join(reasons)}
def adjudicate_payload(p):
    s,reason=gate(p)
    if s!="CLEAR": return {"adjudicator_version":"0.1","test":"T02-COMPACT-v0.1","status":s,"reason":reason}
    d=json.loads(p["results"][0]["raw_output"]); v=voi(d); a=alignment(d); overall=max((v["status"],a["status"]),key=lambda x:STATUS_ORDER[x]); regs=[]
    if v["status"]!="PASS": regs.append({"id":"REG-VOI-UNDEREXPLICIT","status":"OBSERVED","reason":v["reason"]})
    if a["status"]!="PASS": regs.append({"id":"REG-HYPOTHESIS-EXPERIMENT-MISMATCH","status":"OBSERVED","reason":a["reason"]})
    return {"adjudicator_version":"0.1","test":"T02-COMPACT-v0.1","status":overall,"semantic_adjudication":{"voi":v,"experiment_alignment":a},"regressions":regs}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("input",type=Path); ap.add_argument("--json-out",type=Path); ap.add_argument("--text-out",type=Path); a=ap.parse_args()
    out=json.dumps(adjudicate_payload(json.loads(a.input.read_text(encoding="utf-8"))),ensure_ascii=False,indent=2); print(out)
    for p in (a.json_out,a.text_out):
        if p: p.parent.mkdir(parents=True,exist_ok=True); p.write_text(out+"\n",encoding="utf-8")
if __name__=="__main__": main()
