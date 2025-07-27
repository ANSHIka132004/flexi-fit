import base64
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import DailyHealthData, WeeklyStats
import json
from .predictor import predict_dish
from .utils import get_nutrition_info
from .speechRecognition import transcribe_audio as sr_transcribe
from .spaCy import extract_goal_from_text as spacy_extract
from .cohere_bot import cohere_generate as cohere_response
from gtts import gTTS
import uuid
import os
from django.conf import settings
from django.shortcuts import render  # Make sure this line is present at the top

def login_view(request):
    return render(request, 'login.html')





def landing_view(request):
    return render(request, "landing.html")


def predict_view(request):
    context = {}
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        try:
            # Updated: get both label and confidence
            prediction, confidence = predict_dish(image)
            nutrition_info = get_nutrition_info(prediction.lower())

            context = {
                "prediction": {
                    "food_name": prediction,
                    "confidence": round(confidence * 100, 2),  # as percentage
                },
                "nutrition": nutrition_info,
            }
        except Exception as e:
            context["error"] = f"Prediction error: {str(e)}"
    return render(request, "predict.html", context)


def meal_planner_view(request):
    chat_messages = []
    if request.method == "POST":
        user_message = request.POST.get("user_message")
        if user_message:
            chat_messages.append({
                'content': user_message,
                'is_user': True
            })
            try:
                prompt = (
                    f"Create a healthy Indian meal plan for: {user_message}\n"
                    "Format the response as follows:\n"
                    "Breakfast:\n- [Dish 1] ([Calories] kcal)\n- [Dish 2] ([Calories] kcal)\n"
                    "Lunch:\n- [Dish 1] ([Calories] kcal)\n- [Dish 2] ([Calories] kcal)\n"
                    "Dinner:\n- [Dish 1] ([Calories] kcal)\n- [Dish 2] ([Calories] kcal)\n"
                    "Snacks:\n- [Dish 1] ([Calories] kcal)\n"
                    "Add a short nutrition tip at the end, and use clear line breaks."
                )
                ai_response = cohere_response(prompt)
                chat_messages.append({
                    'content': ai_response,
                    'is_user': False
                })
            except Exception as e:
                chat_messages.append({
                    'content': f"Cohere error: {str(e)}",
                    'is_user': False
                })
    return render(request, "meal_planner.html", {
        "chat_messages": chat_messages
    })


def workout_planner_view(request):
    workout_plan = None
    response = None
    transcript = None
    if request.method == "POST":
        if request.FILES.get("audio"):
            try:
                audio = request.FILES["audio"]
                transcript = sr_transcribe(audio)
                fitness_goal = spacy_extract(transcript)
                prompt = f"Generate a 7-day workout plan for someone with this goal: {fitness_goal}"
                response = cohere_response(prompt)
            except Exception as e:
                response = f"Error: {str(e)}"
        else:
            fitness_level = request.POST.get("fitness_level")
            goal = request.POST.get("goal")
            duration = request.POST.get("duration")
            days_per_week = request.POST.get("days_per_week")
            equipment = request.POST.get("equipment")
            notes = request.POST.get("notes", "")
            prompt = f"""Generate a structured 7-day workout plan for someone with these specifications:
- Fitness Level: {fitness_level}
- Primary Goal: {goal}
- Workout Duration: {duration} minutes
- Days per Week: {days_per_week}
- Equipment Available: {equipment}
- Additional Notes: {notes}

Please format the response with clear sections and bullet points like this:

**Day 1: [Day Name]**
- Exercise 1: [Description]
- Exercise 2: [Description]
- Exercise 3: [Description]

**Day 2: [Day Name]**
- Exercise 1: [Description]
- Exercise 2: [Description]
- Exercise 3: [Description]

Continue for all 7 days with clear formatting and specific exercises."""
            try:
                workout_plan = cohere_response(prompt)
            except Exception as e:
                workout_plan = f"Cohere error: {str(e)}"

    return render(request, "workout_planner.html", {
        "workout_plan": workout_plan,
        "response": response,
        "transcript": transcript
    })


def voice_goal_view(request):
    response = None
    transcript = None
    audio_url = None
    if request.method == "POST":
        audio_file = None
        audio_data = request.POST.get("audio_data")
        if audio_data:
            header, b64data = audio_data.split(",", 1)
            audio_bytes = base64.b64decode(b64data)
            temp = tempfile.NamedTemporaryFile(delete=False, suffix='.webm')
            temp.write(audio_bytes)
            temp.flush()
            temp.seek(0)
            audio_file = temp
        elif request.FILES.get("audio"):
            audio_file = request.FILES["audio"]
        if audio_file:
            try:
                transcript = sr_transcribe(audio_file)
                goal = spacy_extract(transcript)
                prompt = f"Generate a personalized workout plan for the goal: {goal}"
                response = cohere_response(prompt)
                # --- gTTS Text-to-Speech ---
                if response and not response.startswith("Error"):
                    try:
                        tts = gTTS(text=response, lang='en')
                        filename = f"ai_speech_{uuid.uuid4().hex}.mp3"
                        media_dir = os.path.join(settings.BASE_DIR, 'predictor', 'static', 'ai_speech')
                        os.makedirs(media_dir, exist_ok=True)
                        audio_path = os.path.join(media_dir, filename)
                        tts.save(audio_path)
                        audio_url = f"/static/ai_speech/{filename}"
                    except Exception as tts_error:
                        print(f"gTTS Error: {tts_error}")
                        audio_url = None
            except Exception as e:
                response = f"Error: {str(e)}"
            finally:
                if audio_data and audio_file:
                    audio_file.close()
        else:
            response = "No audio data received."
    return render(request, "voice_goal.html", {
        "response": response,
        "transcript": transcript,
        "audio_url": audio_url
    })


def daily_analyzer_view(request):
    """Daily calorie and steps analyzer dashboard"""
    today = timezone.now().date()
    
    # Get or create today's data
    daily_data, created = DailyHealthData.objects.get_or_create(
        date=today,
        defaults={
            'food_calories': 0,
            'exercise_calories': 0,
            'steps': 1550,  # Default starting steps
            'exercise_time': 0,
            'base_goal': 2050
        }
    )
    
    # Get weekly stats
    week_start = today - timedelta(days=today.weekday())
    weekly_stats, created = WeeklyStats.objects.get_or_create(
        week_start=week_start,
        defaults={
            'total_calories': 0,
            'total_steps': 0,
            'total_exercise_calories': 0,
            'active_days': 0
        }
    )
    
    # Calculate weekly stats
    week_data = DailyHealthData.objects.filter(
        date__gte=week_start,
        date__lte=today
    )
    
    weekly_stats.total_calories = sum(d.food_calories for d in week_data)
    weekly_stats.total_steps = sum(d.steps for d in week_data)
    weekly_stats.total_exercise_calories = sum(d.exercise_calories for d in week_data)
    weekly_stats.active_days = week_data.count()
    weekly_stats.save()
    
    context = {
        'daily_data': daily_data,
        'weekly_stats': weekly_stats,
        'today': today
    }
    
    return render(request, "daily_analyzer.html", context)

def update_health_data(request):
    """AJAX endpoint to update health data"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            today = timezone.now().date()
            
            # Get or create today's data
            daily_data, created = DailyHealthData.objects.get_or_create(
                date=today,
                defaults={'base_goal': 2050}
            )
            
            # Update fields
            daily_data.food_calories = data.get('food_calories', 0)
            daily_data.exercise_calories = data.get('exercise_calories', 0)
            daily_data.steps = data.get('steps', 0)
            daily_data.exercise_time = data.get('exercise_time', 0)
            daily_data.save()
            
            # Update weekly stats
            week_start = today - timedelta(days=today.weekday())
            weekly_stats, created = WeeklyStats.objects.get_or_create(
                week_start=week_start,
                defaults={
                    'total_calories': 0,
                    'total_steps': 0,
                    'total_exercise_calories': 0,
                    'active_days': 0
                }
            )
            
            week_data = DailyHealthData.objects.filter(
                date__gte=week_start,
                date__lte=today
            )
            
            weekly_stats.total_calories = sum(d.food_calories for d in week_data)
            weekly_stats.total_steps = sum(d.steps for d in week_data)
            weekly_stats.total_exercise_calories = sum(d.exercise_calories for d in week_data)
            weekly_stats.active_days = week_data.count()
            weekly_stats.save()
            
            return JsonResponse({
                'success': True,
                'daily_data': {
                    'food_calories': daily_data.food_calories,
                    'exercise_calories': daily_data.exercise_calories,
                    'steps': daily_data.steps,
                    'exercise_time': daily_data.exercise_time,
                    'remaining_calories': daily_data.remaining_calories,
                    'steps_progress': daily_data.steps_progress,
                    'exercise_progress': daily_data.exercise_progress
                },
                'weekly_stats': {
                    'total_calories': weekly_stats.total_calories,
                    'total_steps': weekly_stats.total_steps,
                    'total_exercise_calories': weekly_stats.total_exercise_calories,
                    'active_days': weekly_stats.active_days
                }
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
