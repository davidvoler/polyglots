import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/requests.dart';
import '../providers/api_provider.dart';

class SubtitlesScreen extends ConsumerStatefulWidget {
  const SubtitlesScreen({super.key});

  @override
  ConsumerState<SubtitlesScreen> createState() => _SubtitlesScreenState();
}

class _SubtitlesScreenState extends ConsumerState<SubtitlesScreen> {
  final _formKey = GlobalKey<FormState>();
  final _sourceController = TextEditingController();
  final _langController = TextEditingController();
  final _limitController = TextEditingController();
  bool _useFullCorpus = true;

  @override
  void dispose() {
    _sourceController.dispose();
    _langController.dispose();
    _limitController.dispose();
    super.dispose();
  }

  void _analyzeSubtitles() {
    if (_formKey.currentState!.validate()) {
      final request = BatchRequest(
        operation: 'subtitles',
        source: _sourceController.text.trim(),
        lang: _langController.text.trim(),
        limit: _useFullCorpus ? -1 : int.tryParse(_limitController.text) ?? -1,
        review: true,
      );

      final apiService = ref.read(apiServiceProvider);
      apiService.analyzeSubtitles(request).then((result) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Subtitles analysis started: ${result.toString()}'),
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
        title: const Text('Subtitles'),
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text(
              'Analyze Subtitles',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 24),
            TextFormField(
              controller: _sourceController,
              decoration: const InputDecoration(
                labelText: 'Source/Corpus *',
                border: OutlineInputBorder(),
                hintText: 'Enter corpus name or source',
              ),
              validator: (value) {
                if (value == null || value.trim().isEmpty) {
                  return 'Please enter source';
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
            SwitchListTile(
              title: const Text('Use Full Corpus'),
              subtitle: const Text('Analyze all subtitles or limit'),
              value: _useFullCorpus,
              onChanged: (value) {
                setState(() {
                  _useFullCorpus = value;
                });
              },
            ),
            if (!_useFullCorpus) ...[
              const SizedBox(height: 16),
              TextFormField(
                controller: _limitController,
                decoration: const InputDecoration(
                  labelText: 'Limit Subtitles',
                  border: OutlineInputBorder(),
                  hintText: 'Number of subtitles to analyze',
                ),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (!_useFullCorpus) {
                    if (value == null || value.trim().isEmpty) {
                      return 'Please enter limit';
                    }
                    final limit = int.tryParse(value);
                    if (limit == null || limit <= 0) {
                      return 'Please enter a valid positive number';
                    }
                  }
                  return null;
                },
              ),
            ],
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: _analyzeSubtitles,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: const Text('Analyze Subtitles'),
            ),
          ],
        ),
      ),
    );
  }
}

