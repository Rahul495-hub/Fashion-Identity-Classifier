# Fashion Identity Finder

A Flask web application that helps users discover their fashion identity through a simple 5-question quiz. The app categorizes users into one of five fashion identities: Classic Elegance, Bohemian Spirit, Minimalist Modern, Trendy Fashion-Forward, or Athleisure Enthusiast.

## Features

- Interactive 5-question quiz to determine fashion identity
- Detailed profile results with personalized recommendations
- Visual representation of style preferences using radar charts
- Responsive design that works on desktop and mobile devices
- Specific product recommendations based on fashion identity

## Installation

1. Clone this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to http://127.0.0.1:5000/
3. Complete the 5-question quiz to discover your fashion identity
4. Explore your personalized fashion profile and recommendations

## Project Structure

- `app.py` - The main Flask application
- `templates/` - HTML templates
  - `index.html` - Landing page
  - `question.html` - Quiz question template
  - `results.html` - Results page showing fashion identity

## How It Works

The application uses a scoring system based on user responses to determine which fashion identity best matches their preferences. Each answer contributes points to different style categories, and the cumulative scores reveal the user's primary fashion identity along with secondary influences.

## Customization

You can easily customize this application by:
- Adding more fashion identities to the `FASHION_IDENTITIES` list in `app.py`
- Modifying or adding questions in the `QUESTIONS` list
- Adjusting the scoring algorithm to refine the classification
- Adding images and product recommendations 