# Debate Forum Application Documentation

## Overview

Developed by Stanislaw Dutkiewicz, the Debate Forum Application provides a platform for users to engage in dynamic discussions. Using the Flask framework and SQLite for data persistence, users can register, create debate topics, post claims, and even reply to existing claims.

## Table of Contents

1. Database Structure
2. API Endpoints
3. Usage Guide

---

### 1. Database Structure

The SQLite database serves as the backbone for data storage. Here's a detailed look:

- **users**: Stores user credentials and personal details.
  - `id`: Unique identifier for each user.
  - `username`: Unique username chosen by the user.
  - `password`: Encrypted password for security.
  - `name`: Full name of the user.
  - `email`: Email address of the user.

- **topics**: Captures the essence of debates.
  - `id`: Unique identifier for each topic.
  - `title`: The subject or title of the debate.
  - `user_id`: References the creator of the topic.
  - `timestamp`: Records when the topic was created.

- **claims**: Represents individual arguments or statements.
  - `id`: Unique identifier for each claim.
  - `header`: A brief header for the claim.
  - `user_id`: References the user who posted the claim.
  - `topic_id`: Links the claim to a specific topic.
  - `timestamp`: Records when the claim was made.

- **replies**: Allows users to discuss or counter a claim.
  - `id`: Unique identifier for each reply.
  - `content`: The actual text of the reply.
  - `user_id`: References the user replying.
  - `author_id`: Optionally references a specific author being replied to.
  - `claim_id`: Associates the reply with a particular claim.
  - `timestamp`: Notes when the reply was posted.

---

### 2. API Endpoints

The application provides several endpoints to facilitate user interactions:

- **GET `/`**: Displays a list of active debate topics.
- **GET/POST `/register`**: Enables new users to register. Upon POST, it checks for username uniqueness, then saves user details if valid.

(Note: The application likely contains more endpoints that provide added functionality such as login, topic creation, etc., which are not detailed in the provided snippet.)

---

### 3. Usage Guide

**Registration**:
1. Navigate to the `/register` endpoint in your browser.
2. Fill in the required fields: `username`, `password`, `name`, and `email`.
3. Click on the register button.
4. If the username is unique and all details are valid, registration will be successful, and you'll be prompted to log in. Otherwise, you'll receive an error message prompting you to choose another username.

(Note: A comprehensive usage guide for functionalities like topic creation, posting claims, and replying to claims would require a complete examination of the `run.py` file.)

---