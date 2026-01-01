# Polyglots 

Polyglots is a system for authoring, and managing language learning data using AI.

## Architecture

This repository contains **3 main applications**, each consisting of a client-server architecture:

1. **Content Manager** - for creating, loading and generating content
   - Client: `content/content_ui/` (Flutter)
   - Server: `content/content_server/` (Python)

2. **Editor** - for creating courses and lessons from existing content
   - Client: `editor/editor_ui/` (Flutter)
   - Server: `editor/editor_server/` (Python)

3. **Student** - for learning
   - Client: `student/student_ui/` (Flutter)
   - Server: `student/student_server/` (Python)

## Technology Stack

- **Client-side**: Flutter (cross-platform mobile and desktop applications)
- **Server-side**: Python (FastAPI-based REST APIs)
- **Database**: PostgreSQL
- **Infrastructure**: Docker Compose for local development


## how do you teach an alphabet?

1. Identify the letter in words or sentences - multi select
2. Meaning or words with the letter - identify the writing from sound - advanced after you know quite most of the letters in the word
3. words practice - just a normal words practice - when all words have the letter in them

