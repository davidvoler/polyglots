import 'package:flutter/material.dart';
import 'courses_screen.dart';
import 'lessons_screen.dart';
import 'schools_screen.dart';
import 'review_screen.dart';
import 'generate_course_wizard_screen.dart';
import 'editor_flow_screen.dart';

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
      title: 'Generate Course',
      icon: Icons.auto_awesome,
      screenBuilder: () => const GenerateCourseWizardScreen(),
    ),
    DashboardMenuItem(
      title: 'Create course (4 steps)',
      icon: Icons.edit_note,
      screenBuilder: () => const EditorCreateCourseScreen(),
    ),
    DashboardMenuItem(
      title: 'Courses',
      icon: Icons.school,
      screenBuilder: () => const CoursesScreen(),
    ),
    DashboardMenuItem(
      title: 'Lessons',
      icon: Icons.book,
      screenBuilder: () => const LessonsScreen(),
    ),
    DashboardMenuItem(
      title: 'Schools',
      icon: Icons.business,
      screenBuilder: () => const SchoolsScreen(),
    ),
    DashboardMenuItem(
      title: 'Review',
      icon: Icons.reviews,
      screenBuilder: () => const ReviewScreen(),
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
            'Welcome to Editor Dashboard',
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
                        Icons.edit_note,
                        color: Theme.of(context).colorScheme.primary,
                      ),
                      const SizedBox(width: 12),
                      Text(
                        'Editor UI',
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
