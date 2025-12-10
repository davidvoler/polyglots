import 'package:flutter/material.dart';
import 'corpus_list_screen.dart';
import 'review_sentences_screen.dart';
import 'analyze_sentences_screen.dart';
import 'translate_corpus_screen.dart';
import 'load_csv_screen.dart';
import 'transliterate_screen.dart';
import 'generate_content_screen.dart';
import 'group_sentences_screen.dart';
import 'dialogues_screen.dart';
import 'subtitles_screen.dart';
import 'courses_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _selectedIndex = 0;

  final List<DashboardMenuItem> _menuItems = [
    DashboardMenuItem(
      title: 'Dashboard',
      icon: Icons.dashboard,
      screenBuilder: null, // Will show empty content area
    ),
    DashboardMenuItem(
      title: 'Corpus',
      icon: Icons.library_books,
      screenBuilder: () => const CorpusListScreen(),
    ),
    DashboardMenuItem(
      title: 'Review',
      icon: Icons.reviews,
      screenBuilder: () => ReviewSentencesScreen(corpusName: ''),
    ),
    DashboardMenuItem(
      title: 'Analyze Texts',
      icon: Icons.analytics,
      screenBuilder: () => AnalyzeSentencesScreen(corpusName: ''),
    ),
    DashboardMenuItem(
      title: 'Translate',
      icon: Icons.translate,
      screenBuilder: () => TranslateCorpusScreen(corpusName: ''),
    ),
    DashboardMenuItem(
      title: 'Transliterate',
      icon: Icons.text_fields,
      screenBuilder: () => TransliterateScreen(corpusName: ''),
    ),
    DashboardMenuItem(
      title: 'Load CSV',
      icon: Icons.upload_file,
      screenBuilder: () => const LoadCsvScreen(),
    ),
    DashboardMenuItem(
      title: 'Generate Content',
      icon: Icons.auto_awesome,
      screenBuilder: () => const GenerateContentScreen(),
    ),
    DashboardMenuItem(
      title: 'Group Sentences',
      icon: Icons.group_work,
      screenBuilder: () => const GroupSentencesScreen(),
    ),
    DashboardMenuItem(
      title: 'Dialogues',
      icon: Icons.chat_bubble_outline,
      screenBuilder: () => const DialoguesScreen(),
    ),
    DashboardMenuItem(
      title: 'Subtitles',
      icon: Icons.subtitles,
      screenBuilder: () => const SubtitlesScreen(),
    ),
    DashboardMenuItem(
      title: 'Courses',
      icon: Icons.school,
      screenBuilder: () => const CoursesScreen(),
    ),
  ];

  Widget get _currentScreen {
    final item = _menuItems[_selectedIndex];
    return item.screenBuilder?.call() ?? _buildEmptyContent();
  }

  void _onMenuSelected(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  Widget _buildEmptyContent() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.dashboard,
            size: 80,
            color: Colors.grey[400],
          ),
          const SizedBox(height: 24),
          Text(
            'Welcome to Content Management',
            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
              color: Colors.grey[600],
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Select an option from the menu to get started',
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
              color: Colors.grey[500],
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          // Left Sidebar Menu
          Container(
            width: 250,
            color: Theme.of(context).colorScheme.surface,
            child: Column(
              children: [
                // Header
                Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: Theme.of(context).colorScheme.primaryContainer,
                    border: Border(
                      bottom: BorderSide(
                        color: Colors.grey[300]!,
                        width: 1,
                      ),
                    ),
                  ),
                  child: Row(
                    children: [
                      Icon(
                        Icons.dashboard,
                        color: Theme.of(context).colorScheme.primary,
                      ),
                      const SizedBox(width: 12),
                      Text(
                        'Content UI',
                        style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.bold,
                          color: Theme.of(context).colorScheme.primary,
                        ),
                      ),
                    ],
                  ),
                ),
                // Menu Items
                Expanded(
                  child: ListView.builder(
                    itemCount: _menuItems.length,
                    itemBuilder: (context, index) {
                      final item = _menuItems[index];
                      final isSelected = _selectedIndex == index;
                      return InkWell(
                        onTap: () => _onMenuSelected(index),
                        child: Container(
                          margin: const EdgeInsets.symmetric(
                            horizontal: 8,
                            vertical: 4,
                          ),
                          decoration: BoxDecoration(
                            color: isSelected
                                ? Theme.of(context).colorScheme.primaryContainer
                                : Colors.transparent,
                            borderRadius: BorderRadius.circular(8),
                            border: isSelected
                                ? Border.all(
                                    color: Theme.of(context).colorScheme.primary,
                                    width: 1,
                                  )
                                : null,
                          ),
                          child: ListTile(
                            leading: Icon(
                              item.icon,
                              color: isSelected
                                  ? Theme.of(context).colorScheme.primary
                                  : Colors.grey[700],
                            ),
                            title: Text(
                              item.title,
                              style: TextStyle(
                                fontWeight: isSelected
                                    ? FontWeight.bold
                                    : FontWeight.normal,
                                color: isSelected
                                    ? Theme.of(context).colorScheme.primary
                                    : Colors.grey[800],
                              ),
                            ),
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
          ),
          // Vertical Divider
          Container(
            width: 1,
            color: Colors.grey[300],
          ),
          // Main Content Area
          Expanded(
            child: _currentScreen,
          ),
        ],
      ),
    );
  }
}

class DashboardMenuItem {
  final String title;
  final IconData icon;
  final Widget Function()? screenBuilder;

  DashboardMenuItem({
    required this.title,
    required this.icon,
    this.screenBuilder,
  });
}
