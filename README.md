# 🤖 AI Chat Assistant

A beautiful, responsive Streamlit frontend for your Groq AI-powered chat application.

## ✨ Features

- **Modern UI Design**: Beautiful gradient design with responsive layout
- **Real-time Chat**: Interactive chat interface with message history
- **Model Selection**: Choose between different Groq LLaMA models
- **Temperature Control**: Adjust response creativity with temperature slider
- **Session Management**: Chat history persists during your session
- **Error Handling**: Robust error handling with user-friendly messages
- **Mobile Responsive**: Optimized for both desktop and mobile devices

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**:
   Create a `.env` file in the project root and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Run the Application**:
   ```bash
   streamlit run main.py
   ```

4. **Open in Browser**:
   The app will automatically open at `http://localhost:8501`

## 🎨 Design Features

- **Gradient Headers**: Beautiful purple-blue gradient header
- **Chat Bubbles**: Distinct styling for user and AI messages
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Adapts to different screen sizes
- **Modern Typography**: Clean, readable fonts
- **Loading States**: Visual feedback during AI processing

## ⚙️ Configuration

- **Models Available**: 
  - LLaMA 3.3 70B Versatile (default)
  - LLaMA 3.1 8B Instant
  - LLaMA 3.1 70B Versatile
- **Temperature Range**: 0.0 (deterministic) to 1.0 (creative)

## 📱 Mobile Support

The interface is fully responsive and optimized for mobile devices with:
- Touch-friendly input areas
- Adjusted message margins for smaller screens
- Responsive header sizing

Enjoy chatting with your AI assistant! 🎉
