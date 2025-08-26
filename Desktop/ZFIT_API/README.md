# ZFIT-API: Automated Workout Planning with Actionable Insights


## Problem Statement


I use **ZFIT**, a mobile app I designed and developed, to create workouts, log exercises, and track progress via data visualizations. However, each workout and exercise must be entered manually, and the visualizations only graph raw data without actionable insights. As a result, planning and logging workouts can take a long time, and the lack of meaningful feedback makes it hard to optimize training effectively.

## Tech Stack


| Layer      | Technologies |
|------------|--------------|
| **Backend**   | Python, Pandas Library|
| **AI**   | Ollama, LLaMA3 |
| **Database**   | Postgres via Supabase|
| **Development Tools**     | VSCode, GitHub|


## Core Features


- **Automated Workout Planning**: To generate a customized plan, the app first gathers user data through a four-part assessment, including age, gender, experience level, goals, availability, and accessible equipment. I formulated an input query for the LLaMA 3 model to generate a workout plan based on this data. The weight and reps for each exercise are determined from the user’s past performance. For exercises the user has never performed, the LLM identifies the most similar exercise previously completed and applies its weight and reps. The generated workout plan is sent to the frontend, where users can review and use AI to modify it. Once saved, the workouts are stored and ready for use.
- **Actionable Exercise Insights**: Users can generate insights for exercises they’ve completed. Using historical data, the LLM analyzes trends in weight and reps, recommends optimal weights and reps for the next session, and provides guidance on how to progress. This feature gives users personalized, actionable advice to improve their training.

## How to Run
## 1. Install Dependencies
Ensure you have Python installed. Then, install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt 
```
## 2. Run the backend server using app.py
## 3. Follow the instructions in the ZFIT GitHub to launch the React Native app
## 4. Log In

Use the following test credentials to sign in:

Email: andrew866799@gmail.com

Password: Test123

##5. Test Features

Create Tab: Generate a customized workout plan.

Progress Tab: Generate actionable insights based on past exercises.

##6. Notes

Generating a program, making changes to a program, or generating insights may take up to one minute to complete.

Ensure both the backend and front end is running.

If using a mobile device with Expo Go, make sure it is on the same Wi-Fi network as your computer.

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