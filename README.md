# Enhanced Digital Kanban System

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Docker](#docker)
7. [API Documentation](#api-documentation)
8. [Card Management](#card-management)
9. [Testing](#testing)
10. [Version Control](#version-control)
11. [Contributing](#contributing)
12. [License](#license)

## Introduction

The Enhanced Digital Kanban System is a web-based application designed to manage inventory replenishment signals efficiently. It provides a visual interface for tracking the status of items across different stages of the supply chain, from full stock to empty, requiring replenishment.

## Features

- Visual Kanban Board with three-column layout (Full, In Use, Empty)
- Color-coded cards for easy status identification
- Filtering system by supplier, location, or item
- Real-time updates
- Responsive design
- Interactive cards with click-to-move functionality
- User authentication with organization-based separation
- Dedicated card management page for viewing and deleting cards

## Project Structure

```
enhanced-digital-kanban/
│
├── app.py                 # Main Flask application
├── card_management.py     # Card management blueprint
├── init_user.py           # Script to initialize the database and create a test user
├── requirements.txt       # Python dependencies
├── test_api.py            # API tests
├── .gitignore             # Git ignore file
├── Dockerfile             # Docker configuration file
├── docker-compose.yml     # Docker Compose configuration file
│
├── templates/
│   ├── index.html         # Main Kanban board template
│   ├── login.html         # Login page template
│   ├── register.html      # Registration page template
│   └── manage_cards.html  # Card management page template
│
└── README.md              # Project documentation
```

## Installation

### Cloning the Repository

1. Clone the repository:
   ```
   git clone https://github.com/YOUR_USERNAME/enhanced-digital-kanban.git
   cd enhanced-digital-kanban
   ```

### Local Installation

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Initialize the database and create a test user:
   ```
   python init_user.py
   ```

## Usage

### Running Locally

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`.

3. Log in with the test user credentials or register a new account.

4. Use the Kanban board to manage inventory items.

5. Access the card management page by clicking the "Manage Cards" link.

## Docker

### Building and Running with Docker

1. Build the Docker image:
   ```
   docker build -t enhanced-kanban .
   ```

2. Run the Docker container:
   ```
   docker run -p 5000:5000 enhanced-kanban
   ```

3. Access the application at `http://localhost:5000`

### Using Docker Compose

To run the application using Docker Compose:

```
docker-compose up
```

Access the application at `http://localhost:5000`

## API Documentation

The system provides a RESTful API for managing Kanban cards. For detailed endpoint information, refer to the [API Documentation](API_DOCUMENTATION.md).

## Card Management

To access the card management feature:
1. Log in to the system
2. Click on the "Manage Cards" link
3. View all Kanban cards in a tabular format
4. Delete cards using the "Delete" button next to each card

## Testing

Run the API tests using:
```
python test_api.py
```

## Version Control

This project uses Git for version control. The repository is hosted on GitHub at:
https://github.com/YOUR_USERNAME/enhanced-digital-kanban

## Contributing

Contributions to the Enhanced Digital Kanban System are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your fork and submit a pull request

Please ensure your code adheres to the existing style and passes all tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
