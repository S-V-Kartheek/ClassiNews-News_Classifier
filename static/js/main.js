const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const navLinks = document.getElementById('navLinks');

if (mobileMenuToggle && navLinks) {
    mobileMenuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        mobileMenuToggle.classList.toggle('active');
    });

    document.addEventListener('click', (e) => {
        if (!navLinks.contains(e.target) && !mobileMenuToggle.contains(e.target)) {
            navLinks.classList.remove('active');
            mobileMenuToggle.classList.remove('active');
        }
    });

    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            mobileMenuToggle.classList.remove('active');
        });
    });
}

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.style.opacity = '0';
        mainContent.style.transition = 'opacity 0.3s ease';
        setTimeout(() => {
            mainContent.style.opacity = '1';
        }, 100);
    }
});

if (!window.homePageScriptLoaded) {
    document.querySelectorAll('.sample-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const articleInputEl = document.getElementById('article');
            if (articleInputEl) {
                const text = btn.querySelector('.example-text')?.textContent || btn.textContent;
                articleInputEl.value = text;
                articleInputEl.focus();
                articleInputEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    });
}

const articleInputOld = document.getElementById('articleInput');
const classifyBtn = document.getElementById('classifyBtn');
const resultCard = document.getElementById('resultCard');
const predictionTag = document.getElementById('predictionTag');
const predictionText = document.getElementById('predictionText');
const predictionMeta = document.getElementById('predictionMeta');

if (classifyBtn && articleInputOld) {
    const setBusy = (busy) => {
        classifyBtn.disabled = busy;
        classifyBtn.classList.toggle("opacity-60", busy);
        classifyBtn.classList.toggle("cursor-not-allowed", busy);
    };

    const showResultCard = () => {
        if (resultCard && !resultCard.classList.contains("show")) {
            resultCard.classList.add("show");
        }
    };

    const displayResult = (category) => {
        if (predictionTag) predictionTag.textContent = category;
        if (predictionText) predictionText.textContent = category;
        if (predictionMeta) predictionMeta.textContent = "Classification complete.";
        showResultCard();
    };

    const displayError = (message) => {
        if (predictionTag) {
            predictionTag.textContent = "Error";
            predictionTag.className = "inline-flex items-center rounded-full px-4 py-1 text-sm font-semibold bg-white/10 text-white/80";
        }
        if (predictionText) predictionText.textContent = "";
        if (predictionMeta) predictionMeta.textContent = message;
        showResultCard();
    };

    const classify = async () => {
        const article = articleInputOld.value.trim();

        if (!article) {
            displayError("Please paste or type a headline/article first.");
            return;
        }

        setBusy(true);
        if (predictionMeta) predictionMeta.textContent = "Classifying...";
        if (predictionTag) predictionTag.textContent = "Processing";
        if (predictionText) predictionText.textContent = "";
        showResultCard();

        try {
            const response = await fetch("/api/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ article }),
            });

            const payload = await response.json();

            if (!response.ok) {
                throw new Error(payload.error || "Unable to classify right now.");
            }

            displayResult(payload.prediction);
        } catch (error) {
            displayError(error.message);
        } finally {
            setBusy(false);
        }
    };

    classifyBtn.addEventListener("click", classify);

    articleInputOld.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
            event.preventDefault();
            classify();
        }
    });
}

