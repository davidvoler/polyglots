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
import '../services/api_service.dart';
import '../models/dashboard.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _selectedIndex = 0;
  final ApiService _apiService = ApiService();
  DashboardResponse? _dashboardData;
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadDashboardData();
  }

  Future<void> _loadDashboardData() async {
    if (_selectedIndex != 0) return; // Only load when dashboard is selected

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final data = await _apiService.getDashboard();
      setState(() {
        _dashboardData = data;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

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
    if (index == 0) {
      _loadDashboardData();
    }
  }

  Widget _buildEmptyContent() {
    if (_isLoading) {
      return const Center(
        child: CircularProgressIndicator(),
      );
    }

    if (_errorMessage != null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.error_outline,
              size: 64,
              color: Colors.red[300],
            ),
            const SizedBox(height: 16),
            Text(
              'Error loading dashboard',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                color: Colors.red[700],
              ),
            ),
            const SizedBox(height: 8),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 32),
              child: Text(
                _errorMessage!,
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: Colors.grey[600],
                ),
              ),
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: _loadDashboardData,
              icon: const Icon(Icons.refresh),
              label: const Text('Retry'),
            ),
          ],
        ),
      );
    }

    if (_dashboardData == null) {
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

    return _buildDashboardContent();
  }

  Widget _buildDashboardContent() {
    final data = _dashboardData!;
    final totalSentences = data.content.fold<int>(0, (sum, item) => sum + item.cnt);
    final totalElements = data.contentElements.fold<int>(0, (sum, item) => sum + item.cnt);
    final totalAudio = data.audio.fold<int>(0, (sum, item) => sum + item.cnt);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Text(
            'Dashboard Overview',
            style: Theme.of(context).textTheme.headlineMedium?.copyWith(
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Content statistics and metrics',
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
              color: Colors.grey[600],
            ),
          ),
          const SizedBox(height: 32),
          // Summary Cards
          Row(
            children: [
              Expanded(
                child: _buildStatCard(
                  'Total Sentences',
                  totalSentences.toString(),
                  Icons.text_fields,
                  Colors.blue,
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: _buildStatCard(
                  'Total Elements',
                  totalElements.toString(),
                  Icons.list,
                  Colors.green,
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: _buildStatCard(
                  'Total Audio Files',
                  totalAudio.toString(),
                  Icons.volume_up,
                  Colors.orange,
                ),
              ),
            ],
          ),
          const SizedBox(height: 32),
          // Content by Corpus and Language
          _buildSection(
            'Sentences by Corpus & Language',
            Icons.library_books,
            data.content.isEmpty
                ? const Text('No data available')
                : _buildContentTable(data.content),
          ),
          const SizedBox(height: 24),
          // Content Elements by Language
          _buildSection(
            'Sentence Elements by Language',
            Icons.list_alt,
            data.contentElements.isEmpty
                ? const Text('No data available')
                : _buildElementsTable(data.contentElements),
          ),
          const SizedBox(height: 24),
          // Audio by Engine and Language
          _buildSection(
            'Audio Files by Engine & Language',
            Icons.volume_up,
            data.audio.isEmpty
                ? const Text('No data available')
                : _buildAudioTable(data.audio),
          ),
        ],
      ),
    );
  }

  Widget _buildStatCard(String title, String value, IconData icon, Color color) {
    return Card(
      elevation: 2,
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: color, size: 28),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    title,
                    style: Theme.of(context).textTheme.titleSmall?.copyWith(
                      color: Colors.grey[600],
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Text(
              value,
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSection(String title, IconData icon, Widget content) {
    return Card(
      elevation: 2,
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: Theme.of(context).colorScheme.primary),
                const SizedBox(width: 12),
                Text(
                  title,
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            content,
          ],
        ),
      ),
    );
  }

  Widget _buildContentTable(List<DashboardContent> items) {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: DataTable(
        columns: const [
          DataColumn(label: Text('Corpus')),
          DataColumn(label: Text('Language')),
          DataColumn(label: Text('Count'), numeric: true),
        ],
        rows: items.map((item) {
          return DataRow(
            cells: [
              DataCell(Text(item.corpus)),
              DataCell(Text(item.lang)),
              DataCell(Text(item.cnt.toString())),
            ],
          );
        }).toList(),
      ),
    );
  }

  Widget _buildElementsTable(List<DashboardContentElements> items) {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: DataTable(
        columns: const [
          DataColumn(label: Text('Language')),
          DataColumn(label: Text('Count'), numeric: true),
        ],
        rows: items.map((item) {
          return DataRow(
            cells: [
              DataCell(Text(item.lang)),
              DataCell(Text(item.cnt.toString())),
            ],
          );
        }).toList(),
      ),
    );
  }

  Widget _buildAudioTable(List<DashboardAudio> items) {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: DataTable(
        columns: const [
          DataColumn(label: Text('Audio Engine')),
          DataColumn(label: Text('Voice')),
          DataColumn(label: Text('Language')),
          DataColumn(label: Text('Count'), numeric: true),
        ],
        rows: items.map((item) {
          return DataRow(
            cells: [
              DataCell(Text(item.audioEngine)),
              DataCell(Text(item.voice)),
              DataCell(Text(item.lang)),
              DataCell(Text(item.cnt.toString())),
            ],
          );
        }).toList(),
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
