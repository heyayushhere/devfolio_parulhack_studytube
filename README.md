# 📘 My Study Platform

My Study Platform is a web application that allows users to search for YouTube videos and create their own video playlists. Users can register, search for videos, add videos to their playlist, view their saved videos, create tasks 📝, and manage their tasks ✅. They can also search for YouTube channels by name and display all the videos from a specific channel.

## ✨ Features

- User Registration 🙋‍♂️🙋‍♀️: Users can create an account to access the platform.
- Video Search 🔍: Users can search for YouTube videos using keywords.
- Video Playlist 🎥📚: Users can add videos to their personal playlist.
- My Videos 📺: Users can view the videos they have added to their playlist.
- Task Creation 📝: Users can create tasks to manage their study schedule.
- Task Management ✅: Users can view all their tasks and mark them as completed.
- YouTube Channel Search 🔍📺: Users can search for YouTube channels by name.
- Channel Videos 📺: Users can display all the videos from a specific YouTube channel.

## 🛠️ Technologies Used

- Django: Web framework used to build the application.
- Python: Programming language used for the backend development.
- YouTube Data API: Integration with the API to fetch video and channel information.
- HTML/CSS: Frontend markup and styling.
- SQLite: Database for storing user information, video data, and tasks.

## 🚀 Getting Started

To run this project locally, follow these steps:

1. Clone the repository: `git clone <repository-url>`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Set up the database: `python manage.py migrate`
4. Set up the YouTube API: Obtain an API key and update the `YOUTUBE_API_KEY` setting in the `settings.py` file.
5. Start the development server: `python manage.py runserver`
6. Access the application in your browser at `http://localhost:8000`

## ⚙️ Configuration

The following configurations can be modified in the `settings.py` file:

- `YOUTUBE_API_KEY`: Your YouTube Data API key.

## 🤝 Contributing

Contributions to this project are welcome! If you find any bugs or have suggestions for improvement, please open an issue or submit a pull request.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
