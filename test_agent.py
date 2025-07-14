# test_agent.py
from agents.meeting_agent import get_enterprise_agent



agent = get_enterprise_agent()
if agent is None:
    raise SystemExit("Agent failed to initialize.")

while True:
    q = input("🔍 You: ")
    if q.lower() in {"exit", "quit"}:
        break
    res = agent.invoke({"query": q})
    print("🤖", res["result"])
