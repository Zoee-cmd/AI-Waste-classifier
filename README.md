# 🌱 EcoSort - AI Waste Segregation Game (Django Version)

A gamified web application built with Django and TensorFlow that uses AI to help users learn proper waste segregation through image classification and interactive feedback.

## 🎯 Features

### Core Functionality
- **AI-Powered Image Classification**: Uses TensorFlow with MobileNetV2 model to classify waste items
- **Three Waste Categories**: Plastic, Paper, and Organic waste classification
- **Database Integration**: SQLite database for storing user scores and classification history
- **Admin Interface**: Django admin panel for managing data
- **Session Management**: Persistent user sessions and progress tracking

### Gamification Elements
- **Points System**: Earn points for providing feedback on AI predictions
- **Level Progression**: Level up based on your total score
- **Leaderboard**: Compare your performance with others
- **Classification History**: View your past classifications and feedback
- **Educational Tips**: Random tips about proper waste segregation

### User Experience
- **Drag & Drop Upload**: Easy image upload with visual feedback
- **Confidence Visualization**: Visual bars showing AI confidence levels
- **Feedback System**: Rate AI predictions to improve accuracy
- **Responsive Design**: Works on desktop and mobile devices
- **History Tracking**: View your classification history

## 🚀 Quick Start

### Local Development

1. **Clone the Repository**
   ```bash
   git clone <your-repository-url>
   cd django_app
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Application**
   ```bash
   python manage.py runserver
   ```

7. **Open in Browser**
   Navigate to `http://localhost:8000`

## 🛠️ Technical Implementation

### Backend (Django)
- **Django Framework**: Full-featured Python web framework
- **TensorFlow**: Server-side AI model processing
- **MobileNetV2**: Pre-trained image classification model
- **SQLite Database**: Local database for data persistence
- **Django Admin**: Built-in admin interface

### Models
- **UserScore**: Stores user scores and levels
- **ClassificationHistory**: Tracks classification results and feedback
- **LeaderboardEntry**: Manages leaderboard data

### Frontend
- **Django Templates**: Server-side rendering with template inheritance
- **CSS3**: Responsive design with animations
- **JavaScript**: Interactive functionality and API communication
- **Canvas API**: Image processing and conversion

### AI Model
```python
# MobileNetV2 pre-trained on ImageNet
model = tf.keras.applications.MobileNetV2(
    weights='imagenet',
    include_top=True,
    input_shape=(224, 224, 3)
)
```

## 📁 Project Structure

```
django_app/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── Procfile                 # Heroku deployment configuration
├── ecosort/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── waste_classifier/         # Django app
│   ├── __init__.py
│   ├── apps.py              # App configuration
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URL configuration
│   └── admin.py             # Admin interface
├── templates/               # Django templates
│   └── waste_classifier/
│       ├── index.html       # Main game page
│       └── history.html     # History page
├── static/                  # Static files
│   ├── css/
│   │   └── styles.css       # CSS styles
│   └── js/
│       └── script.js        # JavaScript functionality
├── media/                   # Uploaded files (auto-created)
└── db.sqlite3              # SQLite database (auto-created)
```

## 🌐 Deployment Options

### 1. Heroku (Recommended)
```bash
# Install Heroku CLI
heroku login
heroku create your-ecosort-django-app
git push heroku main
heroku open
```

### 2. PythonAnywhere
- Upload files to PythonAnywhere
- Install dependencies
- Configure WSGI file
- Set up web app

### 3. Railway
- Connect GitHub repository
- Automatic deployment
- Environment variable configuration

### 4. DigitalOcean App Platform
- Connect repository
- Choose Python runtime
- Automatic deployment

## 🎨 Design Features

### Visual Design
- **Green Theme**: Environmentally conscious color scheme
- **Gradient Backgrounds**: Modern visual appeal
- **Smooth Animations**: Enhanced user experience
- **Responsive Layout**: Works on all screen sizes

### UI Components
- **Score Cards**: Display current score and level
- **Leaderboard**: Show top performers
- **Upload Area**: Interactive file upload interface
- **Confidence Bars**: Visual representation of AI predictions
- **Category Cards**: Educational information about waste types
- **History Page**: View past classifications

## 🔧 Technical Requirements

### Server Requirements
- Python 3.8 or higher
- 2GB RAM minimum (for TensorFlow)
- 1GB disk space
- Internet connection (for model download)

### Browser Support
- Modern browsers with ES6+ support
- Canvas API support
- Local storage capability

### Dependencies
- Django 4.2.7
- TensorFlow 2.13.0
- Pillow 10.0.0
- NumPy 1.24.3
- Gunicorn 21.2.0
- WhiteNoise 6.6.0

## 🎯 MVP Approach Achieved

✅ **Pre-trained Model Integration**: Uses MobileNetV2 via TensorFlow  
✅ **2-3 Waste Categories**: Plastic, Paper, Organic classification  
✅ **Photo Upload & Prediction**: Complete server-side processing workflow  
✅ **Points System**: Gamified scoring with database storage  
✅ **Simple UI**: Clean, intuitive interface  
✅ **Django Backend**: Full-featured web framework implementation  
✅ **Database Integration**: SQLite for data persistence  
✅ **Admin Interface**: Built-in Django admin panel  

## 🚀 Future Enhancements

### Potential Improvements
- **Custom Model Training**: Train on specific waste datasets
- **More Categories**: Add metal, glass, electronic waste
- **User Authentication**: Django user accounts and profiles
- **Social Features**: Share achievements on social media
- **Offline Mode**: Cache model for offline use
- **Multi-language Support**: International accessibility
- **Advanced Analytics**: Detailed user progress tracking
- **API Endpoints**: REST API for mobile apps

### Technical Enhancements
- **PostgreSQL**: Production database
- **Redis**: Caching and session storage
- **Celery**: Background task processing
- **Docker**: Containerized deployment
- **CDN**: Static file delivery
- **Monitoring**: Application performance monitoring

## 🌍 Environmental Impact

This application promotes:
- **Waste Education**: Learn proper segregation practices
- **Behavioral Change**: Gamification encourages participation
- **Environmental Awareness**: Visual feedback on waste types
- **Community Engagement**: Leaderboard fosters competition
- **Data Collection**: Track user behavior for improvement

## 📱 Usage Instructions

1. **Start the App**: Run `python manage.py runserver`
2. **Wait for Model**: AI model loads automatically (first time may take 10-15 seconds)
3. **Upload Image**: Click upload area or drag image file
4. **Analyze**: Click "Analyze Waste" button
5. **Review**: Check confidence percentages for each category
6. **Feedback**: Rate the prediction accuracy
7. **Progress**: Watch your score and level increase
8. **History**: View your classification history

## 🎮 Gamification Elements

- **Points**: Earn points for every interaction
- **Levels**: Progress through levels based on score
- **Leaderboard**: Compare with other users
- **History**: Track your classification history
- **Tips**: Educational content about waste segregation
- **Visual Feedback**: Immediate response to user actions

## 🔒 Privacy & Data

- **Server-side Processing**: AI model runs on server
- **Database Storage**: User data stored in SQLite database
- **Session Management**: Django session framework
- **Admin Access**: Secure admin interface
- **File Uploads**: Secure file handling with validation

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Slow**
   - First run downloads model (~14MB)
   - Ensure stable internet connection
   - Check available disk space

2. **Database Issues**
   - Run migrations: `python manage.py migrate`
   - Check database permissions
   - Verify SQLite file exists

3. **Static Files Not Loading**
   - Run: `python manage.py collectstatic`
   - Check STATIC_ROOT setting
   - Verify file permissions

4. **Upload Errors**
   - Check file format (JPG, PNG, WebP)
   - Ensure file size < 16MB
   - Verify media directory exists

## 📊 Performance

### Optimization Tips
- **Image Compression**: Reduce quality to 0.8 for faster uploads
- **Model Caching**: Model loads once and stays in memory
- **Database Indexing**: Optimize database queries
- **Static Files**: Use CDN for static assets in production
- **Caching**: Implement Redis for session storage

### Benchmarks
- **Model Load Time**: ~10-15 seconds (first run)
- **Image Processing**: ~2-5 seconds per image
- **Response Time**: < 1 second for API calls
- **Memory Usage**: ~500MB with model loaded

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ for a greener future! 🌱**

*Deploy your own instance and help make the world a cleaner place!* 