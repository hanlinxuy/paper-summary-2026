#!/usr/bin/env python3
"""
Concurrent Kimi API fetcher for arxiv paper summaries.
Fetches Q&A summaries from papers.cool API with rate limiting (max 5/sec).
"""

import asyncio
import aiohttp
import json
import re
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

# Output directory
OUTPUT_DIR = Path(
    "/Users/hanlinxuy/Documents/CodeSpace/paper_reading/paper_single_reading/paper-summary/knowledge/kimi_summaries"
)
FAILURE_LOG = Path(
    "/Users/hanlinxuy/Documents/CodeSpace/paper_reading/paper_single_reading/paper-summary/knowledge/kimi_failures.log"
)

# Rate limiting
MAX_CONCURRENT = 5
REQUESTS_PER_SECOND = 5

# All 150 arxiv_ids from 6 days of papers
ARXIV_IDS = [
    "2602.17270",
    "2602.16855",
    "2602.17663",
    "2602.17664",
    "2602.17659",
    "2602.17650",
    "2602.17547",
    "2602.17665",
    "2602.17658",
    "2602.17004",
    "2602.16968",
    "2602.17124",
    "2602.16802",
    "2602.17465",
    "2602.17616",
    "2602.17636",
    "2602.16928",
    "2602.17594",
    "2602.17584",
    "2602.17634",
    "2602.17641",
    "2602.17196",
    "2602.16891",
    "2602.16742",
    "2602.17363",
    "2602.18308",
    "2602.18428",
    "2602.18434",
    "2602.18291",
    "2602.18432",
    "2602.18422",
    "2602.18224",
    "2602.18292",
    "2602.18020",
    "2602.17902",
    "2602.17909",
    "2602.18424",
    "2602.18283",
    "2602.18425",
    "2602.17807",
    "2602.18322",
    "2602.18420",
    "2602.17871",
    "2602.18232",
    "2602.18066",
    "2602.18282",
    "2602.17709",
    "2602.17951",
    "2602.18022",
    "2602.18095",
    "2602.20021",
    "2602.20159",
    "2602.20161",
    "2602.19526",
    "2602.18532",
    "2602.19919",
    "2602.20089",
    "2602.18846",
    "2602.18882",
    "2602.20152",
    "2602.20122",
    "2602.19810",
    "2602.18710",
    "2602.19895",
    "2602.18887",
    "2602.19213",
    "2602.20157",
    "2602.20160",
    "2602.18702",
    "2602.19672",
    "2602.20117",
    "2602.19969",
    "2602.20052",
    "2602.19870",
    "2602.18873",
    "2602.21193",
    "2602.21204",
    "2602.21009",
    "2602.20945",
    "2602.21201",
    "2602.20739",
    "2602.21188",
    "2602.21189",
    "2602.20399",
    "2602.21198",
    "2602.20794",
    "2602.21053",
    "2602.21172",
    "2602.21015",
    "2602.21052",
    "2602.20937",
    "2602.21158",
    "2602.21186",
    "2602.20980",
    "2602.21143",
    "2602.20913",
    "2602.21105",
    "2602.21064",
    "2602.21196",
    "2602.20528",
    "2602.22208",
    "2602.22010",
    "2602.21818",
    "2602.21224",
    "2602.21545",
    "2602.21633",
    "2602.21534",
    "2602.22094",
    "2602.22175",
    "2602.21929",
    "2602.22144",
    "2602.22190",
    "2602.22212",
    "2602.21677",
    "2602.21497",
    "2602.21780",
    "2602.21810",
    "2602.21441",
    "2602.22056",
    "2602.21552",
    "2602.21760",
    "2602.21341",
    "2602.21704",
    "2602.21814",
    "2602.21854",
    "2602.23330",
    "2602.23361",
    "2602.23058",
    "2602.23363",
    "2602.23351",
    "2602.22437",
    "2602.22897",
    "2602.22675",
    "2602.23359",
    "2602.23306",
    "2602.22765",
    "2602.23152",
    "2602.23132",
    "2602.23349",
    "2602.22576",
    "2602.23225",
    "2602.22953",
    "2602.23360",
    "2602.23008",
    "2602.23258",
    "2602.23205",
    "2602.22732",
    "2602.22913",
    "2602.23358",
    "2602.22543",
]


def parse_html_qa(html_content: str) -> Optional[Dict[str, str]]:
    """Parse HTML response to extract Q&A pairs.

    HTML structure:
    <p class="faq-q"><strong>Q1</strong>: 问题</p>
    <div class="faq-a">答案</div>
    ...
    """
    result = {}

    # Split the HTML into question-answer pairs
    # Pattern: <p class="faq-q"><strong>Q1</strong>: 问题</p> followed by <div class="faq-a">答案</div>

    # Find all question blocks
    q_pattern = r'<p class="faq-q"><strong>(Q\d+)</strong>.*?</p>'
    question_matches = list(re.finditer(q_pattern, html_content))

    for i, q_match in enumerate(question_matches):
        q_num = q_match.group(1)  # Q1, Q2, etc.
        q_key = f"q{q_num.lower().replace('q', '')}"  # q1, q2, etc.

        # Find the answer div that follows this question
        # Start searching after the question tag ends
        start_pos = q_match.end()

        # Find the next <div class="faq-a"> after this question
        answer_div_pattern = r'<div class="faq-a">(.*?)</div>'
        answer_match = re.search(
            answer_div_pattern, html_content[start_pos:], re.DOTALL
        )

        if answer_match:
            answer = answer_match.group(1)
            # Clean the answer: remove HTML tags, decode entities, clean whitespace
            answer = re.sub(r"<[^>]+>", "", answer)
            answer = (
                answer.replace("&nbsp;", " ")
                .replace("&lt;", "<")
                .replace("&gt;", ">")
                .replace("&amp;", "&")
            )
            answer = " ".join(answer.split())

            if answer and len(answer) > 10:
                result[q_key] = answer

    # Check if we have all 7 Q&A
    if len(result) >= 7:
        return result

    return None if not result else result


async def fetch_kimi_summary(
    session: aiohttp.ClientSession,
    arxiv_id: str,
    semaphore: asyncio.Semaphore,
    rate_limiter: asyncio.Lock,
) -> Dict:
    """Fetch Kimi summary for a single paper."""
    url = f"https://papers.cool/arxiv/kimi?paper={arxiv_id}"

    async with semaphore:
        async with rate_limiter:
            await asyncio.sleep(1.0 / REQUESTS_PER_SECOND)

        try:
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                if response.status == 200:
                    html_content = await response.text()
                    qa_data = parse_html_qa(html_content)

                    if qa_data:
                        result = {"arxiv_id": arxiv_id, **qa_data}
                        return {"success": True, "data": result}
                    else:
                        return {
                            "success": False,
                            "arxiv_id": arxiv_id,
                            "error": "Failed to parse Q&A from HTML",
                        }
                else:
                    return {
                        "success": False,
                        "arxiv_id": arxiv_id,
                        "error": f"HTTP {response.status}",
                    }
        except asyncio.TimeoutError:
            return {"success": False, "arxiv_id": arxiv_id, "error": "Timeout"}
        except Exception as e:
            return {"success": False, "arxiv_id": arxiv_id, "error": str(e)}


async def main():
    """Main function to fetch all Kimi summaries."""
    print(f"Starting to fetch {len(ARXIV_IDS)} papers...")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    successes = []
    failures = []

    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    rate_limiter = asyncio.Lock()

    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_kimi_summary(session, arxiv_id, semaphore, rate_limiter)
            for arxiv_id in ARXIV_IDS
        ]

        for coro in asyncio.as_completed(tasks):
            result = await coro

            if result["success"]:
                successes.append(result["data"])
                output_file = OUTPUT_DIR / f"{result['data']['arxiv_id']}.json"
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(result["data"], f, ensure_ascii=False, indent=2)
                print(
                    f"[{len(successes)}/{len(ARXIV_IDS)}] Saved: {result['data']['arxiv_id']}"
                )
            else:
                failures.append(result)
                print(
                    f"[FAIL] {result['arxiv_id']}: {result.get('error', 'Unknown error')}"
                )

    # Write failure log
    with open(FAILURE_LOG, "w", encoding="utf-8") as f:
        f.write(f"Kimi API Failures - {datetime.now().isoformat()}\n")
        f.write(
            f"Total: {len(ARXIV_IDS)}, Success: {len(successes)}, Failed: {len(failures)}\n"
        )
        f.write("=" * 50 + "\n")
        for failure in failures:
            f.write(f"{failure['arxiv_id']}: {failure.get('error', 'Unknown error')}\n")

    # Print summary
    print("\n" + "=" * 50)
    print(f"SUMMARY")
    print(f"=" * 50)
    print(f"Total papers: {len(ARXIV_IDS)}")
    print(f"Successes: {len(successes)} ({len(successes) / len(ARXIV_IDS) * 100:.1f}%)")
    print(f"Failures: {len(failures)}")
    print(f"Success rate: {len(successes) / len(ARXIV_IDS) * 100:.1f}%")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Failure log: {FAILURE_LOG}")

    if len(successes) < 135:
        print(
            f"\nWarning: Success rate below 90% target (need >= 135, got {len(successes)})"
        )
    else:
        print(f"\nSuccess rate >= 90% target achieved!")


if __name__ == "__main__":
    asyncio.run(main())
