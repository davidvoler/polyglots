import 'dart:convert';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:just_audio/just_audio.dart';
import 'package:http/http.dart' as http;
import '../models/quiz_model.dart';
import '../../core/services/api_service.dart';
import '../../core/services/user_preferences_service.dart';

// Quiz state class
class QuizState {
  final Quiz? quiz;
  final bool isLoading;
  final String? error;
  final int currentQuestionIndex;
  final bool isAnswered;
  final List<int> correctAnswers;
  final List<int> wrongAnswers;
  final bool isReviewMode;

  const QuizState({
    this.quiz,
    this.isLoading = false,
    this.error,
    this.currentQuestionIndex = 0,
    this.isAnswered = false,
    this.correctAnswers = const [],
    this.wrongAnswers = const [],
    this.isReviewMode = false,R
  });

  QuizState copyWith({
    Quiz? quiz,
    bool? isLoading,
    String? error,
    int? currentQuestionIndex,
    bool? isAnswered,
    List<int>? correctAnswers,
    List<int>? wrongAnswers,
    bool? isReviewMode,
  }) {
    return QuizState(
      quiz: quiz ?? this.quiz,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
      currentQuestionIndex: currentQuestionIndex ?? this.currentQuestionIndex,
      isAnswered: isAnswered ?? this.isAnswered,
      correctAnswers: correctAnswers ?? this.correctAnswers,
      wrongAnswers: wrongAnswers ?? this.wrongAnswers,
      isReviewMode: isReviewMode ?? this.isReviewMode,
    );
  }

  // Getters
  bool get isLoaded => quiz != null;
  bool get isLastQuestion => quiz != null && currentQuestionIndex >= quiz!.sentences.length - 1;
  bool get isFirstQuestion => currentQuestionIndex == 0;
  double get progress => quiz != null ? (currentQuestionIndex + 1) / quiz!.sentences.length : 0.0;
  int get totalQuestions => quiz?.sentences.length ?? 0;
  double get accuracy => totalQuestions > 0 ? (correctAnswers.length / totalQuestions) * 100 : 0.0;
  
  QuizSentence? get currentSentence => 
      quiz != null && currentQuestionIndex < quiz!.sentences.length 
          ? quiz!.sentences[currentQuestionIndex] 
          : null;
}

// Quiz notifier
class QuizNotifier extends StateNotifier<QuizState> {
  final AudioPlayer _audioPlayer = AudioPlayer();

  QuizNotifier() : super(const QuizState());

  @override
  void dispose() {
    _audioPlayer.dispose();
    super.dispose();
  }

  // Load quiz from backend
  Future<void> loadQuiz({PracticeModes mode = PracticeModes.step}) async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final request = QuizRequest(
        userId: UserPreferencesService.userId,
        lang: UserPreferencesService.sourceLanguage.code,
        toLang: UserPreferencesService.targetLanguage.code,
        corpus: UserPreferencesService.corpus,
        practiceId: UserPreferencesService.practiceId,
        practiceType: UserPreferencesService.practiceType,
        practiceMode: mode.name,
        reverseMode: UserPreferencesService.reverseMode,
        lastMode: UserPreferencesService.lastMode,
      );

      final quiz = await ApiService.getQuiz(request);

      // Save practice ID and type from response
      UserPreferencesService.practiceId = quiz.practiceId;
      UserPreferencesService.practiceType = quiz.practiceType;
      UserPreferencesService.lastMode = mode.name;

      state = state.copyWith(
        quiz: quiz,
        isLoading: false,
        currentQuestionIndex: 0,
        isAnswered: false,
        correctAnswers: [],
        wrongAnswers: [],
        isReviewMode: false,
      );
    } catch (e) {
      print('Failed to load quiz from backend: $e');
      // Fallback to demo quiz
      final demoQuiz = ApiService.createDemoQuiz(
        lang: UserPreferencesService.sourceLanguage.code,
        toLang: UserPreferencesService.targetLanguage.code,
      );

      state = state.copyWith(
        quiz: demoQuiz,
        isLoading: false,
        error: 'Backend not accessible. Using demo quiz with ${UserPreferencesService.sourceLanguage.name} → ${UserPreferencesService.targetLanguage.name}',
        currentQuestionIndex: 0,
        isAnswered: false,
        correctAnswers: [],
        wrongAnswers: [],
        isReviewMode: false,
      );
    }
  }

  // Select option (single-choice flow)
  void selectOption(int index) {
    if (state.isAnswered) return;
    
    final currentSentence = state.currentSentence;
    if (currentSentence == null) return;

    // Increment attempts for the current sentence
    currentSentence.attempts++;
    
    // Mark this option as selected
    currentSentence.options[index].selected = true;
    
    // Check if this option is correct
    if (currentSentence.options[index].correct) {
      // Correct answer found - mark sentence as answered
      _markAnswered(isCorrect: true, currentSentence: currentSentence);
    } else {
      // Wrong answer - add to wrong answers but allow more attempts
      List<int> newWrongAnswers = List.from(state.wrongAnswers);
      newWrongAnswers.add(state.currentQuestionIndex);
      state = state.copyWith(wrongAnswers: newWrongAnswers);
    }
  }

  void toggleOption(int index) {
    final currentSentence = state.currentSentence;
    if (currentSentence == null) return;
    if (state.isAnswered) return;
    if (index < 0 || index >= currentSentence.options.length) return;

    currentSentence.options[index].selected = !currentSentence.options[index].selected;
    state = state.copyWith(); // trigger rebuild
  }

  void submitAnswer() {
    final currentSentence = state.currentSentence;
    if (currentSentence == null) return;
    if (state.isAnswered) return;

    switch (currentSentence.questionType) {
      case QuizQuestionType.explanation:
      case QuizQuestionType.wordSearch:
        currentSentence.attempts++;
        _markAnswered(isCorrect: true, currentSentence: currentSentence);
        break;
      case QuizQuestionType.multipleChoice:
        currentSentence.attempts++;
        final selected = <int>{};
        final correct = <int>{};
        for (var i = 0; i < currentSentence.options.length; i++) {
          if (currentSentence.options[i].selected) selected.add(i);
          if (currentSentence.options[i].correct) correct.add(i);
        }
        final isCorrect = selected.isNotEmpty && selected.length == correct.length && selected.containsAll(correct);
        _markAnswered(isCorrect: isCorrect, currentSentence: currentSentence);
        break;
      case QuizQuestionType.singleChoice:
        // For single-choice, keep legacy flow: selectOption already marks answered when correct
        break;
    }
  }

  void _markAnswered({required bool isCorrect, required QuizSentence currentSentence}) {
    currentSentence.answered = true;
    state = state.copyWith(isAnswered: true);

    if (isCorrect) {
      final newCorrectAnswers = List<int>.from(state.correctAnswers)..add(state.currentQuestionIndex);
      state = state.copyWith(correctAnswers: newCorrectAnswers);
      saveResultsSingle(currentSentence);
    } else {
      final newWrongAnswers = List<int>.from(state.wrongAnswers)..add(state.currentQuestionIndex);
      state = state.copyWith(wrongAnswers: newWrongAnswers);
    }
  }

  // Check if an option is selected
  bool isOptionSelected(int index) {
    final currentSentence = state.currentSentence;
    if (currentSentence == null) return false;
    
    if (index >= 0 && index < currentSentence.options.length) {
      return currentSentence.options[index].selected;
    }
    return false;
  }

  // Check if an option is correct
  bool isOptionCorrect(int index) {
    final currentSentence = state.currentSentence;
    if (currentSentence == null) return false;
    
    if (index >= 0 && index < currentSentence.options.length) {
      return currentSentence.options[index].correct;
    }
    return false;
  }

  // Next question
  void nextQuestion() {
    if (state.isLastQuestion) return;

    state = state.copyWith(
      currentQuestionIndex: state.currentQuestionIndex + 1,
      isAnswered: false,
    );

    // Auto-play if enabled
    if (UserPreferencesService.autoPlay) {
      Future.delayed(const Duration(milliseconds: 300), () {
        playAudio(normal: true);
      });
    }
  }

  // Previous question
  void previousQuestion() {
    if (state.isFirstQuestion) return;

    state = state.copyWith(
      currentQuestionIndex: state.currentQuestionIndex - 1,
      isAnswered: false,
    );
  }

  // Play audio
  Future<void> playAudio({required bool normal}) async {
    final currentSentence = state.currentSentence;
    if (currentSentence == null) {
      print('❌ No current sentence available');
      return;
    }
    
    if (!currentSentence.hasAudio()) {
      print('❌ No audio available for current sentence');
      return;
    }

    try {
      final audioUrl = ApiService.getSoundUrl(currentSentence.sound);
      print('🔊 Playing audio: $audioUrl');
      
      if (audioUrl.isEmpty) {
        print('❌ Empty audio URL');
        return;
      }

      // Test if audio file is accessible
      final isAccessible = await ApiService.testAudioUrl(currentSentence.sound);
      if (!isAccessible) {
        print('❌ Audio file is not accessible');
        return;
      }

      await _audioPlayer.stop();
      await _audioPlayer.setUrl(audioUrl);
      await _audioPlayer.setSpeed(normal ? 1.0 : 0.7);
      await _audioPlayer.play();
      
      print('✅ Audio playback started successfully');
    } catch (e) {
      print('❌ Audio playback error: $e');
      // Re-throw the error so the UI can handle it
      rethrow;
    }
  }

  // Reset quiz
  void resetQuiz() {
    state = state.copyWith(
      currentQuestionIndex: 0,
      isAnswered: false,
      correctAnswers: [],
      wrongAnswers: [],
      isReviewMode: false,
    );
  }

  // Enter review mode
  void enterReviewMode() {
    state = state.copyWith(
      currentQuestionIndex: 0,
      isAnswered: false,
      isReviewMode: true,
    );
  }

  // Load next quiz
  Future<void> loadNextQuiz() async {
    await loadQuiz(mode: PracticeModes.step);
  }

  // Save results for a single sentence
  Future<void> saveResultsSingle(QuizSentence sentence) async {
    try {
      final url = Uri.parse('http://localhost:8000/api/v1/results/save_results');
      final client = http.Client();
      
      final data = {
        "user_id": UserPreferencesService.userId,
        "lang": UserPreferencesService.lang,
        "part_id": sentence.id,
        "attempts": sentence.attempts,
        "words": sentence.words,
        "step": state.quiz?.practiceId ?? '',
        "dialogue_line": sentence.dialogueLine,
        "dialogue_id": sentence.dialogueId,
        "corpus": UserPreferencesService.corpus,
      };

      print('📤 Saving results for sentence: ${sentence.id}');
      print('📤 Data: $data');

      final response = await client.post(
        url,
        body: json.encode(data),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Some token',
        },
      );

      print('📥 Save results response: ${response.statusCode}');
      print('📥 Response body: ${response.body}');

      if (response.statusCode == 200) {
        print('✅ Results saved successfully');
      } else {
        print('❌ Failed to save results: ${response.statusCode}');
      }
    } catch (e) {
      print("❌ Problem with saving results: $e");
    }
  }

  // Save results for the entire quiz
  Future<void> saveResults() async {
    if (state.quiz == null) {
      print('❌ No quiz to save results for');
      return;
    }

    print('📤 Saving results for entire quiz');
    
    // Save results for each answered sentence
    for (int i = 0; i < state.quiz!.sentences.length; i++) {
      final sentence = state.quiz!.sentences[i];
      if (sentence.answered) {
        await saveResultsSingle(sentence);
      }
    }
    
    print('✅ All results saved');
  }
}

// Providers
final quizProvider = StateNotifierProvider<QuizNotifier, QuizState>((ref) {
  return QuizNotifier();
});

final currentSentenceProvider = Provider<QuizSentence?>((ref) {
  final quizState = ref.watch(quizProvider);
  return quizState.currentSentence;
});

final quizProgressProvider = Provider<double>((ref) {
  final quizState = ref.watch(quizProvider);
  return quizState.progress;
});

final quizAccuracyProvider = Provider<double>((ref) {
  final quizState = ref.watch(quizProvider);
  return quizState.accuracy;
}); 