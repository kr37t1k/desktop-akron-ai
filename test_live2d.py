#!/usr/bin/env python3
"""
Test script to verify Live2D integration
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'AkronNova'))

from AkronNova.src.live2d_handler import Live2DModel

def test_live2d_model():
    print("Testing Live2D model loading...")
    
    try:
        # Load the 香風智乃 model
        model = Live2DModel("香風智乃", "AkronNova/model_dict.json")
        print(f"✓ Successfully loaded model: {model.live2d_model_name}")
        print(f"✓ Model info: {model.model_info}")
        print(f"✓ Available emotions: {model.emo_map}")
        
        # Test emotion extraction
        test_text = "Hello there! [joy] I'm so happy to see you! [surprise] Oh my, what a surprise! [anger] Let's have a cute conversation."
        emotions = model.extract_emotion(test_text)
        clean_text = model.remove_emotion_keywords(test_text)
        
        print(f"✓ Extracted emotions: {emotions}")
        print(f"✓ Cleaned text: {clean_text}")
        
        return True
    except Exception as e:
        print(f"✗ Error loading Live2D model: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_live2d_model()
    if success:
        print("\n✓ Live2D model integration test passed!")
    else:
        print("\n✗ Live2D model integration test failed!")
        sys.exit(1)