# flexi-fit
django based web application having inbuild ai features related to fitness
An AI-powered full-stack fitness web app built with Django and modern AI/ML technologies to help users achieve their fitness goals with personalized meal and workout plans.


🚀 Features
🍽️ Meal Planner Bot (Gemini): Chat-based personalized meal suggestions.

🗣️ Voice-Based MealBot: Interacts via speech and gives spoken meal advice using AI.

📷 Food Image Classifier: Upload food images and get nutrient information using a CNN model.

🧠 AI Workout Planner: Generates 7-day workout plans based on fitness goals.

🎙️ Voice-to-Goal Detection: Users speak their goals, and AI detects and plans accordingly.

🧾 BMI, TDEE & Calorie Calculations: Auto-calculates user metrics based on inputs.

🧠 Goal Extraction with spaCy: Extract fitness goals from text input using NLP.

🔐 Login/Signup: Secure authentication and user data storage.


## 🛠️ Tech Stack
🌐 Frontend
HTML5, CSS3, Bootstrap

JavaScript
## ⚙️ Backend
Django (Python web framework)

Django REST Framework (for APIs)

SQLite / PostgreSQL (Database)

🤖 AI/ML & NLP
OpenAI GPT / Gemini API (meal & workout suggestions)

TensorFlow / Keras CNN Model (food image classification)

spaCy (goal extraction from voice/text)

SpeechRecognition (voice input)

🔊 Other Tools & Libraries
gTTS (text-to-speech)

pydub (audio handling)

dotenv (API key management)

Pillow (image handling)

MealApp/
│
├── static/                # CSS, JS, images
├── templates/             # HTML templates
├── food_classifier/       # CNN model, image preprocessing
├── ai_utils/
│   ├── speech_to_text.py  # Voice input processing
│   ├── spacy.py           # Goal extraction via spaCy
│
├── mealapp/
│   ├── views.py           # Core logic for each feature
│   ├── models.py          # User and image models
│   ├── urls.py            # Routing
│
├── db.sqlite3             # Database
├── manage.py
└── requirements.txt


# Environment Setup
1. Clone the Repo
bash
Copy
Edit
git clone https://github.com/ANSHIka132004/flexi-fit.git
cd flexi-fit
2. Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
3. Setup .env File
env
Copy
Edit
OPENAI_API_KEY=your_openai_key
COHERE_API_KEY=your_cohere_key
4. Run the App
bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
Visit http://127.0.0.1:8000 🎉

# Model Info
🍱 CNN Image Classifier
Trained on Food-11 dataset (~16K images)

Achieves ~85% accuracy

Uses ResNet-based architecture (custom or transfer learning)

# Dependencies
bash
Copy
Edit
Django
tensorflow
opencv-python
Pillow
SpeechRecognition
gTTS
pydub
python-dotenv
spacy
cohere
openai

check this out-> <img width="554" height="798" alt="Screenshot 2025-07-27 213336" src="https://github.com/user-attachments/assets/d1485f90-a3c5-40e2-af81-e6ed67284eb7" />
<img width="544" height="809" alt="Screenshot 2025-07-27 213724" src="https://github.com/user-attachments/assets/886407e4-43c3-440a-8071-85a24644c800" />
<img width="552" height="791" alt="Screenshot 2025-07-27 213938" src="https://github.com/user-attachments/assets/ce6a0f29-3b7f-4844-8668-8dce1ee4b4e8" />


