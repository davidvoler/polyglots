import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'core/theme/app_theme.dart';
import 'core/services/user_preferences_service.dart';
import 'core/services/user_service.dart';
import 'features/home/presentation/pages/home_page.dart';
import 'features/progress/presentation/pages/progress_page.dart';
import 'shared/models/app_data.dart';
import 'shared/providers/theme_provider.dart';
import 'shared/providers/language_provider.dart';

void main() async {
  // Load environment variables
  await dotenv.load(fileName: ".env");
  
  // Initialize services
  await UserPreferencesService.initialize();
  
  // Initialize user data from backend
  await UserService.initializeUser();
  
  runApp(
    const ProviderScope(
      child: LanguageLearningApp(),
    ),
  );
}

class LanguageLearningApp extends ConsumerWidget {
  const LanguageLearningApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeState = ref.watch(themeProvider);
    final currentTheme = themeState.isDarkMode ? AppTheme.darkTheme : AppTheme.lightTheme;
    
    // Initialize language provider
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final languageNotifier = ref.read(languageProvider.notifier);
      // Set base URL from environment if available
      final baseUrl = dotenv.env['API_BASE_URL'] ?? 'http://localhost:8000';
      languageNotifier.setBaseUrl(baseUrl);
      languageNotifier.loadLanguages();
    });
    
    return MaterialApp(
      title: 'Listen & Learn',
      theme: currentTheme,
      home: MainScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class MainScreen extends ConsumerStatefulWidget {
  @override
  ConsumerState<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends ConsumerState<MainScreen> {
  int _currentPageIndex = 0;
  int questionsToday = 12;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _currentPageIndex,
        children: [
          HomePage(),
          ProgressPage(questionsToday: questionsToday),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentPageIndex,
        onTap: (index) {
          setState(() {
            _currentPageIndex = index;
          });
        },
        type: BottomNavigationBarType.fixed,
        selectedItemColor: Colors.blue.shade600,
        unselectedItemColor: Colors.grey.shade500,
        items: [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.trending_up),
            label: 'Progress',
          ),
        ],
      ),
    );
  }
}