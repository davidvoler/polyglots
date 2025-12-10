import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/requests.dart';
import '../providers/api_provider.dart';

class CoursesScreen extends ConsumerStatefulWidget {
  const CoursesScreen({super.key});

  @override
  ConsumerState<CoursesScreen> createState() => _CoursesScreenState();
}

class _CoursesScreenState extends ConsumerState<CoursesScreen> {
  final _formKey = GlobalKey<FormState>();
  final _corpusController = TextEditingController();
  final _langController = TextEditingController();
  final _toLangController = TextEditingController();

  @override
  void dispose() {
    _corpusController.dispose();
    _langController.dispose();
    _toLangController.dispose();
    super.dispose();
  }

  void _loadCourses() {
    if (_formKey.currentState!.validate()) {
      final request = CoursesRequest(
        corpus: _corpusController.text.trim().isEmpty 
            ? null 
            : _corpusController.text.trim(),
        lang: _langController.text.trim().isEmpty 
            ? null 
            : _langController.text.trim(),
        toLang: _toLangController.text.trim().isEmpty 
            ? null 
            : _toLangController.text.trim(),
      );

      final apiService = ref.read(apiServiceProvider);
      apiService.getCourses(request).then((result) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Courses loaded: ${result.toString()}'),
            backgroundColor: Colors.green,
          ),
        );
      }).catchError((error) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error: $error'),
            backgroundColor: Colors.red,
          ),
        );
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Courses'),
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text(
              'View Courses',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 24),
            TextFormField(
              controller: _corpusController,
              decoration: const InputDecoration(
                labelText: 'Corpus (optional)',
                border: OutlineInputBorder(),
                hintText: 'Filter by corpus name',
              ),
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _langController,
              decoration: const InputDecoration(
                labelText: 'Language (optional)',
                border: OutlineInputBorder(),
                hintText: 'e.g., en, es, fr',
              ),
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _toLangController,
              decoration: const InputDecoration(
                labelText: 'Target Language (optional)',
                border: OutlineInputBorder(),
                hintText: 'e.g., en, es, fr',
              ),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: _loadCourses,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: const Text('Load Courses'),
            ),
            const SizedBox(height: 16),
            const Card(
              child: Padding(
                padding: EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Note:',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    SizedBox(height: 8),
                    Text(
                      'Leave fields empty to view all courses. Use filters to narrow down results.',
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

