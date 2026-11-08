# RAG Evaluation Results

Total questions: 30

Grade each answer manually: mark Correct, Partial, or Wrong in the 'Grade' line after review.

## 1. What does the route_after_grading function decide?

**Expected source:** backend/routing.py (route_after_grading)

**Retrieved sources:**
- tests/test_rewriter_and_routing.py:33-34 (function test_route_goes_to_generate_when_relevant)
- tests/test_rewriter_and_routing.py:41-42 (function test_route_defaults_to_corrective_path_when_relevance_missing)
- tests/test_rewriter_and_routing.py:1-42 (module (module level))
- tests/test_rewriter_and_routing.py:37-38 (function test_route_goes_to_rewrite_when_irrelevant)
- backend/routing.py:6-14 (function route_after_grading)

**Answer:**
> The `route_after_grading` function decides the next node once documents have been graded (backend/routing.py:7). If there are enough relevant chunks (indicated by a "relevant" state), it decides to move to the "generate" node; otherwise, it takes the corrective path to "rewrite_query" (backend/routing.py:8-14, tests/test_rewriter_and_routing.py:33-42).

**Grade:** Correct

---

## 2. What is the default value of MIN_RELEVANT_DOCS and what does it control?

**Expected source:** backend/config.py

**Retrieved sources:**
- tests/test_grader_node.py:61-67 (function test_min_relevant_docs_threshold_is_respected)
- backend/ingestion/loader.py:11-37 (function load_documents)
- scripts/ingest.py:15-36 (function main)
- backend/nodes/grader.py:28-104 (function grade_documents)
- tests/test_grader_node.py:8-12 (function _docs)

**Answer:**
> The provided code context does not specify the default value of `min_relevant_docs`. While `tests/test_grader_node.py` demonstrates setting the value to 2 for testing purposes (tests/test_grader_node.py:63), the actual default value is not defined in the files provided.
>
> Regarding its function, `min_relevant_docs` controls the threshold for document relevance evaluation in the `grade_documents` node: if the number of relevant documents found is greater than or equal to `min_relevant_docs`, the relevance state is set to "relevant"; otherwise, it is set to "irrelevant," which triggers the graph's corrective path (backend/nodes/grader.py:29-31, 80-81).

**Grade:** Partial

---

## 3. How many chunks does the retriever fetch per query by default?

**Expected source:** backend/config.py (RETRIEVAL_K) / backend/nodes/retriever.py

**Retrieved sources:**
- backend/ingestion/indexer.py:34-36 (function collection_count)
- backend/ingestion/indexer.py:21-31 (function index_documents)
- tests/test_api.py:53-62 (function test_knowledge_base_counts_chunks_per_source)
- backend/nodes/retriever.py:10-54 (function retrieve)
- backend/nodes/retriever.py:1-54 (module (module level))

**Answer:**
> The provided code context does not specify a numerical default for how many chunks the retriever fetches per query. It indicates that the retriever fetches the number of chunks defined by `settings.retrieval_k` (`backend/nodes/retriever.py:27`, `backend/nodes/retriever.py:16`).

**Grade:** Partial

---

## 4. What fields does GraphState hold?

**Expected source:** backend/state.py (GraphState)

**Retrieved sources:**
- backend/nodes/grader.py:1-104 (module (module level))
- backend/graph.py:1-73 (module (module level))
- backend/graph.py:42-67 (function build_graph)
- backend/events.py:1-52 (module (module level))
- backend/nodes/retriever.py:1-54 (module (module level))

**Answer:**
> The provided code context does not contain the definition or the fields of the `GraphState` class. While `GraphState` is imported in `backend/nodes/grader.py` (line 10), `backend/graph.py` (line 12), and `backend/nodes/retriever.py` (line 5), the contents of the file where it is defined are not provided.

**Grade:** Wrong

---

## 5. Which models are used for the LLM and for embeddings by default?

**Expected source:** backend/config.py / backend/llm.py / backend/embeddings.py

**Retrieved sources:**
- backend/embeddings.py:1-15 (module (module level))
- backend/embeddings.py:10-15 (function get_embeddings)
- backend/llm.py:10-16 (function get_llm)
- backend/llm.py:1-16 (module (module level))
- backend/config.py:13-45 (class Settings)

**Answer:**
> By default, the LLM and embedding models are:
>
> *   **LLM:** `llama3.1:8b` (backend/config.py:23)
> *   **Embeddings:** `nomic-embed-text` (backend/config.py:24)

**Grade:** Correct

---

## 6. What chunk size and overlap are used during ingestion?

**Expected source:** backend/config.py / backend/ingestion/chunker.py

**Retrieved sources:**
- tests/test_ingestion.py:1-25 (module (module level))
- backend/ingestion/chunker.py:1-25 (module (module level))
- backend/ingestion/indexer.py:9-18 (function _chunk_id)
- backend/ingestion/indexer.py:34-36 (function collection_count)
- backend/ingestion/chunker.py:8-25 (function split_documents)

**Answer:**
> The chunk size and overlap used during ingestion are retrieved from the application settings by default, though they can be overridden by arguments provided to the `split_documents` function. Specifically:
>
> *   If `chunk_size` is not provided to the function, `settings.chunk_size` is used (backend/ingestion/chunker.py:18).
> *   If `chunk_overlap` is not provided to the function, `settings.chunk_overlap` is used (backend/ingestion/chunker.py:19).

**Grade:** Partial

---

## 7. How does it decide the documents are bad?

**Expected source:** backend/nodes/grader.py + backend/routing.py

**Retrieved sources:**
- tests/test_web_search_node.py:15-25 (function test_to_documents_maps_fields_and_skips_empty_bodies)
- backend/ingestion/loader.py:11-37 (function load_documents)
- tests/test_grader_node.py:30-37 (function test_grade_documents_flags_irrelevant_when_nothing_passes)
- tests/test_ingestion.py:5-13 (function test_load_documents_reads_only_supported_non_empty_files)
- tests/test_generator_node.py:6-18 (function _docs)

**Answer:**
> Based on the provided code, the determination of whether documents are "bad" (or irrelevant) occurs within the `grade_documents` function. When documents do not meet the grading criteria, they are filtered out and the relevance is flagged as "irrelevant":
>
> *   The `grade_documents` function performs grading, and if nothing passes the criteria, it updates the "relevance" to "irrelevant" and sets the "documents" list to empty (tests/test_grader_node.py:30-37).
> *   The actual grading logic is delegated to a helper function, `_grade_chunk`, which is used during the grading process (tests/test_grader_node.py:31).

**Grade:** Partial

---

## 8. What happens when the model breaks?

**Expected source:** backend/nodes/grader.py / rewriter.py / generator.py (error handling)

**Retrieved sources:**
- tests/test_generator_node.py:57-59 (function broken)
- tests/test_api.py:34-43 (function test_health_degrades_when_store_is_unavailable)
- tests/test_generator_node.py:56-65 (function test_generate_reports_llm_failure)
- backend/api/routes.py:17-32 (function health)
- scripts/healthcheck.py:25-63 (function main)

**Answer:**
> When the LLM breaks, the behavior depends on the context:
>
> *   **During generation:** When the generator encounters an LLM failure, it reports `generator.GENERATION_ERROR_ANSWER` as the `generation` value (tests/test_generator_node.py:63-65).
> *   **During health checks:** If an error occurs when attempting to retrieve the collection count (which is part of the application's health status), the `chunks_indexed` field is set to `None` and the overall status is set to `"degraded"` (backend/api/routes.py:17-32; tests/test_api.py:34-43).
>
> Regarding the `scripts/healthcheck.py` script, if errors occur during model verification or collection retrieval, the script prints specific failure messages and returns an exit code of `1` (scripts/healthcheck.py:25-63).

**Grade:** Correct

---

## 9. How does it avoid adding the same file twice?

**Expected source:** backend/ingestion/indexer.py (content-hash chunk IDs)

**Retrieved sources:**
- backend/ingestion/loader.py:11-37 (function load_documents)
- tests/test_web_search_node.py:28-40 (function test_web_search_combines_with_existing_documents)
- tests/test_ingestion.py:5-13 (function test_load_documents_reads_only_supported_non_empty_files)
- tests/test_ingestion.py:16-25 (function test_split_documents_respects_size_and_keeps_metadata)
- scripts/ingest.py:15-36 (function main)

**Answer:**
> The provided code context does not indicate that the system has a mechanism to prevent adding the same file twice during the loading process.
>
> The `load_documents` function iterates over every file found in the directory path using `root.rglob("*")` and adds each supported, non-empty file to the `documents` list (backend/ingestion/loader.py:18-33). The provided code does not show any logic to check if a file has already been processed or to verify uniqueness based on file path or content during this ingestion phase.

**Grade:** Wrong

---

## 10. How does the thing talk to the browser live?

**Expected source:** backend/api/routes.py + backend/runner.py (SSE streaming)

**Retrieved sources:**
- backend/llm.py:10-16 (function get_llm)
- tests/test_web_search_node.py:57-65 (function test_web_search_survives_network_failure)
- backend/llm.py:1-16 (module (module level))
- backend/nodes/web_search.py:12-15 (function _search_web)
- tests/test_web_search_node.py:58-59 (function boom)

**Answer:**
> The provided code context does not contain information regarding how the system talks to a browser live. While `backend/nodes/web_search.py` performs a DuckDuckGo text search (backend/nodes/web_search.py:12-15), there is no mention of live browser interaction.

**Grade:** Wrong

---

## 11. Where does the internet part happen?

**Expected source:** backend/nodes/web_search.py

**Retrieved sources:**
- tests/test_web_search_node.py:57-65 (function test_web_search_survives_network_failure)
- backend/api/routes.py:56-66 (function ask)
- backend/api/routes.py:1-66 (module (module level))
- scripts/ask.py:1-57 (module (module level))
- tests/test_web_search_node.py:58-59 (function boom)

**Answer:**
> Based on the provided code context, the internet search functionality is implemented via a function named `_search_web`, which is located in the `web_search` module (tests/test_web_search_node.py:60).

**Grade:** Partial

---

## 12. How does the system handle errors?

**Expected source:** multiple files (grader, rewriter, web_search, generator, events)

**Retrieved sources:**
- tests/test_runner.py:52-64 (function test_node_crash_becomes_an_error_message)
- tests/test_api.py:34-43 (function test_health_degrades_when_store_is_unavailable)
- backend/runner.py:1-45 (module (module level))
- tests/test_generator_node.py:56-65 (function test_generate_reports_llm_failure)
- tests/test_grader_node.py:49-58 (function test_grader_error_counts_as_not_relevant)

**Answer:**
> The system handles errors in the following ways depending on the context:
>
> *   **During `stream_run`:** When the graph execution crashes, the system yields a message of type `"error"` containing the exception message and ensures no `"final"` type messages are returned (backend/runner.py: 1-11; tests/test_runner.py: 52-64).
> *   **During `generator.generate`:** If an LLM failure occurs, the generator returns an update containing `generator.GENERATION_ERROR_ANSWER` (tests/test_generator_node.py: 56-65).
> *   **During `grader.grade_documents`:** If the grader encounters an error, the system counts the documents as `"irrelevant"` and sets the reason for the grades to start with "Grader error" (tests/test_grader_node.py: 49-58).
> *   **API Health:** If the store is unavailable (e.g., `collection_count` raises a `RuntimeError`), the `/api/health` endpoint returns a status of `"degraded"` with `chunks_indexed` set to `None` (tests/test_api.py: 34-43).

**Grade:** Correct

---

## 13. Where are settings stored?

**Expected source:** backend/config.py

**Retrieved sources:**
- backend/config.py:49-51 (function get_settings)
- backend/config.py:1-51 (module (module level))
- backend/llm.py:10-16 (function get_llm)
- backend/vectorstore.py:1-18 (module (module level))
- backend/embeddings.py:1-15 (module (module level))

**Answer:**
> Settings are defined in `backend/config.py` (backend/config.py:1-51) and can be overridden through environment variables or a local `.env` file (backend/config.py:3-4).

**Grade:** Correct

---

## 14. What does the prompt tell the model to do?

**Expected source:** backend/prompts.py (grader, rewriter, generator prompts)

**Retrieved sources:**
- backend/nodes/generator.py:1-103 (module (module level))
- scripts/healthcheck.py:20-22 (function _has_model)
- scripts/healthcheck.py:25-63 (function main)
- backend/llm.py:10-16 (function get_llm)
- tests/test_runner.py:8-10 (function _fake_generate)

**Answer:**
> The provided code context does not contain the content of the `GENERATOR_PROMPT`, so I cannot answer what it tells the model to do. The file `backend/nodes/generator.py` imports `GENERATOR_PROMPT` (backend/nodes/generator.py:5), but the text of the prompt itself is not included in the provided context.

**Grade:** Wrong

---

## 15. How do I bake a cake?

**Expected source:** NONE: should refuse, not in codebase

**Retrieved sources:**
- backend/llm.py:10-16 (function get_llm)
- backend/llm.py:1-16 (module (module level))
- tests/test_rewriter_and_routing.py:33-34 (function test_route_goes_to_generate_when_relevant)
- tests/test_rewriter_and_routing.py:10-11 (function test_clean_query_uses_fallback_when_blank)
- tests/test_rewriter_and_routing.py:41-42 (function test_route_defaults_to_corrective_path_when_relevance_missing)

**Answer:**
> The provided code context does not contain information on how to bake a cake.

**Grade:** Correct

---

## 16. Who won the 2022 FIFA World Cup?

**Expected source:** NONE: not in codebase

**Retrieved sources:**
- tests/test_rewriter_and_routing.py:14-19 (function test_rewrite_query_updates_search_query)
- tests/test_web_search_node.py:15-25 (function test_to_documents_maps_fields_and_skips_empty_bodies)
- tests/test_web_search_node.py:1-65 (module (module level))
- tests/test_runner.py:8-10 (function _fake_generate)
- tests/test_generator_node.py:6-18 (function _docs)

**Answer:**
> According to the provided code context, Argentina won the 2022 World Cup (tests/test_web_search_node.py:1-6).

**Grade:** Wrong

---

## 17. How does Django's ORM work?

**Expected source:** NONE: coding question but not about this repo

**Retrieved sources:**
- backend/embeddings.py:10-15 (function get_embeddings)
- backend/embeddings.py:1-15 (module (module level))
- backend/llm.py:10-16 (function get_llm)
- backend/api/routes.py:17-32 (function health)
- scripts/ask.py:1-57 (module (module level))

**Answer:**
> The provided code context does not contain any information regarding how Django's ORM works.

**Grade:** Correct

---

## 18. What font does the dashboard use?

**Expected source:** NONE in indexed data: lives in frontend CSS, which is not indexed

**Retrieved sources:**
- backend/main.py:26-27 (function dashboard_not_built)
- backend/main.py:14-28 (function create_app)
- backend/graph.py:22-39 (function get_topology)
- backend/events.py:1-52 (module (module level))
- backend/main.py:1-36 (module (module level))

**Answer:**
> The provided code context does not contain information regarding the font used by the dashboard.

**Grade:** Correct

---

## 19. How does the retry loop use MAX_REWRITE_ATTEMPTS?

**Expected source:** backend/config.py (setting exists but is not used)

**Retrieved sources:**
- backend/nodes/rewriter.py:25-60 (function rewrite_query)
- tests/test_rewriter_and_routing.py:22-30 (function test_rewrite_query_falls_back_to_original_on_llm_error)
- tests/test_rewriter_and_routing.py:10-11 (function test_clean_query_uses_fallback_when_blank)
- tests/test_rewriter_and_routing.py:14-19 (function test_rewrite_query_updates_search_query)
- tests/test_rewriter_and_routing.py:41-42 (function test_route_defaults_to_corrective_path_when_relevance_missing)

**Answer:**
> The provided code context does not contain any information about a retry loop or a `MAX_REWRITE_ATTEMPTS` constant. Therefore, I cannot answer how such a loop uses that constant.

**Grade:** Correct

---

## 20. How does the system grade web search results?

**Expected source:** NONE: web results are not graded (roadmap item)

**Retrieved sources:**
- tests/test_web_search_node.py:1-65 (module (module level))
- backend/nodes/web_search.py:12-15 (function _search_web)
- backend/state.py:7-28 (class GraphState)
- backend/nodes/web_search.py:1-87 (module (module level))
- tests/test_retriever_node.py:7-16 (class FakeStore)

**Answer:**
> The provided code context does not contain information regarding how the system grades web search results. While the `GraphState` definition includes a `grades` field described as "per-document verdicts: {'source', 'relevant', 'reason'}" (backend/state.py:18-19), the provided files do not describe the logic or process used to perform these gradings.

**Grade:** Correct

---

## 21. How does the agent remember previous questions in a conversation?

**Expected source:** NONE: no multi-turn memory (roadmap item)

**Retrieved sources:**
- backend/prompts.py:1-42 (module (module level))
- backend/api/routes.py:56-66 (function ask)
- scripts/ask.py:1-57 (module (module level))
- tests/test_api.py:70-84 (function test_ask_streams_runner_messages_as_sse)
- scripts/ask.py:12-53 (function main)

**Answer:**
> The provided code context does not contain information about how the agent remembers previous questions in a conversation. Therefore, I cannot answer this question.

**Grade:** Correct

---

## 22. How are PDF files ingested?

**Expected source:** NONE: only .md and .txt are supported (PDF is a roadmap item)

**Retrieved sources:**
- scripts/ingest.py:15-36 (function main)
- scripts/ingest.py:1-40 (module (module level))
- tests/test_ingestion.py:1-25 (module (module level))
- tests/test_ingestion.py:5-13 (function test_load_documents_reads_only_supported_non_empty_files)
- backend/ingestion/loader.py:11-37 (function load_documents)

**Answer:**
> The provided code context does not indicate that PDF files are supported or ingested. According to `backend/ingestion/loader.py`, the system recursively loads files based on a set of `SUPPORTED_EXTENSIONS` (backend/ingestion/loader.py:20), and the provided tests specifically show that files like `.png` are ignored (tests/test_ingestion.py:9-12), while documentation suggests only `.txt` and `.md` files are intended for ingestion (scripts/ingest.py:17, 21).

**Grade:** Correct

---

## 23. How does the system authenticate API requests?

**Expected source:** NONE: no authentication in codebase

**Retrieved sources:**
- backend/api/routes.py:56-66 (function ask)
- backend/api/routes.py:1-66 (module (module level))
- tests/test_api.py:1-84 (module (module level))
- backend/main.py:1-36 (module (module level))
- tests/test_api.py:65-67 (function test_ask_rejects_empty_and_oversized_questions)

**Answer:**
> The provided code context does not contain information regarding how the system authenticates API requests.

**Grade:** Correct

---

## 24. What happens end-to-end when no retrieved chunk is relevant?

**Expected source:** backend/graph.py + routing.py + nodes/rewriter.py + nodes/web_search.py + nodes/generator.py

**Retrieved sources:**
- backend/ingestion/chunker.py:8-25 (function split_documents)
- backend/ingestion/indexer.py:9-18 (function _chunk_id)
- tests/test_ingestion.py:16-25 (function test_split_documents_respects_size_and_keeps_metadata)
- backend/ingestion/indexer.py:21-31 (function index_documents)
- backend/ingestion/indexer.py:34-36 (function collection_count)

**Answer:**
> The provided code context does not contain information regarding what happens when a retrieved chunk is not relevant. The context covers document splitting (backend/ingestion/chunker.py:8-25), chunk ID generation (backend/ingestion/indexer.py:9-18), indexing documents (backend/ingestion/indexer.py:21-31), and counting chunks in a collection (backend/ingestion/indexer.py:34-36), but it does not describe retrieval or relevance processing.

**Grade:** Wrong

---

## 25. What happens if the grader LLM throws an error, and how does that affect routing?

**Expected source:** backend/nodes/grader.py + backend/routing.py

**Retrieved sources:**
- tests/test_rewriter_and_routing.py:41-42 (function test_route_defaults_to_corrective_path_when_relevance_missing)
- tests/test_rewriter_and_routing.py:1-42 (module (module level))
- tests/test_rewriter_and_routing.py:37-38 (function test_route_goes_to_rewrite_when_irrelevant)
- tests/test_rewriter_and_routing.py:33-34 (function test_route_goes_to_generate_when_relevant)
- backend/nodes/grader.py:1-104 (module (module level))

**Answer:**
> The provided code context does not contain information regarding how the system handles errors thrown by the grader LLM or how such errors affect routing.

**Grade:** Wrong

---

## 26. What does the generator do when there is no usable context at all?

**Expected source:** backend/nodes/generator.py + backend/prompts.py

**Retrieved sources:**
- tests/test_generator_node.py:45-53 (function test_generate_without_context_never_calls_llm)
- tests/test_generator_node.py:46-47 (function must_not_run)
- tests/test_generator_node.py:56-65 (function test_generate_reports_llm_failure)
- tests/test_generator_node.py:57-59 (function broken)
- backend/nodes/generator.py:53-103 (function generate)

**Answer:**
> When there is no usable context, the generator node returns an honest "could not find" answer instead of calling the LLM (backend/nodes/generator.py:53-56). Specifically, the `generate` function checks if the `documents` list is empty, and if so, it appends `NO_CONTEXT_ANSWER` to the pieces (backend/nodes/generator.py:73-74). This behavior is confirmed by the test `test_generate_without_context_never_calls_llm`, which asserts that the result matches `generator.NO_CONTEXT_ANSWER` when no documents are provided (tests/test_generator_node.py:45-53).

**Grade:** Correct

---

## 27. How do the tests verify the routing behavior?

**Expected source:** tests/ (routing tests) + backend/routing.py

**Retrieved sources:**
- tests/test_rewriter_and_routing.py:33-34 (function test_route_goes_to_generate_when_relevant)
- tests/test_rewriter_and_routing.py:41-42 (function test_route_defaults_to_corrective_path_when_relevance_missing)
- tests/test_rewriter_and_routing.py:37-38 (function test_route_goes_to_rewrite_when_irrelevant)
- tests/test_rewriter_and_routing.py:10-11 (function test_clean_query_uses_fallback_when_blank)
- tests/test_rewriter_and_routing.py:1-42 (module (module level))

**Answer:**
> The tests verify the routing behavior by checking the output of the `route_after_grading` function against different inputs:
>
> *   When the input dictionary contains `{"relevance": "relevant"}`, the route is verified to be `"generate"` (tests/test_rewriter_and_routing.py:33-34).
> *   When the input dictionary contains `{"relevance": "irrelevant"}`, the route is verified to be `"rewrite_query"` (tests/test_rewriter_and_routing.py:37-38).
> *   When the input dictionary is empty (`{}`), the route is verified to default to `"rewrite_query"` (tests/test_rewriter_and_routing.py:41-42).

**Grade:** Correct

---

## 28. Why does Flux-CRAG use OpenAI embeddings?

**Expected source:** backend/embeddings.py (uses Ollama nomic-embed-text)

**Retrieved sources:**
- backend/config.py:13-45 (class Settings)
- backend/embeddings.py:1-15 (module (module level))
- backend/state.py:1-28 (module (module level))
- backend/routing.py:1-14 (module (module level))
- backend/embeddings.py:10-15 (function get_embeddings)

**Answer:**
> The provided context does not state that Flux-CRAG uses OpenAI embeddings. Instead, `backend/embeddings.py` indicates that the project uses `OllamaEmbeddings` (backend/embeddings.py:2-10). These embeddings are configured using the `embedding_model` and `ollama_base_url` settings (backend/embeddings.py:10-15), which default to `"nomic-embed-text"` and `"http://localhost:11434"` respectively (backend/config.py:23-25).

**Grade:** Correct

---

## 29. Why does the vector store use Pinecone?

**Expected source:** backend/vectorstore.py (uses persistent ChromaDB)

**Retrieved sources:**
- backend/vectorstore.py:1-18 (module (module level))
- backend/vectorstore.py:11-18 (function get_vectorstore)
- backend/ingestion/indexer.py:34-36 (function collection_count)
- backend/ingestion/indexer.py:1-36 (module (module level))
- backend/nodes/retriever.py:1-54 (module (module level))

**Answer:**
> The provided code context does not mention Pinecone. It explicitly states that the vector store is a "Persistent local ChromaDB vector store" (backend/vectorstore.py:3).

**Grade:** Correct

---

## 30. How does the grader assign a relevance score from 0 to 1 to each chunk?

**Expected source:** backend/nodes/grader.py (structured yes/no verdict with reason, not a score)

**Retrieved sources:**
- backend/nodes/grader.py:22-25 (function _grade_chunk)
- backend/nodes/grader.py:28-104 (function grade_documents)
- backend/nodes/grader.py:13-19 (class GradeResult)
- tests/test_grader_node.py:49-58 (function test_grader_error_counts_as_not_relevant)
- tests/test_grader_node.py:15-17 (function _fake_grade)

**Answer:**
> The provided code does not assign a relevance score from 0 to 1. Instead, the grader performs a binary classification where a chunk is deemed "relevant" if the LLM returns "yes" for its relevance, and "irrelevant" otherwise (backend/nodes/grader.py:41, 45).

**Grade:** Correct

---
