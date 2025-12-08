import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/sentence.dart';
import '../models/requests.dart';
import 'api_provider.dart';

final reviewSentencesProvider = FutureProvider.family<List<Sentence>, ReviewRequest>(
  (ref, request) async {
    final apiService = ref.watch(apiServiceProvider);
    return await apiService.getSentencesForReview(request);
  },
);

final analyzeSentencesProvider = FutureProvider.family<Map<String, dynamic>, AnalyzeRequest>(
  (ref, request) async {
    final apiService = ref.watch(apiServiceProvider);
    return await apiService.analyzeSentences(request);
  },
);

final translateCorpusProvider = FutureProvider.family<Map<String, dynamic>, TranslateRequest>(
  (ref, request) async {
    final apiService = ref.watch(apiServiceProvider);
    return await apiService.translateCorpus(request);
  },
);

