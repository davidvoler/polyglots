import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/requests.dart';
import '../providers/api_provider.dart';

class GenerateContentScreen extends ConsumerStatefulWidget {
  const GenerateContentScreen({super.key});

  @override
  ConsumerState<GenerateContentScreen> createState() => _GenerateContentScreenState();
}

class _GenerateContentScreenState extends ConsumerState<GenerateContentScreen> {
  final _formKey = GlobalKey<FormState>();
  final _sourceController = TextEditingController();
  final _langController = TextEditingController();
  final _toLangController = TextEditingController();
  final _limitController = TextEditingController();
  bool _useFullCorpus = true;
  bool _hasToLang = false;

  @override
  void dispose() {
    _sourceController.dispose();
    _langController.dispose();
    _toLangController.dispose();
    _limitController.dispose();
    super.dispose();
  }

  void _generateContent() {
    if (_formKey.currentState!.validate()) {
      final request = GenerateContentRequest(
        source: _sourceController.text.trim(),
        lang: _langController.text.trim(),
        toLang: _hasToLang ? _toLangController.text.trim() : null,
        limit: _useFullCorpus ? -1 : int.tryParse(_limitController.text) ?? -1,
        review: true,
      );

      final apiService = ref.read(apiServiceProvider);
      apiService.generateContent(request).then((result) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Content generation started: ${result.toString()}'),
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
        title: const Text('Generate Content'),
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
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
            const SizedBox(height: 16),
            SwitchListTile(
              title: const Text('Include Target Language'),
              subtitle: const Text('Generate content for a specific target language'),
              value: _hasToLang,
              onChanged: (value) {
                setState(() {
                  _hasToLang = value;
                });
              },
            ),
            if (_hasToLang) ...[
              const SizedBox(height: 16),
              TextFormField(
                controller: _toLangController,
                decoration: const InputDecoration(
                  labelText: 'Target Language',
                  border: OutlineInputBorder(),
                  hintText: 'e.g., en, es, fr',
                ),
              ),
            ],
            const SizedBox(height: 24),
            SwitchListTile(
              title: const Text('Use Full Corpus'),
              subtitle: const Text('Generate for all sentences or limit'),
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
                  labelText: 'Limit Sentences',
                  border: OutlineInputBorder(),
                  hintText: 'Number of sentences',
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
              onPressed: _generateContent,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: const Text('Generate Content'),
            ),
          ],
        ),
      ),
    );
  }
}

