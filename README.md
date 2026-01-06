Hat Checker
A computer vision application that analyzes how well a hat fits you using AI. Runs entirely on your local machine with no API keys or cloud services required.
What It Does
This tool uses your webcam to capture photos of you wearing a hat, then analyzes the fit using the LLaVA vision model running through Ollama. You'll get feedback on face shape compatibility, proportions, style matching, positioning, and color coordination, along with a numerical rating and suggestions for improvement.
Requirements
Before running this application, you need:

Python 3.7 or higher
A working webcam
Ollama installed on your system
The LLaVA model downloaded through Ollama

The script will automatically install the requests library if you don't have it.
Installation
First, install Ollama if you haven't already. Download it from https://ollama.ai/download and follow the installation instructions for your operating system.
Once Ollama is installed, pull the LLaVA model by running this command in your terminal:
bashollama pull llava
This downloads the vision model to your computer. The download is around 4-5GB, so it may take a few minutes depending on your internet connection.
After the model is downloaded, make sure Ollama is running. It typically starts automatically after installation, but you can verify by checking if port 11434 is accessible.
Usage
Run the application with:
bashpython hat_checker.py
The application will guide you through these steps:

Position yourself in front of your webcam wearing the hat
Press SPACE to capture the front view (or ESC to cancel)
Optionally capture a back view for more complete analysis
Wait while the AI analyzes your images (typically 10-30 seconds)
Review the detailed feedback and rating
Save the analysis to a text file if desired

You can analyze multiple hats in the same session by choosing to continue when prompted.
How the Analysis Works
The application evaluates five main aspects:

Face Shape Compatibility: Whether the hat style complements your facial structure
Proportions: If the hat size is appropriate for your head and body
Style Match: How well the hat suits your overall appearance
Fit and Positioning: Whether the hat is worn correctly
Color Coordination: How the hat color works with your complexion and clothing

Results include an overall rating out of 10, detailed feedback explaining what works or doesn't, and specific suggestions for improvement or alternative styles.
Performance Notes
Analysis speed depends on your hardware. Systems with dedicated GPUs will process images faster than CPU-only systems. The first analysis after starting Ollama may take longer as the model loads into memory.
If analysis takes too long or times out, try capturing smaller images by sitting further from the webcam or reducing your webcam resolution in your system settings.
Troubleshooting
"Ollama is not running" error
Make sure Ollama is installed and running. You can test by opening http://localhost:11434/api/tags in your web browser. If it doesn't load, restart Ollama or check your installation.
"Could not open webcam" error
Verify your webcam is connected and working. Check that no other applications are using the webcam. On some systems, you may need to grant camera permissions to Python or your terminal application.
Analysis timing out
The LLaVA model is computationally intensive. If you consistently get timeouts, ensure no other heavy applications are running, or consider using a more powerful computer. You can also try reducing image quality by adjusting webcam settings.
Model not found
If you get errors about the model not being available, run ollama pull llava again to ensure the model is properly downloaded.
Privacy
All processing happens on your local machine. No images or data are sent to any external servers. Your photos are only stored temporarily in memory during analysis and can optionally be saved to your local disk if you choose.
Technical Details
Built with Python using OpenCV for webcam capture, PIL for image processing, and Ollama's API for running the LLaVA vision model locally. The application communicates with Ollama through HTTP requests on localhost port 11434.
