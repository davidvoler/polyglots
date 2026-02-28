import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:just_audio/just_audio.dart';
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
    this.isReviewMode = false,
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

  // Lesson context for saving results
  int _courseId = 0;
  int _moduleId = 0;
  int _lessonId = 0;
  String _lang = '';
  String _toLang = '';

  QuizNotifier() : super(const QuizState());

  @override
  void dispose() {
    _audioPlayer.dispose();
    super.dispose();
  }

  // Load quiz from backend (legacy flow from home page)
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
      final demoQuiz = ApiService.createDemoQuiz(
        lang: UserPreferencesService.sourceLanguage.code,
        toLang: UserPreferencesService.targetLanguage.code,
      );

      state = state.copyWith(
        quiz: demoQuiz,
        isLoading: false,
        error: 'Backend not accessible. Using demo quiz.',
        currentQuestionIndex: 0,
        isAnswered: false,
        correctAnswers: [],
        wrongAnswers: [],
        isReviewMode: false,
      );
    }
  }

  // Load quiz for a specific lesson (from course detail page)
  Future<void> loadQuizForLesson({
    required int courseId,
    required int lessonId,
    required int moduleId,
    required String lang,
    required String toLang,
  }) async {
    _courseId = courseId;
    _moduleId = moduleId;
    _lessonId = lessonId;
    _lang = lang;
    _toLang = toLang;

    state = state.copyWith(isLoading: true, error: null);

    try {
      final quiz = await ApiService.getQuizForLesson(
        courseId: courseId,
        lessonId: lessonId,
        moduleId: moduleId,
        lang: lang,
        toLang: toLang,
        userId: UserPreferencesService.userId,
      );

      if (quiz.sentences.isEmpty) {
        state = state.copyWith(
          isLoading: false,
          error: 'No exercises found for this lesson.',
        );
        return;
      }

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
      print('Failed to load lesson quiz: $e');
      state = state.copyWith(
        isLoading: false,
        error: 'Failed to load quiz: $e',
      );
    }
  }

  // Select option (single-choice flow)
  void selectOption(int index) {
    if (state.isAnswered) return;

    final currentSentence = state.currentSentence;
    if (currentSentence == null) return;

    currentSentence.attempts++;
    currentSentence.options[index].selected = true;

    if (currentSentence.options[index].correct) {
      _markAnswered(isCorrect: true, currentSentence: currentSentence);
    } else {
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
      case QuizQuestionType.typing:
        currentSentence.attempts++;
        _markAnswered(isCorrect: true, currentSentence: currentSentence);
        break;
      case QuizQuestionType.multipleChoice:
      case QuizQuestionType.identifyWords:
        currentSentence.attempts++;
        final selected = <int>{};
        final correct = <int>{};
        for (var i = 0; i < currentSentence.options.length; i++) {
          if (currentSentence.options[i].selected) {
            selected.add(i);
          }
          if (currentSentence.options[i].correct) {
            correct.add(i);
          }
        }
        final isCorrect = selected.isNotEmpty && selected.length == correct.length && selected.containsAll(correct);
        _markAnswered(isCorrect: isCorrect, currentSentence: currentSentence);
        break;
      case QuizQuestionType.singleChoice:
        break;
    }
  }

  void _markAnswered({required bool isCorrect, required QuizSentence currentSentence}) {
    currentSentence.answered = true;
    state = state.copyWith(isAnswered: true);

    if (isCorrect) {
      final newCorrectAnswers = List<int>.from(state.correctAnswers)..add(state.currentQuestionIndex);
      state = state.copyWith(correctAnswers: newCorrectAnswers);
    } else {
      final newWrongAnswers = List<int>.from(state.wrongAnswers)..add(state.currentQuestionIndex);
      state = state.copyWith(wrongAnswers: newWrongAnswers);
    }

    // Save result for this exercise
    saveResultsSingle(currentSentence, isCorrect);
  }

  bool isOptionSelected(int index) {
    final currentSentence = state.currentSentence;
    if (currentSentence == null) return false;
    if (index >= 0 && index < currentSentence.options.length) {
      return currentSentence.options[index].selected;
    }
    return false;
  }

  bool isOptionCorrect(int index) {
    final currentSentence = state.currentSentence;
    if (currentSentence == null) return false;
    if (index >= 0 && index < currentSentence.options.length) {
      return currentSentence.options[index].correct;
    }
    return false;
  }

  void nextQuestion() {
    if (state.isLastQuestion) return;

    state = state.copyWith(
      currentQuestionIndex: state.currentQuestionIndex + 1,
      isAnswered: false,
    );

    if (UserPreferencesService.autoPlay) {
      Future.delayed(const Duration(milliseconds: 300), () {
        playAudio(normal: true);
      });
    }
  }

  void previousQuestion() {
    if (state.isFirstQuestion) return;

    state = state.copyWith(
      currentQuestionIndex: state.currentQuestionIndex - 1,
      isAnswered: false,
    );
  }

  Future<void> playAudio({required bool normal}) async {
    final currentSentence = state.currentSentence;
    if (currentSentence == null) return;
    if (!currentSentence.hasAudio()) return;

    try {
      final audioUrl = ApiService.getSoundUrl(currentSentence.sound);
      if (audioUrl.isEmpty) return;

      final isAccessible = await ApiService.testAudioUrl(currentSentence.sound);
      if (!isAccessible) return;

      await _audioPlayer.stop();
      await _audioPlayer.setUrl(audioUrl);
      await _audioPlayer.setSpeed(normal ? 1.0 : 0.7);
      await _audioPlayer.play();
    } catch (e) {
      print('Audio playback error: $e');
    }
  }

  void resetQuiz() {
    state = state.copyWith(
      currentQuestionIndex: 0,
      isAnswered: false,
      correctAnswers: [],
      wrongAnswers: [],
      isReviewMode: false,
    );
  }

  void enterReviewMode() {
    state = state.copyWith(
      currentQuestionIndex: 0,
      isAnswered: false,
      isReviewMode: true,
    );
  }

  Future<void> loadNextQuiz() async {
    await loadQuiz(mode: PracticeModes.step);
  }

  // Save result for a single exercise
  Future<void> saveResultsSingle(QuizSentence sentence, bool isCorrect) async {
    try {
      final exerciseId = int.tryParse(sentence.id) ?? 0;
      await ApiService.saveResult(
        userId: UserPreferencesService.userId,
        lang: _lang.isNotEmpty ? _lang : UserPreferencesService.sourceLanguage.code,
        toLang: _toLang.isNotEmpty ? _toLang : UserPreferencesService.targetLanguage.code,
        courseId: _courseId,
        moduleId: _moduleId,
        lessonId: _lessonId,
        exerciseId: exerciseId,
        exerciseType: _questionTypeToExerciseType(sentence.questionType),
        correct: isCorrect,
        attempts: sentence.attempts,
      );
    } catch (e) {
      print("Problem with saving results: $e");
    }
  }

  String _questionTypeToExerciseType(QuizQuestionType type) {
    switch (type) {
      case QuizQuestionType.singleChoice:
        return 'sentence_single_choice';
      case QuizQuestionType.multipleChoice:
        return 'sentence_multiple_choice';
      case QuizQuestionType.identifyWords:
        return 'identify_words_in_speech';
      case QuizQuestionType.explanation:
        return 'explanation';
      case QuizQuestionType.typing:
        return 'type_question';
      case QuizQuestionType.wordSearch:
        return 'words_in_grid';
    }
  }

  // Save results for the entire quiz (called on finish)
  Future<void> saveResults() async {
    // Results are already saved per-question in _markAnswered
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
