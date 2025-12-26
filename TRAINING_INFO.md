# Dataset and Training Information

## Dataset: AG News

The model is trained on the **AG News** dataset from HuggingFace.

### Dataset Details
- **Source**: HuggingFace Datasets (`datasets` library)
- **Name**: `ag_news`
- **Size**: ~120,000 training samples, ~7,600 test samples
- **Categories**: 4 classes
  - 0: World News
  - 1: Sports
  - 2: Business
  - 3: Sci/Tech
- **Format**: Each sample has `text` (article) and `label` (0-3)

### How Dataset is Loaded

The dataset is **automatically downloaded** from HuggingFace when you run the training script. It's not stored in the repository.

```python
from datasets import load_dataset
ds = load_dataset("ag_news")
```

This downloads the dataset on first use and caches it locally (usually in `~/.cache/huggingface/`).

## Training Script Location

**Training file**: `genai-project/train_model.py` (in the root folder, not in project/)

### Training Process

1. **Load dataset** from HuggingFace
2. **Preprocess text**:
   - Convert to lowercase
   - Remove URLs
   - Remove special characters
   - Remove stopwords (NLTK)
3. **Split data**: 80% train, 20% validation
4. **Feature extraction**: TF-IDF vectorization (max 30,000 features, unigrams + bigrams)
5. **Train model**: Multinomial Naive Bayes (alpha=0.1)
6. **Save models**: 
   - `tfidf_vectorizer.joblib`
   - `news_clf_nb.joblib`

### To Train the Model

```bash
cd genai-project
python train_model.py
```

This will:
- Download AG News dataset (if not already cached)
- Train the model
- Save model files to the current directory
- Print accuracy and classification report

### Expected Results

- **Accuracy**: ~94% on validation set
- **Training time**: ~2-5 minutes (depending on hardware)
- **Model files**: ~50-100 MB total

## Model Files Location

After training, copy these files to `project/` directory:
- `tfidf_vectorizer.joblib` → `project/tfidf_vectorizer.joblib`
- `news_clf_nb.joblib` → `project/news_classifier.joblib`

The app loads these from the `project/` directory.

## Notes

- The dataset is **not included** in the repository (too large)
- Dataset is downloaded automatically on first training run
- Pre-trained models are included in `project/` folder
- You can retrain anytime by running `train_model.py`


