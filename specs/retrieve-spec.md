# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Query approach

*Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?*

```
I'll be calling _collection.query() like this:
    results = _collection.query(
        query_texts = [query],
        n_results = n_results,
        include=["documents", "metadatas","distances"]
    )
```

---

### Return structure

*Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?*

```
  {               
      "text": "A settlement may not be built adjacent to...",
      "game": "catan",                                                                                                                                                                               
      "distance": 0.18
  }                                                                                                                                                                                                  
                  
  - text comes from results["documents"]                                                                                                                                                             
  - game comes from results["metadatas"]
  - distance comes from results["distances"] 
```

---

### Handling the nested result structure

*`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists.*

```
Nesting exists bc ChromaDB supports multiple queries at once. 

  So results["documents"] looks like:
  [                                                                                                                                                                                                  
      ["chunk text 1", "chunk text 2", "chunk text 3"]  # ← index [0], your one query
  ]                                                                                  
                                                                                                                                                                                                     
  You need results["documents"][0] to get the actual list. Same for metadatas and distances — always [0].
                                                                                                             
```

---

### Relevance threshold

*Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?*

```
- Return all `n_results` no matter what: It is simple and predictable, however, can include irrelevant chunks such as some with scores of 0.9
- Filters out chunks above a distance cutoff (e.g. 0.5): It can have cleaner context for the LLM, however can return no results for weird queries.

Approach: Don't filter out for now, we can let the generator decide. Once complete build test and reasses. 
```

---

### Edge cases

*How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?*

```
[your answer here]
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**Test query and top result returned:**

```
Query: `What happens when you roll a 7?`
Top result game: Catan
Distance score: 0.466
Does it make sense? no it just says `x, that hex produces no resources that turn, regardless of the number rolled.`
```

**One thing about the query results that surprised you:**

```
[your answer here]
```
