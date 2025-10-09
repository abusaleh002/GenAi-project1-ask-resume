


#!/bin/bash
echo "------------------------------------"
echo "🚀 Setting up your Python environment..."
echo "------------------------------------"

# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
source .venv/Scripts/activate

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Fix FAISS version if needed
if grep -q "faiss-cpu==1.8.0.post1" requirements.txt; then
  echo "⚙️  Fixing FAISS version for Windows..."
  sed -i 's/faiss-cpu==1.8.0.post1/faiss-cpu==1.7.4/' requirements.txt
fi

# 5. Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# 6. Run Streamlit app
echo "🌐 Starting Streamlit app..."
streamlit run app.py


# 1. ▶️ How to Run It

#Open VS Code terminal (Ctrl + `).

# 2. Make sure you’re in your project folder:

# Example:  D:\Machine Learning(AI)\GenAI\genai-project1-ask-my-resume

# 3. Run the script:
# bash setup_and_run.sh

# 4. It’ll:

# Create .venv

#Activate it

# Install all dependencies

# Fix FAISS for Windows

# Launch your Streamlit app automatically 🎉