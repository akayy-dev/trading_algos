import finnhub

client = finnhub.Client(api_key="cvaaqk9r01qshflh67sgcvaaqk9r01qshflh67t0")

res = client.earnings_calendar(symbol="TSLA", _from="2025-01-01", to="2026-01-01")

print(res)