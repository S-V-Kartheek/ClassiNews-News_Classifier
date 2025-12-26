from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from typing import Dict, List, Any, Tuple
import joblib
import re
import nltk
from nltk.corpus import stopwords
from datetime import datetime
import json
import os

# download stopwords if not already there
nltk.download("stopwords", quiet=True)

STOP = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    # clean up the text like we did in training
    text = text.lower()
    text = re.sub(r"http\S+", "", text)  # get rid of urls
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOP]
    return " ".join(tokens)

def load_models() -> Tuple[Any, Any]:
    # load the model files
    vectorizer_path = os.path.join(os.path.dirname(__file__), "tfidf_vectorizer.joblib")
    model_path = os.path.join(os.path.dirname(__file__), "news_classifier.joblib")
    
    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(f"TF-IDF vectorizer not found at {vectorizer_path}")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Classifier model not found at {model_path}")
    
    try:
        tfidf = joblib.load(vectorizer_path)
        model = joblib.load(model_path)
        return tfidf, model
    except Exception as e:
        raise RuntimeError(f"Error loading models: {str(e)}") from e

# using json for now, might switch to db later
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "prediction_history.json")

def load_history() -> List[Dict[str, Any]]:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing history file: {e}")
            return []
        except Exception as e:
            print(f"Error loading history: {e}")
            return []
    return []

def save_history(entry: Dict[str, Any]) -> None:
    history = load_history()
    history.insert(0, entry)
    # keep it to 100 max
    history = history[:100]
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Error saving history: {e}")
        raise

def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24).hex())
    
    # load models at startup
    try:
        tfidf, model = load_models()
    except (FileNotFoundError, RuntimeError) as e:
        print(f"CRITICAL: {e}")
        print("Please ensure model files are in the project directory")
        raise
    
    @app.context_processor
    def inject_globals() -> Dict[str, Any]:
        return {"current_year": datetime.now().year}
    
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")
            
            # basic login check
            if email and password:
                session["logged_in"] = True
                session["email"] = email
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({"success": True, "redirect": url_for("home")})
                return redirect(url_for("home"))
            else:
                error_msg = "Please enter both email and password"
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({"success": False, "error": error_msg}), 400
                return render_template("login.html", error=error_msg, current_year=datetime.now().year)
        
        if session.get("logged_in"):
            return redirect(url_for("home"))
        
        error = request.args.get("error", "")
        return render_template("login.html", error=error, current_year=datetime.now().year)

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/")
    def home():
        return render_template("home.html", current_year=datetime.now().year)

    @app.route("/about")
    def about():
        return render_template("about.html", current_year=datetime.now().year)

    @app.route("/history")
    def history():
        try:
            history_data = load_history()
            stats: Dict[str, Any] = {
                'total': len(history_data),
                'categories': {}
            }
            for entry in history_data:
                cat = entry.get('prediction', 'Unknown')
                stats['categories'][cat] = stats['categories'].get(cat, 0) + 1
            
            return render_template("history.html", 
                                 history=history_data[:20],
                                 stats=stats,
                                 current_year=datetime.now().year)
        except Exception as e:
            print(f"Error loading history page: {e}")
            return render_template("history.html", 
                                 history=[],
                                 stats={'total': 0, 'categories': {}},
                                 current_year=datetime.now().year)

    @app.route("/api-docs")
    def api_docs():
        return render_template("api_docs.html", current_year=datetime.now().year)

    @app.route("/predict", methods=["POST"])
    def predict():
        article = request.form.get("article", "").strip()

        if not article:
            return render_template(
                "home.html",
                error="Please provide an article to classify.",
                current_year=datetime.now().year
            )

        try:
            cleaned = clean_text(article)
            vector = tfidf.transform([cleaned])
            prediction = model.predict(vector)[0]

            entry = {
                'article': article[:200] + "..." if len(article) > 200 else article,
                'prediction': prediction,
                'timestamp': datetime.now().isoformat()
            }
            save_history(entry)

            return render_template(
                "home.html",
                prediction_text="Predicted Category: " + prediction,
                article_text=article,
                current_year=datetime.now().year
            )
        except Exception as e:
            print(f"Error during prediction: {e}")
            return render_template(
                "home.html",
                error="An error occurred while classifying the article. Please try again.",
                current_year=datetime.now().year
            ), 500

    @app.route("/api/predict", methods=["POST"])
    def api_predict():
        try:
            data = request.get_json(silent=True) or {}
            article = data.get("article", "")

            if not article or not article.strip():
                return jsonify({"error": "Article text is required"}), 400

            article = article.strip()
            cleaned = clean_text(article)
            vector = tfidf.transform([cleaned])
            prediction = model.predict(vector)[0]

            probabilities = model.predict_proba(vector)[0]
            classes = model.classes_
            confidence = max(probabilities)

            entry = {
                'article': article[:200] + "..." if len(article) > 200 else article,
                'prediction': prediction,
                'timestamp': datetime.now().isoformat()
            }
            save_history(entry)

            return jsonify({
                "prediction": prediction,
                "confidence": float(confidence),
                "probabilities": {str(classes[i]): float(probabilities[i]) for i in range(len(classes))}
            })
        except ValueError as e:
            return jsonify({"error": f"Invalid input: {str(e)}"}), 400
        except Exception as e:
            print(f"Error in API prediction: {e}")
            return jsonify({"error": "An error occurred while processing your request"}), 500
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
