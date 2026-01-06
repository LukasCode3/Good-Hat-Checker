"""
Hat Checker Application - Uses LOCAL Ollama with LLaVA
100% FREE - No API key needed! Runs on your computer!
"""

import cv2
import os
from PIL import Image
import io
import time
import base64
import json

try:
    import requests
except ImportError:
    print("Installing required package: requests")
    os.system("pip install requests")
    import requests


class HatCheckerOllama:
    def __init__(self):
        """
        Initialize Hat Checker with local Ollama
        No API key needed - completely free!
        """
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "llava:latest"  # Free vision model
        
        # Check if Ollama is running
        if not self.check_ollama():
            raise Exception(
                "Ollama is not running!\n"
                "Please install and start Ollama:\n"
                "1. Download from: https://ollama.ai/download\n"
                "2. Install Ollama\n"
                "3. Run: ollama pull llava\n"
                "4. Ollama will start automatically"
            )
        
        print("✓ Ollama connected successfully!")
        print("✓ Using model: llava (100% FREE - runs locally!)")
    
    def check_ollama(self):
        """Check if Ollama is running"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def capture_image_from_webcam(self, window_name="Hat Checker"):
        """
        Capture image from webcam with live preview
        Press SPACE to capture, ESC to exit
        """
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            raise Exception("Could not open webcam")
        
        print(f"\n📸 {window_name}")
        print("   Press SPACE to capture")
        print("   Press ESC to exit")
        
        captured_frame = None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            display_frame = frame.copy()
            cv2.putText(display_frame, "Press SPACE to capture, ESC to exit", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow(window_name, display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == 32:  # SPACE key
                captured_frame = frame
                print("   ✓ Image captured!")
                break
            elif key == 27:  # ESC key
                print("   ✗ Capture cancelled")
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if captured_frame is not None:
            frame_rgb = cv2.cvtColor(captured_frame, cv2.COLOR_BGR2RGB)
            return Image.fromarray(frame_rgb)
        
        return None
    
    def image_to_base64(self, image):
        """Convert PIL Image to base64"""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    def analyze_hat_fit(self, front_image, back_image=None):
        """
        Analyze hat fit using local Ollama LLaVA model
        """
        print("\n🤔 Analyzing hat fit with AI (running locally)...")
        print("   (This may take 10-30 seconds depending on your computer)")
        
        prompt = """You are a professional fashion stylist and hat fitting expert. 
Analyze whether this hat looks good on this person.

Please evaluate:
1. Face Shape Compatibility: Does the hat shape complement their face shape?
2. Proportions: Is the hat size appropriate for their head and body?
3. Style Match: Does the hat style suit their overall appearance?
4. Fit & Positioning: Is the hat positioned correctly and fitting well?
5. Color Coordination: If visible, how well does the color work?

Provide:
- Overall Rating: X/10
- Detailed Feedback: Explain what works and what doesn't
- Suggestions: How to improve or what alternative hat styles might work better

Be honest but constructive in your feedback."""
        
        if back_image:
            prompt += "\n\nNote: You're seeing both front and back views for a complete assessment."
        
        try:
            # Convert image to base64
            front_b64 = self.image_to_base64(front_image)
            
            # Prepare request
            data = {
                "model": self.model,
                "prompt": prompt,
                "images": [front_b64],
                "stream": False
            }
            
            # If back image provided, analyze separately and combine
            if back_image:
                back_b64 = self.image_to_base64(back_image)
                data["images"].append(back_b64)
            
            # Make request to Ollama
            response = requests.post(self.ollama_url, json=data, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response received')
            else:
                return f"Error: Received status code {response.status_code}"
        
        except requests.exceptions.Timeout:
            return "⚠️ Request timed out. The model might be taking too long. Try again or use a smaller image."
        except Exception as e:
            return f"Error during analysis: {str(e)}"
    
    def run_interactive_session(self):
        """
        Run interactive hat checking session
        """
        print("\n" + "="*60)
        print("🎩 HAT CHECKER - AI-Powered Hat Fit Analysis")
        print("="*60)
        print("\nThis app runs 100% locally on your computer!")
        print("No API keys, no cloud, completely FREE!\n")
        
        # Capture front view
        print("\n[Step 1] Let's capture the FRONT view")
        print("         Position yourself facing the camera with the hat on")
        front_img = self.capture_image_from_webcam("FRONT VIEW - Press SPACE to capture")
        
        if front_img is None:
            print("\n❌ Session cancelled.")
            return
        
        # Ask if user wants back view
        print("\n[Step 2] Do you want to capture a BACK view? (recommended)")
        choice = input("         Enter 'y' for yes, any other key to skip: ").strip().lower()
        
        back_img = None
        if choice == 'y':
            print("\n         Great! Please turn around and face away from camera")
            input("         Press ENTER when ready...")
            back_img = self.capture_image_from_webcam("BACK VIEW - Press SPACE to capture")
        
        # Analyze
        result = self.analyze_hat_fit(front_img, back_img)
        
        # Display results
        print("\n" + "="*60)
        print("📊 HAT FIT ANALYSIS RESULTS")
        print("="*60)
        print(result)
        print("="*60)
        
        # Save option
        save = input("\nWould you like to save the analysis to a file? (y/n): ").strip().lower()
        if save == 'y':
            filename = f"hat_analysis_{int(time.time())}.txt"
            with open(filename, 'w') as f:
                f.write("HAT FIT ANALYSIS\n")
                f.write("="*60 + "\n")
                f.write(result)
            print(f"✓ Analysis saved to: {filename}")
        
        # Another check?
        again = input("\nWant to check another hat? (y/n): ").strip().lower()
        if again == 'y':
            self.run_interactive_session()


def main():
    """Main entry point"""
    print("\n🎩 Welcome to Hat Checker (Ollama Edition)!")
    print("\n" + "="*60)
    print("100% FREE - Runs completely on your computer!")
    print("="*60)
    print("\nSetup Instructions:")
    print("1. Install Ollama from: https://ollama.ai/download")
    print("2. Run: ollama pull llava")
    print("3. Run this script!")
    print("\nOllama will use your CPU/GPU to run the AI model locally.")
    print("No internet required after initial model download!\n")
    
    try:
        # Initialize checker
        checker = HatCheckerOllama()
        
        # Run interactive session
        checker.run_interactive_session()
        
        print("\n👋 Thanks for using Hat Checker!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is installed and running")
        print("2. Run: ollama pull llava")
        print("3. Check that port 11434 is not blocked")
        print("4. Verify your webcam is working")


if __name__ == "__main__":
    main()