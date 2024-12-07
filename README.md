# BlogSite - Detailed Documentation

[Blogsite Website](https://blogsite-6ljs.onrender.com/)

This document provides comprehensive documentation for the BlogSite application, a Django-based blogging platform with LLM-powered tag generation and a RESTful API.

## Overview

BlogSite allows users to create and publish blog posts, automatically generating relevant tags using a Large Language Model (LLM) provided by Cohere.  It offers a RESTful API for programmatic access to its features and is designed for scalability and maintainability.  A frontend UI is currently using HTML , CSS and JS.

## Features

* **User Authentication:** Secure user registration and login using Django's built-in authentication system.
* **Blog Post Management:** Create and retrieve of blog posts.
* **LLM-Powered Tag Generation:**  Automatically generates tags for blog posts using the Cohere API, enhancing discoverability and organization.
* **RESTful API:**  Provides a well-defined API for interacting with the platform programmatically for create , retriveing a single and all blogs.
* **Paginated API Responses:** Handles large datasets efficiently with paginated responses.
* **Frontend UI :**  A user-friendly interface for browsing and managing blog content. some comp

## Architecture

The application follows a standard Django project structure:

* **`blogsite/`**: The root directory containing the project files.
* **`core/`**:  The main application containing models, API logic, and UI views.
    * **`apis/`**: API endpoints implemented using Django REST Framework (DRF).
    * **`llm/`**: Code for interacting with the LLM API (Cohere).
    * **`ui/`**: Code for the frontend UI.
    * **`registration/`**: Code for user registration and authentication.
    * **`models.py`**: Database models defining the data structure.
    * **`views.py`**: View functions for handling API requests and UI rendering.
    * **`static`**: Static files like CSS and JS.
    * **`templates`**: HTML templates for rendering UI.
    * **`forms.py`**: Django forms for user interaction.
    * **`tests.py`**: Unit tests for the application.
* **`website/`**: The Django project configuration directory.
    * **`settings.py`**: Project-level settings.
    * **`urls.py`**: URL routing configuration.
* **`manage.py`**: Django's command-line utility.

## API Documentation

The RESTful API is built using Django REST Framework and provides the following endpoints:

**Authentication:**

* **`/api/get-token/` (POST):**  Obtains an authentication token using username and password.  Returns an access token required for accessing protected API endpoints. And it also can use for refresh token.

**Blog Posts:**

* **`/api/posts/` (GET):** Retrieves a list of all blog posts. Supports pagination.
* **`/api/posts/` (POST):** Creates a new blog post. Requires `title` and `content`.  Tags are generated automatically.
* **`/api/posts/<int:pk>/` (GET):** Retrieves a specific blog post by its primary key (`pk`).

**Tags** For more detail see the file core/apis/README.md

**API Request Examples (using `curl`):**

```bash
# Get all blog posts
curl -H "Authorization: Bearer <your_access_token>" https://blogsite-6ljs.onrender.com//api/blogs/

# Create a new blog post
curl -X POST -H "Authorization: Bearer <your_access_token>" -H "Content-Type: application/json" -d '{"title": "My Blog Post", "content": "This is the content of my blog post."}' https://blogsite-6ljs.onrender.com/api/blogs/ 

```

## Frontend Documentation

The frontend code is organized within the `core/ui/static` , `core/ui/templates` , `core/resgisteration/static` and `core/registeration/templates` directories.  Key functionalities include:

* **User Authentication:**  Forms and JavaScript functions for handling user registration and login, interacting with the `/api/get-token/` endpoint.
* **Blog Post Display:**  JavaScript code to retrieve and display blog posts using the `/api/posts/` endpoint, including pagination support.
* **Blog Post Creation:**  A form and JavaScript functions to create new blog posts, sending data to the `/api/posts/` endpoint.
* **Tag Display:**  Functionality to display the automatically generated tags for each blog post.

## Urls 

* **`/signup/'** : For signup 
* **`/login/'** : For login
* **`/logout/'** : For logout
* **`/tags/'** : For selecting tags
* **`/home/'** : That hold feed personlized blog based upon you selected tags
* **`/create/'** : For create new blog
* **`/blog/<int:id>'** : For getting the full blog 
* **`/feed/'** : For paginated personalized feed (for api calls only by frontend)
* **`/all_feed/'** : For paginated all feed (for api calls only by frontend)

## Development Setup

* ... (Backend setup remains the same)
* **Frontend Development:** You may use a local development server or build process depending on your frontend framework (if any). The frontend code interacts with the backend API endpoints.

## Deployment

* **`Platformm`** : Render using guincorn with wsgi server ( in future try to use agsi server )
* **`Built`**: App was build using the **build.sh** file in root directory.
* **`Deployment`**: Is done dynamically with commit to github and it all action are performed using **render.yaml** file in root directory.
* **`Testing`**: It is done by using using test case in **core/tests.py** file.
* **`DataBase`**: Postgres is use as the database. and it is also configured using **render.yaml** file in root directory.
* **`CI\CD`**: CI\CD pipeline are from **.github/workflows/deploy.yml**

## Frontend specifics (Expanding on this crucial part)

**Directory Structure:**

* **`core/static/css/style.css`**:  Main stylesheet for the frontend.
* **`core/static/js/script.js`**:  Main JavaScript file containing functions for API interaction, DOM manipulation, and user interface logic.
* **`core/templates/index.html`**: The main HTML template for displaying the list of blog posts.
* **`core/templates/create_blog.html`**:  The template for the blog post creation form.
* **`core/templates/... other templates`**: Other HTML templates as needed.  (e.g., for user authentication, blog detail views).

