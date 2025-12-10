import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/requests.dart';
import '../providers/api_provider.dart';

class GroupSentencesScreen extends ConsumerStatefulWidget {
  const GroupSentencesScreen({super.key});

  @override
  ConsumerState<GroupSentencesScreen> createState() => _GroupSentencesScreenState();
}

class _GroupSentencesScreenState extends ConsumerState<GroupSentencesScreen> {
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

  void _groupSentences() {
    if (_formKey.currentState!.validate()) {
      final request = GroupSentencesRequest(
        source: _sourceController.text.trim(),
        lang: _langController.text.trim(),
        limit: _useFullCorpus ? -1 : int.tryParse(_limitController.text) ?? -1,
        review: true,
      );

      final apiService = ref.read(apiServiceProvider);
      apiService.groupSentences(request).then((result) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Sentence grouping started: ${result.toString()}'),
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
        title: const Text('Group Sentences'),
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
            const SizedBox(height: 24),
            SwitchListTile(
              title: const Text('Use Full Corpus'),
              subtitle: const Text('Group all sentences or limit'),
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
                  hintText: 'Number of sentences to group',
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
              onPressed: _groupSentences,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: const Text('Group Sentences'),
            ),
          ],
        ),
      ),
    );
  }
}

