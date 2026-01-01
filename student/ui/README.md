# Listen & Learn - Quiz UI 1

A Flutter language learning app with a clean, organized architecture.

## Project Structure

The app has been refactored from a single `main.dart` file into a well-organized feature-based structure:

```
lib/
├── main.dart                           # App entry point
├── core/                              # App-wide configurations
│   └── theme/
│       └── app_theme.dart             # Theme configuration
├── features/                          # Feature-specific pages
│   ├── home/
│   │   └── presentation/
│   │       └── pages/
│   │           └── home_page.dart     # Main home screen
│   ├── languages/
│   │   └── presentation/
│   │       └── pages/
│   │           └── languages_page.dart # Language selection
│   ├── progress/
│   │   └── presentation/
│   │       └── pages/
│   │           └── progress_page.dart # Progress tracking
│   └── quiz/
│       └── presentation/
│           └── pages/
│               └── quiz_page.dart     # Quiz functionality
└── shared/                            # Shared components
    ├── models/
    │   ├── app_data.dart              # Static app data
    │   ├── language_model.dart        # Language data model
    │   └── quiz_model.dart            # Quiz data models
    └── widgets/
        ├── language_dropdown.dart     # Reusable dropdown
        └── settings_toggle.dart       # Reusable toggle
```

## Features

### Home Page (`features/home/`)
- Main dashboard with language progress
- Quick access to start learning
- Settings configuration
- Daily question counter
- **Scrollable content** to prevent overflow

### Languages Page (`features/languages/`)
- Native language selection
- Target language selection with progress
- Visual language cards with flags
- **Proper scrolling** with constrained heights

### Progress Page (`features/progress/`)
- Learning statistics
- Recent words and sentences
- Progress tracking
- **Scrollable content** with Expanded widget

### Quiz Page (`features/quiz/`)
- Interactive audio-based quizzes
- Multiple choice questions
- Progress tracking
- Quiz summary with results
- **Scrollable quiz summary** to prevent overflow

## Shared Components

### Models (`shared/models/`)
- **LanguageModel**: Represents language data with flags, progress, etc.
- **QuizQuestion**: Quiz question structure with audio, text, options
- **QuizAnswer**: User answer tracking
- **AppData**: Static data like language lists and quiz content

### Widgets (`shared/widgets/`)
- **LanguageDropdown**: Reusable dropdown for language selection
- **SettingsToggle**: Reusable toggle for app settings

## Scrolling Implementation

All pages now have proper scrolling to prevent overflow issues:

### Home Page
- Wrapped in `SingleChildScrollView` to handle content overflow
- Added bottom padding for better scroll experience

### Languages Page
- Uses `Expanded` with `SingleChildScrollView` for proper scrolling
- Grid and List views have constrained heights with `NeverScrollableScrollPhysics`

### Progress Page
- Uses `Expanded` with `SingleChildScrollView` for scrollable content
- Proper layout structure prevents overflow

### Quiz Page
- Quiz summary wrapped in `SingleChildScrollView`
- Removed `Spacer()` and added proper spacing
- Added bottom padding for better scroll experience

## Architecture Benefits

1. **Separation of Concerns**: Each feature is isolated in its own directory
2. **Reusability**: Shared widgets and models can be used across features
3. **Maintainability**: Easy to find and modify specific functionality
4. **Scalability**: New features can be added following the same pattern
5. **Testability**: Individual components can be tested in isolation
6. **Responsive Design**: All pages handle different screen sizes with proper scrolling

## Getting Started

1. Ensure Flutter is installed
2. Run `flutter pub get` to install dependencies
3. Run `flutter run` to start the app

## Code Quality

The app follows Flutter best practices:
- Proper widget separation
- Type-safe models
- Reusable components
- Clean architecture principles
- Responsive scrolling implementation

## Future Enhancements

- Add state management (Provider/Riverpod)
- Implement actual audio functionality
- Add backend integration
- Include more language pairs
- Add user authentication


## Providers & Services

The app uses Riverpod for state management with the following providers:

### Core Services (`lib/core/services/`)

#### UserPreferencesService
- Manages local storage of user preferences
- Handles language settings, quiz options, and user stats
- Provides getters/setters for all user data

#### UserService
- Handles backend communication
- Loads and saves user preferences
- Manages quiz results synchronization
- Handles API calls with timeout and error handling

#### QuizService
- **Dedicated service for quiz-related API calls**
- **Fetches quiz data from `/api/v1/quiz/get_quiz`**
- **Saves quiz results to `/api/v1/quiz/save_results`**
- **Gets quiz statistics from `/api/v1/quiz/get_stats`**
- Handles quiz-specific data formatting and validation

### Providers (`lib/shared/providers/`)

#### ThemeProvider
- Manages app theme state (light/dark mode)
- Persists theme preferences
- Provides theme switching functionality

#### SettingsProvider
- Manages user settings state
- Handles language selection and quiz options
- Syncs with backend via UserService
- Provides loading states and error handling

#### ProgressProvider
- Manages user progress data
- Tracks questions answered, accuracy, and stats
- Handles quiz result saving
- Provides progress reset functionality

#### QuizProvider
- Manages quiz state and flow
- **Fetches quiz data from `/api/v1/quiz/get_quiz`**
- Handles question navigation and answer selection
- Manages audio playback simulation
- Provides quiz summary and result saving
- **Supports fallback to local data if API fails**
- **Includes loading states for quiz data fetching**

### Provider Usage

```dart
// Access providers in widgets
final settings = ref.watch(settingsProvider);
final progress = ref.watch(progressProvider);
final quiz = ref.watch(quizProvider);

// Update state
ref.read(settingsProvider.notifier).updateSelectedLanguage('french');
ref.read(progressProvider.notifier).incrementQuestionsToday();
ref.read(quizProvider.notifier).selectAnswer(0);

// Quiz-specific operations
ref.read(quizProvider.notifier).refreshQuizData(); // Reload from API
ref.read(quizProvider.notifier).startNewQuiz(); // Start fresh quiz
ref.read(quizProvider.notifier).saveQuizResults(); // Save to backend
```

### Data Flow

1. **Initialization**: Services load data from local storage and backend
2. **State Management**: Providers manage reactive state updates
3. **Persistence**: Changes are saved to local storage and backend
4. **Error Handling**: Providers handle loading states and errors gracefully 





