# Weekly CFB
Weekly CFB is a website that ranks the top college football games of the week by how entertaining they are to watch using statistical analysis.

# Motivation

We know how much it sucks feeling drunk and bitter at the end of yet another no-score Alabama and Clemson game. Not only that, but we despise when we only hear about the 7-OT LSU and A&M game when that asshole Greg spoils the score. That's why CFB Game of The Week's algorithm reviews the games after they happen and tells you which replays to watch: spoiler-free. 

We wanted this website to be able to automatically tell us the top games through history without having to either take some rando's word for it or having some ESPN article spell out exactly how the game happened. We use a variety of methods to determine if a game is interesting, including mathematical analysis of the play-by-play data and historical analysis of similar games. There are plans to make the rankings more subjective to include human reasons for getting blitzed on a Saturday night. For example, high-pressure games, rivalry games, and ranked games will get a boost to their rating. There are even plans on using state-of-the-art technology to automatically rank A&M's games as boring. 

# Tech/framework used

Part of the motivation for this project included learning some new architectures, tools, and frameworks.

Weekly CFB was built with:
* Python3 (for backend lambdas)
* React (for the frontend)
* AWS Serverless Application Model (for IaC)
* DynamoDB (for persistance)
* TravisCI / Jest / Pytest (for CI/CD)


# Installation

1. Download the repository
2. Install the AWS SAM commandline and yarn.
3. Run `yarn install` in the `frontend/` folder to install the dependencies for the React project.
4. Use `yarn start` in the `frontend/` folder to start the development frontend server locally.
5. Use `sam local` to test the backend code locally.
6. Done!

# Tests
TravisCI tests every commit and deploys changes that pass the tests defined for React, Python, and AWS.
## Frontend
Use `yarn test` to run the frontend testing suite.

## Backend
Use `sam validate` to test the AWS SAM template.

Use `pytest <filename>` to run the backend testing suite for Python.

# How to use?

Visit the website at [https://cfbgameoftheweek.com/](https://cfbgameoftheweek.com/).

# Contribute

Any and all contributions are welcome. This is a labor of love so development may slow down or speed up depending on how well the Longhorns are doing at the moment, so please be patient with me getting back to you.

# Credits

This project wouldn't be where it is today without the help of [andmcadams](https://github.com/andmcadams).

# License

This project uses the GNU GPLv3 license.
