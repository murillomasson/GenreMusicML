# GenreMusicML
A machine learning project that predicts music genres using audio features from tracks. It integrates with Spotify to manage track data, perform genre predictions, and store results in a database. This repository aims to enhance music recommendations and analyze musical trends through data insights.


The language used is python. The CI environment is maintained in GitHub through the Actions tab, the process goes like:
1. Push code to feature development branch Proj-001
2. Pull Request to merge with dev branch
3. Pipeline recognizes pull request and triggers build of environment and project
4. Trigger run of automated tests through pytest
5. Trigger static code analysis tool, flake8
6. Logs of success/fail of automated actions available for view in Github Actions tab
