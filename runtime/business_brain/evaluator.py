import re
from runtime.business_brain.models import AssertionResult, ScenarioResult, Scenario, ModelResponse
_STOP={"the","and","for","with","from","that","this","into","must","should","avoid","not","before","after","where","without","also","only","what","how","can","does","business","brain"}
def _tokens(text):
    return {w for w in re.findall(r"[a-záéíóúñü0-9]{4,}", text.lower()) if w not in _STOP}
def evaluate_assertion(assertion, response):
    a,r=_tokens(assertion),_tokens(response)
    if not a: return AssertionResult(assertion,"INVALID","No evaluable tokens")
    overlap=len(a&r)/len(a)
    if overlap>=.55: return AssertionResult(assertion,"PASS",f"lexical evidence overlap={overlap:.2f}")
    if overlap>=.25: return AssertionResult(assertion,"PARTIAL",f"lexical evidence overlap={overlap:.2f}")
    return AssertionResult(assertion,"FAIL",f"lexical evidence overlap={overlap:.2f}")
def evaluate_scenario(scenario, response):
    rs=[evaluate_assertion(a,response.text) for a in scenario.assertions]
    statuses={x.status for x in rs}
    status="INVALID" if "INVALID" in statuses else "FAIL" if "FAIL" in statuses else "PARTIAL" if "PARTIAL" in statuses else "PASS"
    return ScenarioResult(scenario.scenario_id,scenario.title,status,response.provider,rs,response.metadata)
