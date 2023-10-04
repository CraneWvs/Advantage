# Advantage
## Introduction

This is the summer group project. We developed a React + Django web application for advertisers to find busy areas in New York City utilizing machine learning model.

## Screenshots for key features
![login](https://github.com/CraneWvs/Pictures/blob/main/Advantage/login.png)

login page

![home_page](https://github.com/CraneWvs/Pictures/blob/main/Advantage/home1.png)

home page

![solutions_page_overview](https://github.com/CraneWvs/Pictures/blob/main/Advantage/solutions2.png)

solution page overview

![zone_detail](https://github.com/CraneWvs/Pictures/blob/main/Advantage/map-viewer-mode1.png)

zone detail

![compare_tool](https://github.com/CraneWvs/Pictures/blob/main/Advantage/solutions-compare-board1.png)

compare tool 1

![compare_tool](https://github.com/CraneWvs/Pictures/blob/main/Advantage/solutions-compare-board2.png)

compare tool 2

![save_page](https://github.com/CraneWvs/Pictures/blob/main/Advantage/save%20page%202.png)

bookmark page

# Run
Follow these steps to set up the project on your local machine:

## Set up the environment

### 1. Clone the Repository

Begin by cloning this repository to your local machine using the following command:

```
git clone https://github.com/nezebilo/advantage.git
```

### 2. Create a Virtual Environment

It's recommended to create a virtual environment to isolate project dependencies. Navigate to the project directory and create a virtual environment:

```
cd django-backend-project
python -m venv venv
```

### 3. Activate the Virtual Environment

```
source venv/bin/activate
```

### 4. Install Dependencies

Install the project dependencies using pip:

```
pip install -r requirements.txt
```

Install Gdal:
on Linux:

```
sudo apt-get update && sudo apt-get install -y binutils libproj-dev gdal-bin python3-gdal
```

On Macos:
Follow the instructions in the link below:

```
https://gdal.org/index.html
```

## Front-end Environment Configuration

### 1. JavaScript runtime environment

Make sure you have installed Node.js and npm in your computer. You can check it by type the command in the terminal:
check Node.js

```
node -v
```

check npm (Node Package Manager)

```
npm -v
```

If not installed yet, here is the official website:
https://nodejs.org/en

For this project, recommended version is Node.js (v18.15.0) and npm (9.5.0).

### 2. Install dependencies of project

All dependencies for front-end part are listed in `/website/react-app/package.json`.
Go to front-end folder (`/website/react-app`) and install all dependencies.

```
cd ./website/react-app/
npm install
```

### 3. Run

after installing all the dependencies, we can run the dev environment.

```
cd ./website/react-app/
npm run dev
```

### 4. Build for deployment

you can now build the frontend for deployment.

```
npm run build
```

This will create a folder called dist with all static files that need to be served

## Back-end Environment Configuration

### 1. Database Setup

NOTE: For the fully functional database migrations, your database should be POSTGRESQL with PostGIS extension.
Configure your database settings in settings.py and perform the initial migration to set up the database schema:

```
python manage.py makemigrations
python manage.py migrate
```

### 2. Run the Development Server:

Start the development server to run the project locally:

```
python manage.py runserver
```

### 3. Access the backend application

Access the Application: Open your web browser and navigate to http://localhost:8000/api/ to access the API endpoints provided by the backend.

## Project Structure

website/website: The main project directory containing settings, URLs, and configuration.
website/main, user_api, save_api: The apps' directory where you can define models, views, serializers, and other app-specific components.
requirements.txt: A list of Python dependencies required for the project.
website/manage.py: A command-line utility to interact with the project.
