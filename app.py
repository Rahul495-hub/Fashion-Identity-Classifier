from flask import Flask, render_template, request, redirect, url_for, session, flash
import numpy as np
import os
import logging
from fashion_classifier import FashionClassifier

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize the classifier and load the trained model
classifier = FashionClassifier()
if not classifier.load_model():
    logger.warning("No trained model found. Please run train_model.py first.")

# Shopping Segments
SHOPPING_SEGMENTS = [
    {
        "name": "Trendsetter",
        "description": "You're always at the forefront of fashion, quickly adopting new styles and influencing others. You follow fashion blogs, social media influencers, and stay updated on runway trends.",
        "recommendations": "Focus on bold statement pieces that showcase your fashion-forward perspective. Mix high-street brands with unique finds to create signature looks.",
        "shopping_habits": "Regular shopping at cutting-edge boutiques, online trend-focused retailers, and designer sample sales",
        "image": "trendsetter.jpg"
    },
    {
        "name": "Budget Conscious Shopper",
        "description": "You have a keen eye for value and prioritize cost-effectiveness without sacrificing style. You're strategic about your purchases and know how to create stylish outfits affordably.",
        "recommendations": "Invest in versatile basics that can be mixed and matched, and add affordable trend pieces seasonally. Look for quality at discount stores and during sales events.",
        "shopping_habits": "Sales shopping, thrift stores, outlet malls, and budget-friendly retailers",
        "image": "budget.jpg"
    },
    {
        "name": "Luxury Enthusiast",
        "description": "You appreciate fine craftsmanship and are willing to invest in high-quality pieces. You value exclusivity, premium materials, and the heritage of luxury brands.",
        "recommendations": "Focus on timeless investment pieces from established luxury houses. Choose quality over quantity and build a curated collection of signature items.",
        "shopping_habits": "Designer boutiques, high-end department stores, and exclusive shopping experiences",
        "image": "luxury.jpg"
    },
    {
        "name": "Sustainable Conscious",
        "description": "You prioritize ethical and environmental considerations in your shopping choices. You research brands' practices and prefer companies with transparent supply chains.",
        "recommendations": "Look for certified sustainable brands, secondhand luxury, and timeless designs with long lifespans. Invest in quality pieces made with eco-friendly materials.",
        "shopping_habits": "Ethical brands, secondhand marketplaces, vintage stores, and local artisan shops",
        "image": "sustainable.jpg"
    },
    {
        "name": "Convenience Seeker",
        "description": "You value efficiency and ease in your shopping experience. Time is precious to you, and you prefer straightforward shopping with minimal decision-making.",
        "recommendations": "Use subscription services and personal shoppers to streamline your wardrobe updates. Build a capsule wardrobe of reliable basics that work well together.",
        "shopping_habits": "Online shopping, subscription services, and one-stop retailers with wide selections",
        "image": "convenience.jpg"
    }
]

# Questions for the quiz
QUESTIONS = [
    {
        'id': 0,
        'text': 'How often do you shop for new clothes?',
        'options': ['Weekly', 'Monthly', 'Quarterly']
    },
    {
        'id': 1,
        'text': 'Where do you typically shop for clothes?',
        'options': ['Fast Fashion', 'Department Stores', 'Luxury Boutiques']
    },
    {
        'id': 2,
        'text': 'What influences your clothing purchases the most?',
        'options': ['Trends', 'Price', 'Quality']
    },
    {
        'id': 3,
        'text': 'How would you describe your go-to daily outfit?',
        'options': ['Trendy', 'Business Casual', 'Formal']
    },
    {
        'id': 4,
        'text': 'If you had to choose, would you prefer timeless pieces or trendy items?',
        'options': ['Trendy', 'Mix', 'Timeless']
    }
]

@app.route('/')
def index():
    # Reset session on home page visit
    session.clear()
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    if 'current_question' not in session:
        session['current_question'] = 0
        session['answers'] = {}
    return render_template('quiz.html', 
                         question=QUESTIONS[session['current_question']]['text'],
                         options=QUESTIONS[session['current_question']]['options'],
                         current_question=session['current_question'],
                         total_questions=len(QUESTIONS),
                         progress=(session['current_question'] / len(QUESTIONS)) * 100)

@app.route('/answer', methods=['POST'])
def answer():
    answer = request.form.get('answer')
    if answer is None:
        flash('Please select an answer')
        return redirect(url_for('quiz'))
    
    # Store answer with question ID
    question_id = QUESTIONS[session['current_question']]['id']
    session['answers'][f'{question_id + 1}.{QUESTIONS[session["current_question"]]["text"]}'] = answer
    session['current_question'] += 1
    
    if session['current_question'] >= len(QUESTIONS):
        return redirect(url_for('results'))
    
    return redirect(url_for('quiz'))

@app.route('/results')
def results():
    if 'answers' not in session or len(session['answers']) != len(QUESTIONS):
        return redirect(url_for('quiz'))
    
    try:
        # Make prediction using the trained model
        prediction = classifier.predict(session['answers'])
        
        # Get the predicted segment and probabilities
        primary_segment = prediction['prediction']
        probabilities = prediction['probabilities']
        
        # Get the second highest probability for secondary segment
        segments = ['Trendsetter', 'Budget Conscious', 'Luxury']
        sorted_probs = sorted(zip(segments, probabilities), key=lambda x: x[1], reverse=True)
        secondary_segment = sorted_probs[1][0]
        
        # Prepare data for the radar chart
        radar_data = {
            'labels': segments,
            'scores': probabilities
        }
        
        return render_template('results.html',
                             primary_segment=primary_segment,
                             secondary_segment=secondary_segment,
                             radar_data=radar_data)
                             
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        flash('An error occurred while processing your results. Please try again.')
        return redirect(url_for('quiz'))

if __name__ == '__main__':
    app.run(debug=True) 