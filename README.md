# ClassiNews - AI-Powered News Classification System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5.1-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**An intelligent web application that automatically classifies news articles into categories using machine learning**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API Documentation](#-api-documentation) • [Training](#-training-the-model)

</div>

### Screenshots

<div align="center">

<img width="600" height="568" alt="Home Page" src="https://github.com/user-attachments/assets/30d350ad-d08c-497a-b274-466cabe3f878" />
<img width="450" height="250" alt="Classification Result" src="https://github.com/user-attachments/assets/6136f928-dc51-4b71-9250-54b7e668d8a5" />
<img width="450" height="250" alt="History Page" src="https://github.com/user-attachments/assets/175f9804-2208-43ee-b9c9-b87c8a893a70" />
<img width="600" height="558" alt="About Page" src="https://github.com/user-attachments/assets/58fa8d4e-635c-456f-8765-c70c24a933dc" />

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Training the Model](#-training-the-model)
- [Performance Metrics](#-performance-metrics)
- [Architecture](#-architecture)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

ClassiNews is a production-ready Flask web application that leverages Natural Language Processing (NLP) and Machine Learning to automatically categorize news articles. The system uses a pre-trained Multinomial Naive Bayes classifier with TF-IDF vectorization to classify news content into four distinct categories:

- **World News** - International events, politics, and global affairs
- **Sports** - Athletic events, competitions, and sports-related news
- **Business** - Financial markets, corporate news, and economic updates
- **Sci/Tech** - Science, technology, and innovation news

The application provides both a user-friendly web interface and a RESTful API, making it suitable for both end-users and developers who want to integrate news classification into their own applications.

---

## ✨ Features

### Core Functionality
- **Real-time Classification**: Instant news article categorization with sub-second response times
- **Confidence Scores**: Provides probability distributions for all categories
- **Prediction History**: Tracks and displays past classifications with statistics
- **Batch Processing Ready**: API supports single and potential batch classification

### User Interface
- **Modern, Responsive Design**: Professional UI that works on desktop and mobile devices
- **Interactive Dashboard**: Real-time results with visual feedback
- **History Tracking**: View past predictions with category statistics
- **Multiple Pages**: Home, About, History, and API Documentation pages

### Developer Features
- **RESTful API**: Clean JSON API for programmatic access
- **Comprehensive Documentation**: In-built API documentation page
- **Error Handling**: Robust error handling with meaningful messages
- **Type Hints**: Full Python type annotations for better code maintainability

---

## 🛠 Technology Stack

### Backend
- **Flask 3.0.3** - Lightweight Python web framework
- **scikit-learn 1.5.1** - Machine learning library for model training and inference
- **NLTK 3.8.1** - Natural Language Toolkit for text preprocessing
- **joblib 1.4.2** - Efficient model serialization and loading

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with custom design system
- **JavaScript (ES6+)** - Interactive functionality and API integration
- **Font Awesome** - Icon library for UI elements

### Machine Learning
- **TF-IDF Vectorization** - Text feature extraction (30,000 features, unigrams + bigrams)
- **Multinomial Naive Bayes** - Probabilistic classifier optimized for text data
- **AG News Dataset** - Training dataset from HuggingFace (120,000+ samples)

### Development Tools
- **Python 3.8+** - Programming language
- **Git** - Version control
- **Virtual Environment** - Dependency isolation

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/S-V-Kartheek/ClassiNews-News_Classifier.git
   cd ClassiNews-News_Classifier
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data** (if not already downloaded)
   ```python
   python -c "import nltk; nltk.download('stopwords')"
   ```

5. **Verify model files exist**
   - `tfidf_vectorizer.joblib`
   - `news_classifier.joblib`
   
   If these files are missing, see the [Training the Model](#-training-the-model) section.

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Web Interface: http://localhost:5000
   - API Endpoint: http://localhost:5000/api/predict

---

## 🚀 Usage

### Web Interface

1. Navigate to the home page at `http://localhost:5000`
2. Paste or type a news article or headline in the text area
3. Click "Classify Article" or press `Ctrl+Enter`
4. View the predicted category with confidence score
5. Check the History page to see past predictions

### API Usage

#### Basic Request

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"article": "Stock markets surge to record highs amid positive economic indicators"}'
```

#### Response Format

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

#### Python Example

```python
import requests

url = "http://localhost:5000/api/predict"
data = {
    "article": "Scientists discover new exoplanet in habitable zone"
}

response = requests.post(url, json=data)
result = response.json()

print(f"Category: {result['prediction']}")
print(f"Confidence: {result['confidence']:.2%}")
```

#### JavaScript Example

```javascript
fetch('http://localhost:5000/api/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    article: 'Champions League final set for next month'
  })
})
.then(response => response.json())
.then(data => {
  console.log('Prediction:', data.prediction);
  console.log('Confidence:', data.confidence);
});
```

---

## 📚 API Documentation

### Endpoint: `/api/predict`

Classifies a news article and returns the predicted category with confidence scores.

#### Method
`POST`

#### Headers
```
Content-Type: application/json
```

#### Request Body
```json
{
  "article": "string"  // Required: News article or headline text
}
```

#### Response Codes

| Code | Description |
|------|-------------|
| 200  | Success - Returns prediction with confidence scores |
| 400  | Bad Request - Missing or empty article text |
| 500  | Internal Server Error - Model loading or processing error |

#### Response Schema

```json
{
  "prediction": "string",      // Predicted category (World, Sports, Business, Sci/Tech)
  "confidence": 0.0-1.0,       // Confidence score (0 to 1)
  "probabilities": {           // Probability distribution across all categories
    "World": 0.0-1.0,
    "Sports": 0.0-1.0,
    "Business": 0.0-1.0,
    "Sci/Tech": 0.0-1.0
  }
}
```

#### Error Response

```json
{
  "error": "Article text is required"
}
```

---

## 📁 Project Structure

```
ClassiNews-News_Classifier/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── TRAINING_INFO.md            # Model training documentation
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navigation
│   ├── home.html              # Main classification interface
│   ├── about.html             # About page with tech details
│   ├── history.html           # Prediction history page
│   ├── api_docs.html          # API documentation page
│   ├── login.html             # Login page
│   └── index.html             # Alternative index page
│
├── static/                    # Static assets
│   ├── style.css              # Main stylesheet
│   └── js/
│       └── main.js            # JavaScript for interactions
│
├── tfidf_vectorizer.joblib    # Pre-trained TF-IDF vectorizer
├── news_classifier.joblib     # Pre-trained classification model
└── prediction_history.json    # Prediction history (auto-generated)
```

---

## 🎓 Training the Model

### Dataset

The model is trained on the **AG News** dataset from HuggingFace, which contains:
- **120,000 training samples**
- **7,600 test samples**
- **4 balanced categories** (30,000 samples each)

### Training Process

1. **Data Preprocessing**
   - Convert text to lowercase
   - Remove URLs and special characters
   - Remove stopwords using NLTK
   - Tokenize and clean text

2. **Feature Extraction**
   - TF-IDF vectorization
   - Maximum 30,000 features
   - Unigrams and bigrams (1-2 word combinations)

3. **Model Training**
   - Multinomial Naive Bayes classifier
   - Alpha parameter: 0.1 (smoothing)
   - 80/20 train/validation split

4. **Model Evaluation**
   - Accuracy: ~91%
   - Per-category precision and recall metrics

### Retraining Instructions

To train your own model:

```bash
# Navigate to parent directory
cd ..

# Run training script
python train_model.py
```

This will:
- Download the AG News dataset (if not cached)
- Train a new model
- Save `tfidf_vectorizer.joblib` and `news_clf_nb.joblib`
- Display accuracy and classification report

Then copy the model files to the `project/` directory:
```bash
copy tfidf_vectorizer.joblib project\
copy news_clf_nb.joblib project\news_classifier.joblib
```

For detailed training information, see [TRAINING_INFO.md](TRAINING_INFO.md).

---

## 📊 Performance Metrics

### Model Performance

| Metric | Value |
|--------|-------|
| **Overall Accuracy** | 91.08% |
| **Average Response Time** | < 200ms |
| **Model Size** | ~50-100 MB |

### Per-Category Performance

| Category | Precision | Recall | F1-Score |
|----------|-----------|--------|----------|
| **Sports** | 0.95 | 0.98 | 0.97 |
| **World** | 0.92 | 0.90 | 0.91 |
| **Sci/Tech** | 0.88 | 0.90 | 0.89 |
| **Business** | 0.89 | 0.87 | 0.88 |

### System Requirements

- **RAM**: Minimum 4GB (4GB recommended)
- **Storage**: ~200MB for application + models
- **CPU**: Any modern processor (training requires more resources)

---

## 🏗 Architecture

### System Design

```
┌─────────────────┐
│   Web Browser   │
│  (User Interface)│
└────────┬────────┘
         │ HTTP Request
         ▼
┌─────────────────┐
│   Flask App     │
│  (app.py)       │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│ Text   │ │   TF-IDF     │
│Cleaner │ │ Vectorizer   │
└───┬────┘ └──────┬───────┘
    │             │
    └──────┬──────┘
           │
           ▼
    ┌──────────────┐
    │   Naive      │
    │   Bayes      │
    │  Classifier  │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  Prediction  │
    │  + Confidence│
    └──────────────┘
```

### Data Flow

1. **Input**: User submits news article text
2. **Preprocessing**: Text is cleaned (lowercase, URLs removed, stopwords removed)
3. **Vectorization**: Cleaned text is converted to TF-IDF feature vector
4. **Classification**: Model predicts category and calculates probabilities
5. **Response**: Prediction with confidence scores returned to user

### Key Components

- **Text Preprocessing Module**: Handles text cleaning and normalization
- **Model Loader**: Efficiently loads pre-trained models at startup
- **Prediction Engine**: Processes requests and generates predictions
- **History Manager**: Tracks and stores prediction history
- **API Layer**: RESTful endpoint for programmatic access

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port number | `5000` |
| `SECRET_KEY` | Flask session secret key | Auto-generated |

### Example Configuration

```bash
# Windows
set PORT=8000
set SECRET_KEY=your-secret-key-here
python app.py

# macOS/Linux
export PORT=8000
export SECRET_KEY=your-secret-key-here
python app.py
```

---

## 🚢 Deployment

### Production Deployment

For production deployment, use a production WSGI server:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Recommended Setup

- **Reverse Proxy**: NGINX or Apache
- **HTTPS**: SSL/TLS certificates (Let's Encrypt)
- **Process Manager**: systemd, supervisor, or PM2
- **Monitoring**: Application performance monitoring tools

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write clear commit messages
- Update documentation for new features
- Test your changes thoroughly

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **AG News Dataset** - Provided by HuggingFace Datasets
- **scikit-learn** - Machine learning library
- **Flask** - Web framework
- **NLTK** - Natural language processing toolkit

---

## 📧 Contact & Support

- **Repository**: [https://github.com/S-V-Kartheek/ClassiNews-News_Classifier](https://github.com/S-V-Kartheek/ClassiNews-News_Classifier)
- **Issues**: [GitHub Issues](https://github.com/S-V-Kartheek/ClassiNews-News_Classifier/issues)

---

## 🔮 Future Enhancements

- [ ] Support for additional news categories
- [ ] Batch processing API endpoint
- [ ] User authentication and personal history
- [ ] Model retraining interface
- [ ] Real-time news feed integration
- [ ] Export functionality (CSV, JSON)
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

---

<div align="center">

**Made with ❤️ using Python, Flask, and Machine Learning**

⭐ Star this repo if you find it helpful!

</div>
