import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/corpus_provider.dart';
import 'add_corpus_screen.dart';
import 'translate_corpus_screen.dart';
import 'analyze_sentences_screen.dart';
import 'review_sentences_screen.dart';

class CorpusListScreen extends ConsumerWidget {
  const CorpusListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final corpusListAsync = ref.watch(corpusListProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Corpuses'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              ref.invalidate(corpusListProvider);
            },
          ),
        ],
      ),
      body: corpusListAsync.when(
        data: (corpuses) {
          if (corpuses.isEmpty) {
            return const Center(
              child: Text('No corpuses found. Add one to get started!'),
            );
          }

          return ListView.builder(
            itemCount: corpuses.length,
            itemBuilder: (context, index) {
              final corpus = corpuses[index];
              return Card(
                margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                child: ListTile(
                  title: Text(
                    corpus.name,
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  subtitle: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (corpus.description != null)
                        Padding(
                          padding: const EdgeInsets.only(top: 4),
                          child: Text(corpus.description!),
                        ),
                      const SizedBox(height: 4),
                      Text('Sentences: ${corpus.sentenceCount}'),
                      if (corpus.url != null)
                        Padding(
                          padding: const EdgeInsets.only(top: 4),
                          child: Text(
                            'URL: ${corpus.url}',
                            style: TextStyle(
                              color: Colors.blue[700],
                              fontSize: 12,
                            ),
                          ),
                        ),
                    ],
                  ),
                  trailing: PopupMenuButton<String>(
                    onSelected: (value) {
                      switch (value) {
                        case 'translate':
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => TranslateCorpusScreen(
                                corpusName: corpus.name,
                              ),
                            ),
                          );
                          break;
                        case 'analyze':
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => AnalyzeSentencesScreen(
                                corpusName: corpus.name,
                              ),
                            ),
                          );
                          break;
                        case 'review':
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => ReviewSentencesScreen(
                                corpusName: corpus.name,
                              ),
                            ),
                          );
                          break;
                      }
                    },
                    itemBuilder: (context) => [
                      const PopupMenuItem(
                        value: 'translate',
                        child: Row(
                          children: [
                            Icon(Icons.translate),
                            SizedBox(width: 8),
                            Text('Translate'),
                          ],
                        ),
                      ),
                      const PopupMenuItem(
                        value: 'analyze',
                        child: Row(
                          children: [
                            Icon(Icons.analytics),
                            SizedBox(width: 8),
                            Text('Analyze'),
                          ],
                        ),
                      ),
                      const PopupMenuItem(
                        value: 'review',
                        child: Row(
                          children: [
                            Icon(Icons.reviews),
                            SizedBox(width: 8),
                            Text('Review'),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              );
            },
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
                  ref.invalidate(corpusListProvider);
                },
                child: const Text('Retry'),
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => const AddCorpusScreen(),
            ),
          );
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}

