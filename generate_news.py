
import os
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from openai import OpenAI

# Read your agent instructions
instructions = Path("README.md").read_text(
    encoding="utf-8"
)

today = datetime.now(
    ZoneInfo("Asia/Singapore")
).strftime("%Y-%m-%d")

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

response = client.responses.create(
    model=os.getenv("OPENAI_MODEL", "gpt-5"),
    tools=[{"type": "web_search"}],
    input=f"""
Follow these instructions for today's news briefing:

{instructions}

Today's date in Singapore is {today}.

Research current news using web search.
Prioritise recent, significant developments.
Include publication dates and original source URLs.
Do not invent facts or sources.
Write the finished report in Markdown.
"""
)

report = Path("reports") / f"{today}.md"
report.parent.mkdir(parents=True, exist_ok=True)
report.write_text(
    response.output_text,
    encoding="utf-8"
)

print(f"News report saved to {report}")
