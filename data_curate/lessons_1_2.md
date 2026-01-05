# NeMo Curator Data Curation Workshop
## Lessons 1 & 2: From Raw Text to Training-Ready Datasets

---

Welcome to the NeMo Curator Data Curation Workshop! In these two hands-on lessons, you'll learn how to transform raw multilingual text data into high-quality, training-ready datasets for Large Language Models.

Data quality is the foundation of effective AI. As the saying goes: *"Garbage in, garbage out."* These lessons will equip you with production-grade techniques to ensure your training data is clean, diverse, and free from sensitive information.

---

## Lesson 1: Basics of Data Curation

### Learning Objectives

By the end of this lesson, you will be able to:

1. **Configure a Dask cluster** for distributed data processing on CPU
2. **Build custom text cleaners** using NeMo Curator's `DocumentModifier` interface
3. **Chain multiple curation steps** using the `Sequential` pipeline
4. **Filter documents** by word count and structural quality
5. **Identify and redact PII** (Personally Identifiable Information) from text data

---

### Task 1.1: Environment Setup & Dask Configuration

**Objective:** Initialize an optimized Dask cluster for CPU-based distributed processing.

**What You'll Do:**
- Verify system resources (CPU cores, RAM, GPU availability)
- Configure a `LocalCluster` with memory-safe settings
- Access the Dask dashboard for monitoring

**Key Concepts:**
| Concept | Description |
|---------|-------------|
| **Dask** | Python library for parallel computing; enables processing datasets larger than memory |
| **LocalCluster** | Dask's single-machine distributed scheduler |
| **Memory Spilling** | Automatic disk-based overflow when RAM is exhausted |
| **Workers** | Independent processes that execute tasks in parallel |

**Configuration Best Practices:**
```
Workers × Memory per Worker = 60-70% of System RAM
Example: 3 workers × 3GB = 9GB (for 15GB system)
```

**💡 Takeaway:** Always configure memory limits *before* processing large datasets. Memory exhaustion causes silent worker crashes.

---

### Task 1.2: Text Cleaning and Unification

**Objective:** Standardize text formatting and remove unwanted elements.

**What You'll Do:**
- Create a custom `QuotationTagUnifier` modifier
- Apply Unicode normalization with `UnicodeReformatter`
- Chain modifiers using `Sequential`

**Operations Performed:**
| Issue | Fix |
|-------|-----|
| Inconsistent quotes (`'` `'` `"` `"`) | Standardize to `'` and `"` |
| Tab characters | Replace with spaces |
| HTML tags | Remove completely |
| URLs and emails in text | Strip embedded links |
| Unicode issues | Normalize using `ftfy` library |

**ML/Libraries Used:**
- **ftfy (fixes text for you):** Automatic Unicode repair and normalization

**Code Pattern:**
```python
from nemo_curator import Sequential
from nemo_curator.modules.modify import Modify

cleaners = Sequential([
    Modify(QuotationTagUnifier()),  # Custom modifier
    Modify(UnicodeReformatter()),   # Built-in Unicode fixer
])
cleaned_dataset = cleaners(dataset)
```

**💡 Takeaway:** Text cleaning is often underestimated. Inconsistent encodings and formatting artifacts can significantly degrade model performance.

---

### Task 1.3: Document Size Filtering

**Objective:** Remove documents that are too short, incomplete, or contain excessive repetition.

**What You'll Do:**
- Apply `WordCountFilter` to remove short documents
- Create a custom `IncompleteDocumentFilter` for structural validation
- Use `RepeatingTopNGramsFilter` to detect repetitive content

**Filtering Criteria:**

| Filter | Threshold | Rationale |
|--------|-----------|-----------|
| Minimum word count | 80 words | Short docs lack context |
| Terminating punctuation | `.` `!` `?` `"` | Incomplete docs are noise |
| 2-gram repetition | ≤20% | Detect spam/boilerplate |
| 3-gram repetition | ≤18% | Detect copied content |
| 4-gram repetition | ≤16% | Detect template text |

**Key Concept - N-grams:**
An n-gram is a contiguous sequence of n words. High repetition ratios indicate:
- Spam or auto-generated content
- Legal boilerplate
- Navigation menus scraped from websites

**💡 Takeaway:** Quality over quantity. Filtering out 30% of documents often *improves* model performance by removing noise.

---

### Task 1.4: PII Identification and Removal

**Objective:** Detect and redact sensitive personal information from training data.

**What You'll Do:**
- Configure Presidio Analyzer for multilingual PII detection
- Build a PII redaction pipeline with `PiiModifier`
- Process documents while preserving semantic meaning

**Supported PII Entities:**
| Entity Type | Examples |
|-------------|----------|
| `PERSON` | Names, nicknames |
| `EMAIL_ADDRESS` | user@example.com |
| `PHONE_NUMBER` | 212-555-5555 |
| `CREDIT_CARD` | Card numbers |
| `US_SSN` | Social Security numbers |
| `ADDRESS` | Street addresses |
| `IP_ADDRESS` | Network addresses |

**ML/Libraries Used:**
- **Presidio Analyzer:** Microsoft's PII detection framework
- **spaCy:** NLP library for Named Entity Recognition (NER)
- **Language Models:** `en_core_web_lg`, `es_core_news_sm`, `fr_core_news_sm`

**Important Configuration:**
```python
PiiModifier(
    batch_size=500,          # Memory-safe batch size
    supported_entities=["PERSON", "EMAIL_ADDRESS"],
    anonymize_action="replace",  # Replace with <PERSON>, <EMAIL>
    device="cpu"             # CPU processing for stability
)
```

**💡 Takeaway:** PII removal is legally required in many jurisdictions (GDPR, CCPA). Always redact before sharing or training.

---

### Lesson 1 Summary

**Complete Curation Pipeline:**
```
Raw Data → Clean & Unify → Filter by Size → Redact PII → Training-Ready
```

**Key Files Created:**
- `curated/01_clean_and_unify/` - Cleaned text
- `curated/02_filter_dataset/` - Size-filtered documents
- `curated/03_redact_pii_data_path/` - PII-redacted output

---

## Lesson 2: Advanced Data Processing

### Learning Objectives

By the end of this lesson, you will be able to:

1. **Initialize GPU-accelerated Dask clusters** for high-performance processing
2. **Classify document languages** using FastText models
3. **Categorize content by domain/topic** using transformer-based classifiers
4. **Perform exact deduplication** using document hashing
5. **Perform fuzzy deduplication** using MinHash + LSH algorithms

---

### Task 2.0: GPU Environment Setup

**Objective:** Configure CUDA environment for GPU-accelerated data processing.

**What You'll Do:**
- Set up CUDA headers for CuPy/cuDF compatibility
- Initialize a GPU Dask cluster with memory-safe settings
- Enable cuDF spilling for large operations

**Key Concepts:**

| Concept | Description |
|---------|-------------|
| **RAPIDS** | NVIDIA's GPU-accelerated data science library suite |
| **cuDF** | GPU DataFrame library (pandas-like API, 50-100x faster) |
| **dask-cuda** | GPU-aware Dask scheduler |
| **RMM (RAPIDS Memory Manager)** | GPU memory pooling for reduced allocation overhead |
| **cuDF Spilling** | Automatic GPU→CPU memory overflow |

**GPU Cluster Configuration (8GB VRAM):**
```python
LocalCUDACluster(
    n_workers=1,              # Single GPU worker
    device_memory_limit="6GB", # Leave 2GB headroom
    rmm_pool_size="6GB",       # Pre-allocated memory pool
)
os.environ["CUDF_SPILL"] = "1"  # Enable spilling
```

**💡 Takeaway:** GPU memory is precious. Always configure limits below physical VRAM and enable spilling for stability.

---

### Task 2.1: Language Separation

**Objective:** Automatically detect and separate documents by language.

**What You'll Do:**
- Download and apply the FastText language identification model
- Classify documents across 176 languages
- Separate corpus into language-specific directories

**Model Details:**

| Property | Value |
|----------|-------|
| **Model** | FastText lid.176.bin |
| **Size** | 131 MB |
| **Languages** | 176 supported |
| **Architecture** | Character-level n-gram embeddings |
| **Speed** | Extremely fast (CPU-based) |

**How FastText Language ID Works:**
1. Text is converted to character-level n-grams
2. N-grams are embedded in a shared vector space
3. Classifier predicts language from aggregated embeddings
4. Confidence score indicates prediction reliability

**Output Structure:**
```
curated/04_language_separation/language/
├── EN/file.jsonl    # English documents
├── FR/file.jsonl    # French documents
└── ES/file.jsonl    # Spanish documents
```

**💡 Takeaway:** Language detection should precede most processing steps. Many models are language-specific.

---

### Task 2.2: Domain Classification

**Objective:** Categorize documents by topic/domain for dataset analysis and filtering.

**What You'll Do:**
- Initialize the MultilingualDomainClassifier
- Handle GPU memory constraints during model initialization
- Classify documents into 26 domain categories

**Model Details:**

| Property | Value |
|----------|-------|
| **Model** | microsoft/mdeberta-v3-base |
| **Fine-tuned by** | NVIDIA (nvidia/multilingual-domain-classifier) |
| **Architecture** | DeBERTa V3 Transformer (86M parameters) |
| **Languages** | 52 supported |
| **Domains** | 26 categories |
| **Inference** | GPU-accelerated via CrossFit |

**Domain Categories:**
```
Arts_and_Entertainment, Autos_and_Vehicles, Beauty_and_Fitness,
Books_and_Literature, Business_and_Industrial, Computers_and_Electronics,
Finance, Food_and_Drink, Games, Health, Hobbies_and_Leisure,
Home_and_Garden, Internet_and_Telecom, Jobs_and_Education,
Law_and_Government, News, Online_Communities, People_and_Society,
Pets_and_Animals, Real_Estate, Science, Sensitive_Subjects,
Shopping, Sports, Travel_and_Transportation, Adult
```

**Memory-Safe Configuration (8GB GPU):**
```python
MultilingualDomainClassifier(
    batch_size=8,       # Very small for memory safety
    max_chars=512,      # Truncate long documents
    autocast=True,      # Mixed precision (FP16)
    max_mem_gb=4,       # Conservative limit
)
```

**Key Libraries:**
- **CrossFit:** RAPIDS library for running transformer models on GPUs efficiently
- **Hugging Face Transformers:** Model loading and tokenization

**💡 Takeaway:** Domain classification enables data blending—mixing topics in specific ratios improves model generalization.

---

### Task 2.3: Document Deduplication

#### 2.3.1: Adding Unique IDs

**Objective:** Assign unique identifiers to every document for deduplication tracking.

**Pattern:**
```python
from nemo_curator import AddId

add_id = AddId(
    id_field="id",
    id_prefix="FR_data",  # Language-specific prefix
    start_index=0
)
# Output: FR_data-0000000000, FR_data-0000000001, ...
```

---

#### 2.3.2: Exact Deduplication

**Objective:** Remove byte-identical duplicate documents.

**How It Works:**
1. Compute MD5/SHA hash of each document's text
2. Group documents by hash
3. Keep only the first occurrence per hash group

**Configuration:**
```python
ExactDuplicates(
    id_field="id",
    text_field="text",
    hash_method="md5",  # or "sha256"
)
```

**Performance:** Extremely fast—O(n) time complexity.

**💡 Takeaway:** Exact duplicates are common in web scrapes (syndicated content, boilerplate). Always dedupe before training.

---

#### 2.3.3: Fuzzy Deduplication

**Objective:** Remove near-duplicate documents (paraphrases, slight edits).

**Algorithm: MinHash + LSH (Locality-Sensitive Hashing)**

| Stage | Operation | Purpose |
|-------|-----------|---------|
| 1 | MinHash | Create compact document signatures from n-gram shingles |
| 2 | LSH Bucketing | Hash similar documents to same buckets |
| 3 | Connected Components | Find all documents in same similarity cluster |

**Key Parameters:**

| Parameter | Default | Effect |
|-----------|---------|--------|
| `char_ngrams` | 24 | Shingle size (larger = stricter matching) |
| `num_buckets` | 20 | LSH bands (more = higher recall) |
| `hashes_per_bucket` | 13 | Rows per band (more = higher precision) |
| `false_positive_check` | False | Enable for higher precision (slower) |

**Similarity Threshold:**
The combination of `num_buckets` and `hashes_per_bucket` determines the Jaccard similarity threshold. Default settings catch documents with ~80% similarity.

**Memory-Optimized Configuration:**
```python
FuzzyDuplicatesConfig(
    buckets_per_shuffle=1,  # Reduce memory pressure
    use_64_bit_hash=False,  # 32-bit for memory efficiency
)
```

**GPU Libraries Used:**
- **cugraph:** GPU-accelerated graph algorithms (connected components)
- **cuDF:** GPU DataFrames for MinHash computation

**💡 Takeaway:** Fuzzy deduplication catches paraphrases and near-copies that exact dedup misses. Essential for web-scraped data.

---

### Lesson 2 Summary

**Complete Advanced Pipeline:**
```
Cleaned Data → Language Separation → Domain Classification → Add IDs → Exact Dedup → Fuzzy Dedup
```

**Key Files Created:**
- `curated/04_language_separation/` - Language-separated corpora
- `curated/05_domain_classification/` - Domain-annotated data
- `curated/06_add_id/` - Documents with unique IDs
- `curated/07_Deduplicate/exact/` - Exact-deduplicated data
- `curated/07_Deduplicate/fuzzy_wrapper/` - Fuzzy-deduplicated data

---

## Key Takeaways

### Data Quality Principles

1. **Clean early, clean often** - Text cleaning prevents downstream errors
2. **Filter aggressively** - Less data of higher quality beats more noisy data
3. **Deduplicate thoroughly** - Both exact and fuzzy methods are necessary
4. **Protect privacy** - PII redaction is a legal and ethical requirement
5. **Know your data** - Language and domain classification enable informed decisions

### Technology Stack Summary

| Category | Tool | Purpose |
|----------|------|---------|
| **Distributed Computing** | Dask | CPU parallelization |
| **GPU Acceleration** | RAPIDS (cuDF, dask-cuda, cugraph) | GPU-parallel data processing |
| **Text Processing** | ftfy, regex | Unicode normalization, pattern matching |
| **Language ID** | FastText | Multilingual classification |
| **Domain Classification** | DeBERTa V3 + CrossFit | Topic categorization |
| **PII Detection** | Presidio + spaCy | Named entity recognition |
| **Deduplication** | MD5/SHA, MinHash+LSH | Exact and fuzzy matching |

### Models Used

| Model | Task | Size | Speed |
|-------|------|------|-------|
| **FastText lid.176.bin** | Language ID | 131 MB | Very fast (CPU) |
| **mDeBERTa-v3-base** | Domain classification | ~500 MB | GPU-accelerated |
| **spaCy NER models** | PII detection | 50-500 MB | CPU |

---

## Next Steps

After completing these lessons, you're ready to:

1. **Scale up** - Apply these pipelines to terabyte-scale datasets using multi-node clusters
2. **Customize** - Build domain-specific filters and classifiers
3. **Integrate** - Connect curation pipelines to model training workflows
4. **Explore** - Continue to Lesson 3: Synthetic Data Generation

---

*"The quality of your model is bounded by the quality of your data."*

Happy curating! 🚀

