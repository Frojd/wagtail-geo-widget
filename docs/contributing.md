# Contributing

## General
- This project uses git flow, any pull request should be based on the `develop` branch
- Commits should follow the recommendations mentioned at https://cbea.ms/git-commit/ (TLDR; Use present tense)

## Requirements
- docker
- A working Google Maps API Key

## Instruction
- Run `docker-compose up`
- Open [http://localhost:8085](http://localhost:8085)

## Testing
- Make sure you perform interface testing by going through the page models from `tests` and make sure they all behave as expected in the Wagtail interface
- Run the test suite

## Commiting
- Make sure your code are formatted using black
- Update `CHANGELOG.md` with your changes
