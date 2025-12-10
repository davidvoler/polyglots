import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/requests.dart';
import '../providers/api_provider.dart';

class TransliterateScreen extends ConsumerStatefulWidget {
  final String corpusName;

  const TransliterateScreen({
    super.key,
    required this.corpusName,
  });

  @override
  ConsumerState<TransliterateScreen> createState() => _TransliterateScreenState();
}

class _TransliterateScreenState extends ConsumerState<TransliterateScreen> {
  final _formKey = GlobalKey<FormState>();
  final _langController = TextEditingController();
  final _limitController = TextEditingController();
  bool _useFullCorpus = true;

  @override
  void dispose() {
    _langController.dispose();
    _limitController.dispose();
    super.dispose();
  }

  void _transliterateCorpus() {
    if (_formKey.currentState!.validate()) {
      final request = TransliterateRequest(
        source: widget.corpusName.isEmpty ? _langController.text : widget.corpusName,
        lang: _langController.text.trim(),
        limit: _useFullCorpus ? -1 : int.tryParse(_limitController.text) ?? -1,
        review: true,
      );

      final apiService = ref.read(apiServiceProvider);
      apiService.transliterateCorpus(request).then((result) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Transliteration started: ${result.toString()}'),
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
            ? 'Transliterate' 
            : 'Transliterate: ${widget.corpusName}'),
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            if (widget.corpusName.isNotEmpty)
              Text(
                'Corpus: ${widget.corpusName}',
                style: Theme.of(context).textTheme.titleLarge,
              ),
            if (widget.corpusName.isEmpty) ...[
              TextFormField(
                controller: TextEditingController(text: widget.corpusName),
                decoration: const InputDecoration(
                  labelText: 'Source/Corpus *',
                  border: OutlineInputBorder(),
                  hintText: 'Enter corpus name or source',
                ),
                enabled: false,
              ),
              const SizedBox(height: 16),
            ],
            const SizedBox(height: 24),
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
              subtitle: const Text('Transliterate all sentences or limit for review'),
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
                  hintText: 'Number of sentences to transliterate',
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
              onPressed: _transliterateCorpus,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: const Text('Transliterate'),
            ),
          ],
        ),
      ),
    );
  }
}

