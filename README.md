# Network Troubleshooter

A Python-based web application for managing network devices and supporting network troubleshooting workflows. Built with **FastAPI**, **SQLModel**, and **SQLite**, this project combines my telecommunications and IP networking experience with practical Python development.

## Overview

Network Troubleshooter is a portfolio project designed to explore how web development and automation can support everyday network operations. It provides a foundation for organizing network device information and developing troubleshooting tools.

## Features

- **Device management** — organize and manage network device records.
- **Database integration** — persist device information using SQLite and SQLModel.
- **Network vendor support** — includes Cisco, Juniper, and Huawei as supported vendor options.
- **Web interface** — use FastAPI routes and HTML templates to interact with the application.
- **Modular architecture** — separates routes, services, models, schemas, templates, and utilities.
- **Extensible design** — provides a foundation for adding network diagnostics and automation capabilities.

## Technology Stack

- **Language:** Python
- **Web framework:** FastAPI
- **Database ORM:** SQLModel
- **Database:** SQLite
- **Frontend:** HTML, CSS, and Jinja2 templates
- **Development server:** Uvicorn

## Project Structure

```text
network-troubleshooter/
├── app/
│   ├── core/        # Core application configuration
│   ├── models/      # Database models
│   ├── routes/      # Application endpoints
│   ├── schemas/     # Data validation schemas
│   ├── services/    # Application business logic
│   ├── static/      # Static assets
│   ├── templates/   # HTML templates
│   ├── utils/       # Utility functions
│   ├── database.py  # Database configuration
│   └── main.py      # Application entry point
├── uploads/         # Local uploaded files
├── requirements.txt # Python dependencies
└── .git
