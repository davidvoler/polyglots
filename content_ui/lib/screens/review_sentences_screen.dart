import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/sentence_provider.dart';
import '../models/requests.dart';

class ReviewSentencesScreen extends ConsumerStatefulWidget {
  final String corpusName;

  const ReviewSentencesScreen({
    super.key,
    required this.corpusName,
  });

  @override
  ConsumerState<ReviewSentencesScreen> createState() => _ReviewSentencesScreenState();
}

class _ReviewSentencesScreenState extends ConsumerState<ReviewSentencesScreen> {
  final _sourceController = TextEditingController(text: '');
  final _langController = TextEditingController();
  int _currentIndex = 0;
  String? _selectedLang;
  String? _selectedSource;

  @override
  void initState() {
    super.initState();
    _sourceController.text = widget.corpusName;
  }

  @override
  void dispose() {
    _sourceController.dispose();
    _langController.dispose();
    super.dispose();
  }

  void _loadSentences() {
    if (_sourceController.text.trim().isNotEmpty && 
        _langController.text.trim().isNotEmpty) {
      setState(() {
        _selectedSource = _sourceController.text.trim();
        _selectedLang = _langController.text.trim();
        _currentIndex = 0;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.corpusName.isEmpty 
            ? 'Review Sentences' 
            : 'Review: ${widget.corpusName}'),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                TextField(
                  controller: _sourceController,
                  decoration: const InputDecoration(
                    labelText: 'Source/Corpus',
                    border: OutlineInputBorder(),
                    hintText: 'Enter corpus name or source',
                  ),
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    Expanded(
                      child: TextField(
                        controller: _langController,
                        decoration: const InputDecoration(
                          labelText: 'Language',
                          border: OutlineInputBorder(),
                          hintText: 'e.g., en, es, fr',
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    ElevatedButton(
                      onPressed: _loadSentences,
                      child: const Text('Load'),
                    ),
                  ],
                ),
              ],
            ),
          ),
          if (_selectedLang != null) ...[
            Expanded(
              child: Consumer(
                builder: (context, ref, child) {
                  final request = ReviewRequest(
                    operation: 'review',
                    source: _selectedSource!,
                    lang: _selectedLang!,
                    limit: 300,
                    offset: 0,
                  );

                  final sentencesAsync = ref.watch(reviewSentencesProvider(request));

                  return sentencesAsync.when(
                    data: (sentences) {
                      if (sentences.isEmpty) {
                        return const Center(
                          child: Text('No sentences found for review.'),
                        );
                      }

                      if (_currentIndex >= sentences.length) {
                        return const Center(
                          child: Text('All sentences reviewed!'),
                        );
                      }

                      final sentence = sentences[_currentIndex];

                      return Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Card(
                              elevation: 4,
                              child: Padding(
                                padding: const EdgeInsets.all(16),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      'Sentence ${_currentIndex + 1} of ${sentences.length}',
                                      style: Theme.of(context).textTheme.titleMedium,
                                    ),
                                    const SizedBox(height: 16),
                                    Text(
                                      sentence.text,
                                      style: Theme.of(context).textTheme.bodyLarge,
                                    ),
                                    if (sentence.toText != null) ...[
                                      const SizedBox(height: 16),
                                      const Divider(),
                                      const SizedBox(height: 8),
                                      Text(
                                        'Translation:',
                                        style: Theme.of(context).textTheme.labelLarge,
                                      ),
                                      const SizedBox(height: 8),
                                      Text(
                                        sentence.toText!,
                                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                          fontStyle: FontStyle.italic,
                                        ),
                                      ),
                                    ],
                                    if (sentence.source != null) ...[
                                      const SizedBox(height: 16),
                                      Text(
                                        'Source: ${sentence.source}',
                                        style: Theme.of(context).textTheme.bodySmall,
                                      ),
                                    ],
                                  ],
                                ),
                              ),
                            ),
                            const Spacer(),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                ElevatedButton(
                                  onPressed: _currentIndex > 0
                                      ? () {
                                          setState(() {
                                            _currentIndex--;
                                          });
                                        }
                                      : null,
                                  child: const Text('Previous'),
                                ),
                                Text(
                                  '${_currentIndex + 1} / ${sentences.length}',
                                  style: Theme.of(context).textTheme.bodyLarge,
                                ),
                                ElevatedButton(
                                  onPressed: _currentIndex < sentences.length - 1
                                      ? () {
                                          setState(() {
                                            _currentIndex++;
                                          });
                                        }
                                      : null,
                                  child: const Text('Next'),
                                ),
                              ],
                            ),
                          ],
                        ),
                      );
                    },
                    loading: () => const Center(child: CircularProgressIndicator()),
                    error: (error, stack) => Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text('Error: $error'),
                          const SizedBox(height: 16),
                          ElevatedButton(
                            onPressed: () {
                              ref.invalidate(reviewSentencesProvider(request));
                            },
                            child: const Text('Retry'),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
          ] else
            const Expanded(
              child: Center(
                child: Text('Enter a language and click Load to start reviewing sentences.'),
              ),
            ),
        ],
      ),
    );
  }
}

