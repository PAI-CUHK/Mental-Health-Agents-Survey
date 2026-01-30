# Mental Health Agents Survey

This repository supports the paper "A Scoping Review of Artificial Intelligence Agents in Mental Health."

## 1) Overview
We conduct a scoping review of mental health AI agent systems published from Jan 1st 2023 to Dec 31, 2025, using a six dimension audit framework that characterizes each system by its system type (base model lineage, interface modality, and workflow composition), data scope (modalities and provenance), mental health focus (mapped to ICD 11 diagnostic groupings), demographic coverage (age strata, geography, and sex representation), downstream tasks (screening and triage, clinical decision support, therapeutic intervention, documentation, ethical and legal support, and education or simulation), and evaluation types (automated metrics, language quality benchmarks, safety stress tests, expert review, and clinician or patient involvement).

## 2) Methods
### 2.1 Information sources and search strategy
Search query used for initial retrieval.
```
(Agent OR Chatbot) AND (AI OR LLM OR Large Language Model) AND (Mental Health OR Psychiatry OR Psychology)
```
Implementation details are in `searching/searches.py`.

### 2.2 Duplicates Removal
We remove duplicates by computing Jaccard similarity over a concatenated string of title and author list, then merging records above a chosen similarity threshold.

Implementation details are in `filtering/duplicates_removal.py`.

### 2.3 LLM-assisted filterings and human screening
We apply a three stage filtering workflow to obtain a final set of primary system studies suitable for synthesis.

1. First filtering: Eligibility check  
We verify that each retained record matches the intended query scope and is consistent with the retrieval logic used in the search pipeline.
Implementation details are in `filtering/filter1.py`.

2. Second filtering: Exclude non primary study types  
We remove records that are not primary system studies, including reviews, surveys, opinion or editorial pieces, and purely observational studies.
Implementation details are in `filtering/filter2.py`.

**Downloading**
Before the third filtering stage, we downloaded the full texts of the retained papers to support content based screening. The script `download/download.py` can help to download papers from arXiv and medRxiv.

3. Third filtering: Content based exclusions with LLM assistance  
We remove records that are unlikely to support downstream synthesis. This includes papers that use no data, report no evaluation or only superficial evaluation, or fall outside our ICD 11 based mental health scope. The prompt used for this step is provided below.  
Implementation details are in `filtering/filter3.py`.

4. Human screening  
We then conduct a full human review of the remaining papers. The final included set contains 326 papers. Paper metadata are available in `data/final_all_with_dates.csv`.

## 4) LLM assisted annotation

### 4.1 Six dimensions
We use an LLM to assist annotation of each paper along six dimensions.

1. System type  
2. Data scope  
3. Mental health focus  
4. Demographics  
5. Downstream tasks  
6. Evaluation type  

The detailed categories and elaborations are in `annotation/prompt_guidelines.txt`, and the implementation details are in `annotation/annotate.py`.

### 4.2 Reliability and annotation procedure
To assess reliability, we randomly sampled 15 papers and asked three reviewers to independently annotate each paper, using the model output only as optional hints. Across 435 tag assignments, Krippendorff's alpha was approximately 0.81, indicating strong agreement.

After establishing reliability, three reviewers annotated the remaining papers independently. Final annotations are stored in `data/final_all_with_dates.csv`, where blank cells indicate `False`.























