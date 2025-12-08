import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/sentence_provider.dart';
import '../models/requests.dart';

class AnalyzeSentencesScreen extends ConsumerStatefulWidget {
  final String corpusName;

  const AnalyzeSentencesScreen({
    super.key,
    required this.corpusName,
  });

  @override
  ConsumerState<AnalyzeSentencesScreen> createState() => _AnalyzeSentencesScreenState();
}

class _AnalyzeSentencesScreenState extends ConsumerState<AnalyzeSentencesScreen> {
  final _formKey = GlobalKey<FormState>();
  final _sourceController = TextEditingController(text: '');
  final _langController = TextEditingController();
  final _limitController = TextEditingController();
  bool _useFullCorpus = true;

  @override
  void initState() {
    super.initState();
    _sourceController.text = widget.corpusName;
  }

  @override
  void dispose() {
    _sourceController.dispose();
    _langController.dispose();
    _limitController.dispose();
    super.dispose();
  }

  void _analyzeSentences() {
    if (_formKey.currentState!.validate()) {
      final request = AnalyzeRequest(
        source: _sourceController.text.trim(),
        lang: _langController.text.trim(),
        limit: _useFullCorpus ? -1 : int.tryParse(_limitController.text) ?? -1,
        review: true,
      );

      ref.read(analyzeSentencesProvider(request).future).then((result) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Analysis started: ${result.toString()}'),
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
        title: Text(widget.corpusName.isEmpty 
            ? 'Analyze Sentences' 
            : 'Analyze: ${widget.corpusName}'),
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
              subtitle: const Text('Analyze all sentences or limit for review'),
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
                  hintText: 'Number of sentences to analyze',
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
              onPressed: _analyzeSentences,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: const Text('Analyze Sentences'),
            ),
          ],
        ),
      ),
    );
  }
}

