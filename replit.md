# Overview

This is an AI-Based Automatic Timetable Generator for Universities, designed to solve the complex problem of scheduling courses, faculty, rooms, and time slots while avoiding conflicts. The system provides a web-based interface for managing university timetable data and automatically generates optimized schedules using constraint satisfaction algorithms. The application handles course scheduling across different departments, semesters, and batches while considering faculty availability, room capacity, and time slot constraints.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Web Framework**: Flask-based web application using Jinja2 templating
- **UI Framework**: Bootstrap with dark theme for responsive design
- **Template Structure**: Base template with extended views for different modules (courses, faculty, rooms, generation)
- **Static Assets**: Custom CSS for print styles and timetable-specific formatting
- **Navigation**: Single-page application structure with tab-based views for different timetable perspectives

## Backend Architecture
- **Web Framework**: Flask with SQLAlchemy ORM for database operations
- **Database Layer**: SQLAlchemy with DeclarativeBase for model definitions
- **Session Management**: Flask sessions with configurable secret key
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies
- **Logging**: Built-in Python logging configured at DEBUG level

## Data Storage Solutions
- **Primary Database**: SQLite for development (configurable via DATABASE_URL environment variable)
- **Connection Pooling**: SQLAlchemy engine with connection recycling and pre-ping health checks
- **Models**: Four core entities with relationships:
  - Course: Academic courses with hours, department, and lab designation
  - Faculty: Teaching staff with subject assignments and department affiliation
  - Room: Physical spaces with capacity and type classification
  - TimeSlot: Time periods with day and period number organization

## Scheduling Engine
- **Algorithm**: Constraint Satisfaction Problem (CSP) solver using backtracking
- **Conflict Detection**: Multi-level constraint checking for faculty, room, and time conflicts
- **Optimization**: Basic scheduling with configurable attempt limits
- **Data Export**: Excel generation using openpyxl with formatted output

## Application Structure
- **Modular Design**: Separated concerns with distinct files for models, routes, and scheduling logic
- **Environment Configuration**: Development and production settings via environment variables
- **Error Handling**: Database rollback mechanisms and user feedback through flash messages
- **Extensibility**: Base model class structure allowing for easy model additions

# External Dependencies

## Core Framework Dependencies
- **Flask**: Web application framework with SQLAlchemy integration
- **SQLAlchemy**: ORM with declarative base for database operations
- **Werkzeug**: WSGI utilities including ProxyFix middleware

## Frontend Dependencies
- **Bootstrap**: CSS framework loaded via CDN (agent dark theme variant)
- **Font Awesome**: Icon library for UI elements
- **Custom CSS**: Local stylesheet for print optimization and timetable styling

## Data Processing Dependencies
- **Pandas**: Data manipulation for export functionality
- **OpenPyXL**: Excel file generation with formatting capabilities
- **Python Standard Library**: datetime, random, logging, and os modules

## Database Dependencies
- **SQLite**: Default database engine (development)
- **Database URL Configuration**: Support for PostgreSQL and other databases via environment variables

## Development Dependencies
- **Flask Debug Mode**: Development server with auto-reload
- **Logging Framework**: Python logging with configurable levels
- **Environment Variables**: Configuration management for database URLs and session secrets