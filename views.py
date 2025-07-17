import json
import base64
import io
import numpy as np
from PIL import Image
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserScore, ClassificationHistory, LeaderboardEntry
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Global model variable
model = None

def preprocess_image(image_data):
    """Preprocess image for model input"""
    try:
        # Convert base64 to PIL Image
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Resize to model input size
        image = image.resize((224, 224))
        
        # Convert to array and preprocess
        image_array = np.array(image)
        
        # Ensure 3 channels (RGB)
        if len(image_array.shape) == 2:  # Grayscale
            image_array = np.stack([image_array] * 3, axis=-1)
        elif image_array.shape[2] == 4:  # RGBA
            image_array = image_array[:, :, :3]
        
        # Preprocess for MobileNetV2
        image_array = tf.keras.applications.mobilenet_v2.preprocess_input(image_array)
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        return None

def classify_waste(predictions):
    """Map ImageNet predictions to waste categories"""
    # Keywords for each waste category
    waste_keywords = {
        'plastic': [
            'bottle', 'container', 'plastic', 'bag', 'wrapper', 'packaging',
            'cup', 'straw', 'bottle', 'can', 'jar', 'lid', 'cap'
        ],
        'paper': [
            'paper', 'cardboard', 'newspaper', 'magazine', 'book', 'box',
            'envelope', 'folder', 'notebook', 'calendar', 'poster'
        ],
        'organic': [
            'food', 'fruit', 'vegetable', 'apple', 'banana', 'bread', 'leaf',
            'plant', 'flower', 'tomato', 'orange', 'carrot', 'lettuce'
        ]
    }
    
    # Get top predictions
    top_indices = np.argsort(predictions[0])[-5:][::-1]
    
    scores = {'plastic': 0, 'paper': 0, 'organic': 0}
    
    for idx in top_indices:
        confidence = float(predictions[0][idx])
        
        # Map ImageNet class to waste category
        for category, keywords in waste_keywords.items():
            if any(keyword in str(idx).lower() for keyword in keywords):
                scores[category] += confidence
    
    # Normalize scores
    total = sum(scores.values())
    if total == 0:
        # Default distribution if no matches
        scores = {'plastic': 33, 'paper': 33, 'organic': 34}
    else:
        scores = {k: round((v / total) * 100) for k, v in scores.items()}
    
    return scores

def index(request):
    """Main application page"""
    # Removed model loading logic (no longer needed)
    # Get or create user score
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    
    user_score, created = UserScore.objects.get_or_create(
        session_id=session_id,
        defaults={'score': 0, 'level': 1}
    )
    
    # Get leaderboard
    leaderboard = LeaderboardEntry.objects.all()[:10]
    
    context = {
        'user_score': user_score,
        'leaderboard': leaderboard,
    }
    
    return render(request, 'waste_classifier/index.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def upload_image(request):
    """Handle image upload and classification (now deprecated, returns error)"""
    return JsonResponse({'error': 'Server-side classification is disabled. Use client-side AI.'}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def save_score(request):
    """Save user score"""
    try:
        data = json.loads(request.body)
        score = data.get('score', 0)
        level = data.get('level', 1)
        feedback = data.get('feedback')  # True for correct, False for wrong
        
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        
        # Update or create user score
        user_score, created = UserScore.objects.get_or_create(
            session_id=session_id,
            defaults={'score': score, 'level': level}
        )
        
        if not created:
            user_score.score = score
            user_score.level = level
            user_score.save()
        
        # Update latest classification with feedback
        if feedback is not None:
            latest_classification = ClassificationHistory.objects.filter(
                session_id=session_id
            ).order_by('-created_at').first()
            
            if latest_classification:
                latest_classification.user_feedback = feedback
                latest_classification.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Score saved successfully'
        })
        
    except Exception as e:
        logger.error(f"Error saving score: {e}")
        return JsonResponse({'error': 'Error saving score'}, status=500)

@require_http_methods(["GET"])
def leaderboard(request):
    """Get leaderboard data"""
    try:
        leaderboard_entries = LeaderboardEntry.objects.all()[:10]
        data = []
        
        for entry in leaderboard_entries:
            data.append({
                'name': entry.name,
                'score': entry.score,
                'level': entry.level
            })
        
        return JsonResponse({
            'success': True,
            'leaderboard': data
        })
        
    except Exception as e:
        logger.error(f"Error getting leaderboard: {e}")
        return JsonResponse({'error': 'Error getting leaderboard'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def add_leaderboard_entry(request):
    """Add entry to leaderboard"""
    try:
        data = json.loads(request.body)
        name = data.get('name', 'Anonymous')
        score = data.get('score', 0)
        level = data.get('level', 1)
        
        LeaderboardEntry.objects.create(
            name=name,
            score=score,
            level=level
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Leaderboard entry added successfully'
        })
        
    except Exception as e:
        logger.error(f"Error adding leaderboard entry: {e}")
        return JsonResponse({'error': 'Error adding leaderboard entry'}, status=500)

def history(request):
    """Show classification history"""
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    
    classifications = ClassificationHistory.objects.filter(
        session_id=session_id
    ).order_by('-created_at')[:20]
    
    context = {
        'classifications': classifications
    }
    
    return render(request, 'waste_classifier/history.html', context)

@require_http_methods(["GET"])
def get_recycling_info(request):
    """Get detailed recycling information for waste categories"""
    category = request.GET.get('category', '').lower()
    
    recycling_data = {
        'plastic': {
            'title': '♻️ Plastic Recycling Guide',
            'description': 'Plastic waste can be recycled into new products, reducing environmental impact.',
            'steps': [
                'Clean and rinse plastic items thoroughly',
                'Remove caps and labels when possible',
                'Check local recycling guidelines for accepted plastics',
                'Separate by type (PET, HDPE, PVC, etc.)',
                'Flatten containers to save space'
            ],
            'examples': [
                'Water bottles → New bottles, clothing fibers',
                'Milk jugs → Garden furniture, toys',
                'Food containers → Storage bins, planters',
                'Plastic bags → Composite lumber, new bags'
            ],
            'tips': [
                'Look for the recycling symbol (♻️) on plastic items',
                'Not all plastics are recyclable - check with your local facility',
                'Clean plastics are more valuable for recycling',
                'Consider reusing before recycling'
            ],
            'images': [
                {
                    'url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=200&fit=crop',
                    'explanation': 'Plastic bottles are collected, cleaned, and processed into new bottles or textile fibers.'
                },
                {
                    'url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=200&fit=crop',
                    'explanation': 'Plastic containers are sorted and recycled into items like garden furniture or toys.'
                },
                {
                    'url': 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=300&h=200&fit=crop',
                    'explanation': 'Plastic bags are collected and processed into composite lumber or new bags.'
                }
            ]
        },
        'paper': {
            'title': '📄 Paper Recycling Guide',
            'description': 'Paper and cardboard are among the most recyclable materials.',
            'steps': [
                'Remove any plastic or metal attachments',
                'Keep paper dry and clean',
                'Separate by type (newspaper, cardboard, office paper)',
                'Flatten cardboard boxes',
                'Remove any food residue or grease'
            ],
            'examples': [
                'Newspapers → New paper products, insulation',
                'Cardboard boxes → New boxes, packaging materials',
                'Office paper → New paper, tissue products',
                'Magazines → New paper products, animal bedding'
            ],
            'tips': [
                'Shredded paper can be recycled but may need special handling',
                'Waxed or coated paper may not be recyclable',
                'Paper with food residue should be composted instead',
                'Recycle paper within 6 months for best quality'
            ],
            'images': [
                {
                    'url': 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=300&h=200&fit=crop',
                    'explanation': 'Cardboard and paper are sorted, shredded, and made into new paper products.'
                },
                {
                    'url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=200&fit=crop',
                    'explanation': 'Clean paper is pulped and recycled into tissue or new paper.'
                },
                {
                    'url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=200&fit=crop',
                    'explanation': 'Magazines and newspapers are processed into insulation or animal bedding.'
                }
            ]
        },
        'organic': {
            'title': '🍎 Organic Waste Composting Guide',
            'description': 'Organic waste can be composted to create nutrient-rich soil.',
            'steps': [
                'Collect organic waste in a compost bin',
                'Mix green (nitrogen-rich) and brown (carbon-rich) materials',
                'Keep compost moist but not wet',
                'Turn compost regularly for aeration',
                'Wait 2-6 months for decomposition'
            ],
            'examples': [
                'Fruit peels → Rich compost for gardens',
                'Vegetable scraps → Nutrient-rich soil amendment',
                'Coffee grounds → Natural fertilizer',
                'Leaves and grass → Mulch and soil conditioner'
            ],
            'tips': [
                'Avoid meat, dairy, and oily foods in home composting',
                'Chop materials into smaller pieces for faster decomposition',
                'Maintain a 2:1 ratio of brown to green materials',
                'Compost can be used in gardens, potted plants, and landscaping'
            ],
            'images': [
                {
                    'url': 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=300&h=200&fit=crop',
                    'explanation': 'Organic waste is collected and composted to create nutrient-rich soil.'
                },
                {
                    'url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=200&fit=crop',
                    'explanation': 'Compost piles are turned regularly to speed up decomposition.'
                },
                {
                    'url': 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=300&h=200&fit=crop',
                    'explanation': 'Finished compost is used to enrich gardens and landscapes.'
                }
            ]
        }
    }
    
    if category in recycling_data:
        return JsonResponse({
            'success': True,
            'data': recycling_data[category]
        })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Category not found'
        }, status=404) 