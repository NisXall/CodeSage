"""
eval.py

Runs a fixed set of test questions through the RAG pipeline and records
what was retrieved and what was answered, so accuracy can be manually
graded and reported in the README.

This is intentionally simple (no automated grading) — for a portfolio
project, a transparent log a human reviewer can read is more convincing
than a black-box "95% accuracy" number with no evidence behind it.

Run with: python eval.py
Output: eval_results.md
"""

import json
import time
from generate import answer_question

# Each question includes a short note on what a correct answer should
# reference, so you (or a reader) can grade it by eye afterward.
EVAL_QUESTIONS = [
    # ---- 1. Clear hits (grader: relevant, no correction needed) ----
    {
        "question": "What does the route_after_grading function decide?",
        "expected_source": "backend/routing.py (route_after_grading)",
        "expected_behavior": "RELEVANT: goes to generate if enough chunks passed, else the corrective path",
    },
    {
        "question": "What is the default value of MIN_RELEVANT_DOCS and what does it control?",
        "expected_source": "backend/config.py",
        "expected_behavior": "RELEVANT: default is 1, number of chunks that must pass grading",
    },
    {
        "question": "How many chunks does the retriever fetch per query by default?",
        "expected_source": "backend/config.py (RETRIEVAL_K) / backend/nodes/retriever.py",
        "expected_behavior": "RELEVANT: 4",
    },
    {
        "question": "What fields does GraphState hold?",
        "expected_source": "backend/state.py (GraphState)",
        "expected_behavior": "RELEVANT: question, search_query, documents, grades, relevance, used_web_search, generation",
    },
    {
        "question": "Which models are used for the LLM and for embeddings by default?",
        "expected_source": "backend/config.py / backend/llm.py / backend/embeddings.py",
        "expected_behavior": "RELEVANT: llama3.1:8b and nomic-embed-text via Ollama",
    },
    {
        "question": "What chunk size and overlap are used during ingestion?",
        "expected_source": "backend/config.py / backend/ingestion/chunker.py",
        "expected_behavior": "RELEVANT: 800 characters, 120 overlap",
    },

    # ---- 2. Vague queries (weak first retrieval, rewrite should help) ----
    {
        "question": "How does it decide the documents are bad?",
        "expected_source": "backend/nodes/grader.py + backend/routing.py",
        "expected_behavior": "REWRITE: should be reformulated toward chunk relevance grading",
    },
    {
        "question": "What happens when the model breaks?",
        "expected_source": "backend/nodes/grader.py / rewriter.py / generator.py (error handling)",
        "expected_behavior": "REWRITE: should be reformulated toward LLM failure handling",
    },
    {
        "question": "How does it avoid adding the same file twice?",
        "expected_source": "backend/ingestion/indexer.py (content-hash chunk IDs)",
        "expected_behavior": "REWRITE: should be reformulated toward duplicate prevention in ingestion",
    },
    {
        "question": "How does the thing talk to the browser live?",
        "expected_source": "backend/api/routes.py + backend/runner.py (SSE streaming)",
        "expected_behavior": "REWRITE: should be reformulated toward Server-Sent Events streaming",
    },
    {
        "question": "Where does the internet part happen?",
        "expected_source": "backend/nodes/web_search.py",
        "expected_behavior": "REWRITE: should be reformulated toward web search fallback",
    },

    # ---- 3. Ambiguous queries (grader: partially relevant) ----
    {
        "question": "How does the system handle errors?",
        "expected_source": "multiple files (grader, rewriter, web_search, generator, events)",
        "expected_behavior": "AMBIGUOUS: should combine several chunks or admit the answer is spread out",
    },
    {
        "question": "Where are settings stored?",
        "expected_source": "backend/config.py",
        "expected_behavior": "AMBIGUOUS: should find config.py and not overclaim beyond it",
    },
    {
        "question": "What does the prompt tell the model to do?",
        "expected_source": "backend/prompts.py (grader, rewriter, generator prompts)",
        "expected_behavior": "AMBIGUOUS: three prompts exist, should distinguish them or ask which one",
    },

    # ---- 4. Out-of-scope (grader: irrelevant, should refuse or fall back) ----
    {
        "question": "How do I bake a cake?",
        "expected_source": "NONE: should refuse, not in codebase",
        "expected_behavior": "IRRELEVANT: refuse, no made-up answer",
    },
    {
        "question": "Who won the 2022 FIFA World Cup?",
        "expected_source": "NONE: not in codebase",
        "expected_behavior": "IRRELEVANT: refuse, or take the web fallback if testing the CRAG path",
    },
    {
        "question": "How does Django's ORM work?",
        "expected_source": "NONE: coding question but not about this repo",
        "expected_behavior": "IRRELEVANT: refuse, or clearly say it is not in this codebase",
    },
    {
        "question": "What font does the dashboard use?",
        "expected_source": "NONE in indexed data: lives in frontend CSS, which is not indexed",
        "expected_behavior": "IRRELEVANT: should say it cannot find this in the indexed code",
    },

    # ---- 5. Plausible but absent features (hardest) ----
    {
        "question": "How does the retry loop use MAX_REWRITE_ATTEMPTS?",
        "expected_source": "backend/config.py (setting exists but is not used)",
        "expected_behavior": "TRAP: should say the setting is defined but no retry loop uses it yet",
    },
    {
        "question": "How does the system grade web search results?",
        "expected_source": "NONE: web results are not graded (roadmap item)",
        "expected_behavior": "TRAP: should say web results skip grading, not invent a grader",
    },
    {
        "question": "How does the agent remember previous questions in a conversation?",
        "expected_source": "NONE: no multi-turn memory (roadmap item)",
        "expected_behavior": "TRAP: should say it is not implemented",
    },
    {
        "question": "How are PDF files ingested?",
        "expected_source": "NONE: only .md and .txt are supported (PDF is a roadmap item)",
        "expected_behavior": "TRAP: should say PDF ingestion does not exist",
    },
    {
        "question": "How does the system authenticate API requests?",
        "expected_source": "NONE: no authentication in codebase",
        "expected_behavior": "TRAP: should say it is not implemented",
    },

    # ---- 6. Multi-hop (needs chunks from more than one file) ----
    {
        "question": "What happens end-to-end when no retrieved chunk is relevant?",
        "expected_source": "backend/graph.py + routing.py + nodes/rewriter.py + nodes/web_search.py + nodes/generator.py",
        "expected_behavior": "RELEVANT but needs re-retrieval to cover the full corrective path",
    },
    {
        "question": "What happens if the grader LLM throws an error, and how does that affect routing?",
        "expected_source": "backend/nodes/grader.py + backend/routing.py",
        "expected_behavior": "RELEVANT: error counts as not relevant, so bad context can never pass",
    },
    {
        "question": "What does the generator do when there is no usable context at all?",
        "expected_source": "backend/nodes/generator.py + backend/prompts.py",
        "expected_behavior": "RELEVANT: skips the LLM call and says it found no reliable information",
    },
    {
        "question": "How do the tests verify the routing behavior?",
        "expected_source": "tests/ (routing tests) + backend/routing.py",
        "expected_behavior": "RELEVANT but needs chunks from two files",
    },

    # ---- 7. False-premise questions (should correct, not go along) ----
    {
        "question": "Why does Flux-CRAG use OpenAI embeddings?",
        "expected_source": "backend/embeddings.py (uses Ollama nomic-embed-text)",
        "expected_behavior": "FALSE PREMISE: should correct it, embeddings are local via Ollama",
    },
    {
        "question": "Why does the vector store use Pinecone?",
        "expected_source": "backend/vectorstore.py (uses persistent ChromaDB)",
        "expected_behavior": "FALSE PREMISE: should correct it, ChromaDB on disk",
    },
    {
        "question": "How does the grader assign a relevance score from 0 to 1 to each chunk?",
        "expected_source": "backend/nodes/grader.py (structured yes/no verdict with reason, not a score)",
        "expected_behavior": "FALSE PREMISE: should correct it, the verdict is binary plus a reason",
    },
]


def run_eval():
    results = []

    for i, item in enumerate(EVAL_QUESTIONS, 1):
        print(f"[{i}/{len(EVAL_QUESTIONS)}] {item['question']}")
        result = answer_question(item["question"])

        results.append({
            "question": item["question"],
            "expected_source": item["expected_source"],
            "answer": result["answer"],
            "retrieved_sources": [
                f"{s['file']}:{s['start_line']}-{s['end_line']} ({s['type']} {s['name']})"
                for s in result["sources"]
            ],
        })

        if i < len(EVAL_QUESTIONS):
            time.sleep(13)  # stay under free-tier 5 req/min limit

    return results


def write_markdown_report(results, path="eval_results.md"):
    lines = ["# RAG Evaluation Results\n"]
    lines.append(f"Total questions: {len(results)}\n")
    lines.append("Grade each answer manually: mark ✅ correct / ⚠️ partial / ❌ wrong in the 'Grade' column after review.\n")

    for i, r in enumerate(results, 1):
        lines.append(f"## {i}. {r['question']}\n")
        lines.append(f"**Expected source:** {r['expected_source']}\n")
        lines.append(f"**Retrieved sources:**")
        for s in r["retrieved_sources"]:
            lines.append(f"- {s}")
        lines.append(f"\n**Answer:**\n> {r['answer'].replace(chr(10), chr(10) + '> ')}\n")
        lines.append("**Grade:** _(fill in)_\n")
        lines.append("---\n")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nWrote report to {path}")


if __name__ == "__main__":
    results = run_eval()

    with open("eval_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    write_markdown_report(results)