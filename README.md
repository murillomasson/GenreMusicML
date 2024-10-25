# Music Genre Prediction with Machine Learning

A machine learning project that predicts music genres using audio features from tracks. It integrates with Spotify to manage track data, perform genre predictions, and store results in a database. This repository aims to enhance music recommendations and analyze musical trends through data insights.

## Project Overview

- **Language**: Python
- **Continuous Integration**: The CI environment is maintained in GitHub through the Actions tab. The process workflow is as follows:

  1. Push code to a feature development branch (`Proj-001`)
  2. Create a Pull Request (PR) to merge with the `dev` branch
  3. The pipeline recognizes the pull request and triggers the build of the environment and project
  4. Run automated tests using `pytest`
  5. Run static code analysis using `flake8`
  6. Logs of the success/fail of these automated actions are available for view in the GitHub Actions tab

## Features

- **Audio Data Collection:** Integrates with the Spotify API to gather audio features (like tempo, energy, and danceability) of tracks.
- **Genre Prediction:** Uses machine learning models (e.g., Random Forest) to predict the genre of music based on audio features.
- **Data Storage:** The track data and prediction results are stored in a relational database (PostgreSQL).
- **Continuous Integration:** Set up with GitHub Actions for automated testing, linting, and deployment.

## Setup Instructions
- Clone the repository:

```
git clone https://github.com/murillomasson/GenreMusicML.git
cd GenreMusicML
```
- Create a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```
- Install dependencies:
```
pip install -r requirements.txt
```

## Set up environment variables:
Create a .env file in the root directory with the following content:
```
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
POSTGRES_HOST
POSTGRES_PORT
SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET
```

## Run tests:
```
pytest
```

## Fork the repo
- Create a new branch (```git checkout -b feature-branch```)
- Commit your changes (```git commit -am 'Add some feature'```)
- Push to the branch (```git push origin feature-branch```)

## Future Work
To enhance the performance and capabilities of the GenreMusicML project, several key areas for future development are identified:

- **Establishing a Consistent Dataset:** Creating a more comprehensive and consistent dataset is crucial for training more robust models. This involves standardizing data collection methods, ensuring diverse genre representation, and incorporating various audio features. A well-structured dataset can significantly improve the model's ability to generalize and predict accurately across different genres.

- **Hyperparameter Optimization and Advanced Models:** Future work will focus on experimenting with better hyperparameters and optimizing the existing model. Leveraging advanced models, such as ensemble methods or deep learning architectures like Convolutional Neural Networks (CNNs), can lead to improved prediction accuracy. This includes fine-tuning hyperparameters using techniques such as Grid Search or Bayesian Optimization to find the optimal configurations.

- **Testing New Features for Predictions:** Exploring and integrating new audio features could enhance the predictive capabilities of the model. This may include extracting more nuanced characteristics from audio tracks, such as tempo variations, harmonic content, or key signatures, which can influence genre classification.

- **User Authentication:** Implementing user authentication will allow for personalized track predictions. By enabling users to create accounts and save their preferences, the application can provide tailored recommendations based on individual listening habits.

- **Deployment Strategies:** Deploying the application using Docker and Kubernetes will ensure scalability and reliability. This containerization approach simplifies the deployment process and facilitates better resource management, allowing the application to handle varying loads effectively.

- **Data Insights:** Conducting in-depth analyses to understand the relationship between different audio features and genre classification accuracy will be beneficial. Insights derived from such analyses can inform model improvements and guide future feature selection.
