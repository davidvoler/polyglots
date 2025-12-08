import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/requests.dart';
import '../providers/api_provider.dart';

class LoadCsvScreen extends ConsumerStatefulWidget {
  const LoadCsvScreen({super.key});

  @override
  ConsumerState<LoadCsvScreen> createState() => _LoadCsvScreenState();
}

class _LoadCsvScreenState extends ConsumerState<LoadCsvScreen> {
  final _formKey = GlobalKey<FormState>();
  final _filePathController = TextEditingController();
  final _corpusController = TextEditingController();
  final _langController = TextEditingController();

  @override
  void dispose() {
    _filePathController.dispose();
    _corpusController.dispose();
    _langController.dispose();
    super.dispose();
  }

  void _loadCsv() {
    if (_formKey.currentState!.validate()) {
      final request = LoadCsvRequest(
        filePath: _filePathController.text.trim(),
        corpus: _corpusController.text.trim(),
        lang: _langController.text.trim(),
      );

      final apiService = ref.read(apiServiceProvider);
      apiService.loadCsv(request).then((result) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('CSV loaded successfully: ${result.toString()}'),
          ),
        );
      }).catchError((error) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $error')),
        );
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Load CSV'),
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            TextFormField(
              controller: _filePathController,
              decoration: const InputDecoration(
                labelText: 'File Path *',
                border: OutlineInputBorder(),
                hintText: 'Enter path to CSV file',
              ),
              validator: (value) {
                if (value == null || value.trim().isEmpty) {
                  return 'Please enter file path';
                }
                return null;
              },
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _corpusController,
              decoration: const InputDecoration(
                labelText: 'Corpus Name *',
                border: OutlineInputBorder(),
                hintText: 'Enter corpus name',
              ),
              validator: (value) {
                if (value == null || value.trim().isEmpty) {
                  return 'Please enter corpus name';
                }
                return null;
              },
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _langController,
              decoration: const InputDecoration(
                labelText: 'Language *',
                border: OutlineInputBorder(),
                hintText: 'e.g., en, es, fr',
              ),
              validator: (value) {
                if (value == null || value.trim().isEmpty) {
                  return 'Please enter language';
                }
                return null;
              },
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: _loadCsv,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: const Text('Load CSV'),
            ),
          ],
        ),
      ),
    );
  }
}

