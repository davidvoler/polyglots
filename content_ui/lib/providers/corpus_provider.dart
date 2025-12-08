import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/corpus.dart';
import '../models/requests.dart';
import 'api_provider.dart';

final corpusListProvider = FutureProvider<List<Corpus>>((ref) async {
  final apiService = ref.watch(apiServiceProvider);
  return await apiService.getCorpuses();
});

final addCorpusProvider = FutureProvider.family<Corpus, AddCorpusRequest>(
  (ref, request) async {
    final apiService = ref.watch(apiServiceProvider);
    return await apiService.addCorpus(request);
  },
);

