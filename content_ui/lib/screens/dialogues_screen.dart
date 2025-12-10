import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/requests.dart';
import '../providers/api_provider.dart';

class DialoguesScreen extends ConsumerStatefulWidget {
  const DialoguesScreen({super.key});

  @override
  ConsumerState<DialoguesScreen> createState() => _DialoguesScreenState();
}

class _DialoguesScreenState extends ConsumerState<DialoguesScreen> {
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

  void _processDialogues() {
    if (_formKey.currentState!.validate()) {
      final request = DialoguesRequest(
        source: _sourceController.text.trim(),
        lang: _langController.text.trim(),
        limit: _useFullCorpus ? -1 : int.tryParse(_limitController.text) ?? -1,
        review: true,
      );

      final apiService = ref.read(apiServiceProvider);
      apiService.processDialogues(request).then((result) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Dialogues processing started: ${result.toString()}'),
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
        title: const Text('Dialogues'),
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text(
              'Process Dialogues',
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
              subtitle: const Text('Process all dialogues or limit'),
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
                  labelText: 'Limit Dialogues',
                  border: OutlineInputBorder(),
                  hintText: 'Number of dialogues to process',
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
              onPressed: _processDialogues,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: const Text('Process Dialogues'),
            ),
          ],
        ),
      ),
    );
  }
}

