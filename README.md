# ClassiNews

News classification web app built with Flask and scikit-learn. Classifies news articles into World, Sports, Business, or Sci/Tech categories.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
python app.py
```

3. Open `http://localhost:5000` in your browser

## Features

- Web interface for classifying news articles
- REST API endpoint at `/api/predict`
- Prediction history page
- About page with tech details
- API documentation

## API Example

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"article": "Stock market reaches new highs"}'
```

Returns:
```json
{
  "prediction": "Business",
  "confidence": 0.92,
  "probabilities": {
    "World": 0.03,
    "Sports": 0.02,
    "Business": 0.92,
    "Sci/Tech": 0.03
  }
}
```

## Files

- `app.py` - Main Flask application
- `templates/` - HTML templates
- `static/` - CSS and JavaScript files
- `tfidf_vectorizer.joblib` - Pre-trained vectorizer
- `news_classifier.joblib` - Pre-trained classifier model

## Requirements

- Python 3.8+
- Flask
- scikit-learn
- NLTK
- joblib

See `requirements.txt` for full list.

## Training the Model

The model is trained on the **AG News** dataset from HuggingFace. See `TRAINING_INFO.md` for details.

To train your own model:
```bash
cd ..
python train_model.py
```

This downloads the AG News dataset and trains a new model. Then copy the `.joblib` files to the `project/` directory.

## Notes

- Model files need to be in the project directory
- History is saved to `prediction_history.json` (max 100 entries)
- Dataset is downloaded automatically from HuggingFace (not stored in repo)

