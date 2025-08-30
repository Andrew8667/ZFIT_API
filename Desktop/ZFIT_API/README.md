# ZFIT-API: AI Automated Workout Plans & Insights


## Introduction/Summary


I use **ZFIT**, a mobile app I designed and developed, to create workouts, log exercises, and track progress via data visualizations. However, each workout and exercise must be entered manually, and the visualizations only graph raw data without actionable insights. As a result, planning and logging workouts can take a long time, and the lack of meaningful feedback makes it hard to optimize training effectively.

## Demo


[Click here to watch the demo](https://youtu.be/98nS1DF1aLU) 
*(A video demonstrating the AI automated features using ZFIT_API with ZFIT)*

## Tech Stack used for API


| Layer      | Technologies |
|------------|--------------|
| **Backend**   | Python, Pandas Library|
| **AI**   | Ollama, LLaMA3 |
| **Database**   | Postgres via Supabase|
| **Development Tools**     | VSCode, GitHub|


## Core Features


- **Automated Workout Planning**: To generate a customized plan, the app first gathers user data through a four-part assessment, including age, gender, experience level, goals, availability, and accessible equipment. I formulated an input query for the LLaMA 3 model to generate a workout plan based on this data. The weight and reps for each exercise are determined from the user’s past performance. For exercises the user has never performed, the LLM identifies the most similar exercise previously completed and applies its weight and reps. The generated workout plan is sent to the frontend, where users can review and use AI to modify it. Once saved, the workouts are stored and ready for use.
- **Actionable Exercise Insights**: Users can generate insights for exercises they’ve completed. Using historical data, the LLM analyzes trends in weight and reps, recommends optimal weights and reps for the next session, and provides guidance on how to progress. This feature gives users personalized, actionable advice to improve their training.

## How to Run the App


Required Technologies
- Node.js
- Xcode (for iOS simulator)
- Python
- Visual Studio Code

Step 1: Set Up the Backend (ZFIT_API)
1. Download and unzip ZFIT_API from this repository
2. Run ZFIT_API folder in Visual Studio Code
3. From the ZFIT_API directory, install Python dependencies by running: pip3(or pip) install -r requirements.txt
4. Start the backend server: python3(or python) app.py

Note: Keep this terminal open while using the mobile app

Step 2: Set Up the Front End (ZFIT)
1. Find my GitHub repository called ZFIT 
2. Download and unzip ZFIT from this repository
3. Open the folder ZFIT in Visual Studio Code.
4. From the ZFIT directory, install Node dependencies by running: npm install
5. Verify that Expo CLI is installed: expo --version. If no version appears, install Expo CLI globally: npm install -g expo-cli
6. Start the Expo project: Type and enter ‘expo start’ in the terminal
7. Launch the iOS simulator: Press i in the terminal to open the iPhone 16 simulator (ensure Xcode is installed). You may need to navigate to the Expo Go app in the simulator and manually enter url from the terminal that starts with ‘exp://’
Important: Both the backend (ZFIT_API) and the front end (ZFIT) must be running simultaneously.

Step 3: Using the App
1. Open the mobile app and log in with the following credentials:
- Email: Andrew866799@gmail.com
- Password: Test123

Create Tab: Test the AI-powered workout planner by clicking the Program button.

Progress Tab: Generate insights on completed exercises.

Note: Generating a new workout program from the assessment, making changes to the plan, or
generating insights may take up to one minute.

## Challenges & Learnings


- One challenge was working with Ollama, LLaMA 3, and Flask, technologies I had little prior experience with. Through research and experimentation, I learned to build Flask endpoints and integrate the LLaMA 3 model, successfully enabling communication between the mobile app and Python backend.
- Writing prompts for the LLM was a challenge, as initial outputs were often inaccurate. Through careful experimentation, I discovered that providing highly detailed instructions, which included specifying exactly what the output should and should not contain, significantly improved the model’s accuracy.
- A challenge was integrating the frontend, backend, and database technologies into a cohesive system. I overcame this by mapping out a detailed data flow and creating a clear implementation plan. As a result, all components now communicate seamlessly.

## Future Improvements


- Use a cloud-hosted LLM, such as OpenAI, to achieve faster and more accurate responses.
- Expand the user assessment with additional questions to generate even more personalized workout plans.

## Contact


- Email: [Andrew866799@gmail.com](mailto:Andrew866799@gmail.com) 
- LinkedIn: [linkedin.com/in/andrewkgee](https://www.linkedin.com/in/andrewkgee)