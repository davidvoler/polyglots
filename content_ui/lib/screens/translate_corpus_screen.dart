import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/sentence_provider.dart';
import '../models/requests.dart';

class TranslateCorpusScreen extends ConsumerStatefulWidget {
  final String corpusName;

  const TranslateCorpusScreen({
    super.key,
    required this.corpusName,
  });

  @override
  ConsumerState<TranslateCorpusScreen> createState() => _TranslateCorpusScreenState();
}

class _TranslateCorpusScreenState extends ConsumerState<TranslateCorpusScreen> {
  final _formKey = GlobalKey<FormState>();
  final _fromLangController = TextEditingController();
  final _toLangController = TextEditingController();
  final _limitController = TextEditingController();
  bool _useFullCorpus = true;

  @override
  void dispose() {
    _fromLangController.dispose();
    _toLangController.dispose();
    _limitController.dispose();
    super.dispose();
  }

  void _translateCorpus() {
    if (_formKey.currentState!.validate()) {
      final request = TranslateRequest(
        source: widget.corpusName,
        lang: _fromLangController.text.trim(),
        toLang: _toLangController.text.trim(),
        limit: _useFullCorpus ? -1 : int.tryParse(_limitController.text) ?? -1,
        review: true,
      );

      ref.read(translateCorpusProvider(request).future).then((result) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Translation started: ${result.toString()}'),
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
        title: Text('Translate: ${widget.corpusName}'),
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text(
              'Corpus: ${widget.corpusName}',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 24),
            TextFormField(
              controller: _fromLangController,
              decoration: const InputDecoration(
                labelText: 'From Language *',
                border: OutlineInputBorder(),
                hintText: 'e.g., en, es, fr',
              ),
              validator: (value) {
                if (value == null || value.trim().isEmpty) {
                  return 'Please enter source language';
                }
                return null;
              },
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _toLangController,
              decoration: const InputDecoration(
                labelText: 'To Language *',
                border: OutlineInputBorder(),
                hintText: 'e.g., en, es, fr',
              ),
              validator: (value) {
                if (value == null || value.trim().isEmpty) {
                  return 'Please enter target language';
                }
                return null;
              },
            ),
            const SizedBox(height: 24),
            SwitchListTile(
              title: const Text('Use Full Corpus'),
              subtitle: const Text('Translate all sentences or limit for review'),
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
                  hintText: 'Number of sentences to translate',
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
              onPressed: _translateCorpus,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: const Text('Translate Corpus'),
            ),
          ],
        ),
      ),
    );
  }
}

