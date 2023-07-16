# django-testing

# My Study Platform

My Study Platform is a web application that allows users to search for YouTube videos and create their own video playlists. Users can register, search for videos, add videos to their playlist, and view their saved videos.

## Features

- User Registration: Users can create an account to access the platform.
- Video Search: Users can search for YouTube videos using keywords.
- Video Playlist: Users can add videos to their personal playlist.
- My Videos: Users can view the videos they have added to their playlist.

## Technologies Used

- Django: Web framework used to build the application.
- Python: Programming language used for the backend development.
- YouTube Data API: Integration with the API to fetch video information.
- HTML/CSS: Frontend markup and styling.
- SQLite: Database for storing user information and video data.

## Getting Started

To run this project locally, follow these steps:

1. Clone the repository: `git clone <repository-url>`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Set up the database: `python manage.py migrate`
4. Set up the YouTube API: Obtain an API key and update the `YOUTUBE_API_KEY` setting in `settings.py` file.
5. Start the development server: `python manage.py runserver`
6. Access the application in your browser at `http://localhost:8000`

## Configuration

The following configurations can be modified in the `settings.py` file:

- `YOUTUBE_API_KEY`: Your YouTube Data API key.

## Contributing

Contributions to this project are welcome! If you find any bugs or have suggestions for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
