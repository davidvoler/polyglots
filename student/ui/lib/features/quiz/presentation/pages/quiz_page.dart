import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../shared/providers/quiz_provider.dart';
import '../../../../shared/models/quiz_model.dart';


class QuizPage extends ConsumerStatefulWidget {
  final String selectedLanguage;
  final String nativeLanguage;
  final bool showText;
  final bool autoPlaySound;
  final bool showTransliteration;

  const QuizPage({
    super.key,
    required this.selectedLanguage,
    required this.nativeLanguage,
    required this.showText,
    required this.autoPlaySound,
    required this.showTransliteration,
  });

  @override
  ConsumerState<QuizPage> createState() => _QuizPageState();
}

class _QuizPageState extends ConsumerState<QuizPage> {
  @override
  void initState() {
    super.initState();
    // Load quiz when page is initialized
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ref.read(quizProvider.notifier).loadQuiz();
    });
  }

  @override
  Widget build(BuildContext context) {
    final quizState = ref.watch(quizProvider);
    print('🎯 QuizPage: Building with quiz loaded: ${quizState.isLoaded}, loading: ${quizState.isLoading}');
    
    // Show loading state while fetching quiz data
    if (quizState.isLoading) {
      return Scaffold(
        body: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [Colors.green.shade50, Colors.teal.shade100],
            ),
          ),
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                CircularProgressIndicator(
                  valueColor: AlwaysStoppedAnimation<Color>(Colors.blue.shade600),
                ),
                SizedBox(height: 24),
                Text(
                  'Loading quiz questions...',
                  style: TextStyle(
                    fontSize: 18,
                    color: Colors.grey.shade700,
                  ),
                ),
              ],
            ),
          ),
        ),
      );
    }

    // Show error state if no quiz is loaded
    if (!quizState.isLoaded) {
      return Scaffold(
        body: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [Colors.green.shade50, Colors.teal.shade100],
            ),
          ),
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  Icons.quiz,
                  size: 64,
                  color: Colors.grey.shade400,
                ),
                SizedBox(height: 16),
                Text(
                  'No questions available',
                  style: TextStyle(
                    fontSize: 18,
                    color: Colors.grey.shade600,
                  ),
                ),
                SizedBox(height: 8),
                Text(
                  'Please try again later',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey.shade500,
                  ),
                ),
                SizedBox(height: 24),
                ElevatedButton(
                  onPressed: () {
                    ref.read(quizProvider.notifier).loadQuiz();
                  },
                  child: Text('Retry'),
                ),
              ],
            ),
          ),
        ),
      );
    }

    final currentSentence = quizState.currentSentence;
    if (currentSentence == null) {
      return Scaffold(
        body: Center(child: Text('No question available')),
      );
    }

    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Colors.green.shade50, Colors.teal.shade100],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: EdgeInsets.all(24.0),
            child: Column(
              children: [
                // Header with progress
                _buildQuizHeader(quizState),
                SizedBox(height: 24),

                // Main quiz content
                Expanded(
                  child: Container(
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(16),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.1),
                          blurRadius: 10,
                          offset: Offset(0, 4),
                        ),
                      ],
                    ),
                    padding: EdgeInsets.all(24),
                    child: Column(
                      children: [
                        // Instructions
                        // Text(
                        //   'Listen and select the meaning:',
                        //   style: TextStyle(
                        //     fontSize: 18,
                        //     fontWeight: FontWeight.w600,
                        //     color: Colors.grey.shade800,
                        //   ),
                        // ),

                        // Show data source indicator
                        if (quizState.error != null) ...[
                          SizedBox(height: 8),
                          Container(
                            padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                            decoration: BoxDecoration(
                              color: Colors.orange.shade100,
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(color: Colors.orange.shade300),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(
                                  Icons.warning_amber_rounded,
                                  size: 16,
                                  color: Colors.orange.shade700,
                                ),
                                SizedBox(width: 8),
                                Text(
                                  'Using local questions',
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: Colors.orange.shade700,
                                    fontWeight: FontWeight.w500,
                                  ),
                                ),
                                Spacer(),
                                GestureDetector(
                                  onTap: () {
                                    ref.read(quizProvider.notifier).loadQuiz();
                                  },
                                  child: Container(
                                    padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                    decoration: BoxDecoration(
                                      color: Colors.orange.shade200,
                                      borderRadius: BorderRadius.circular(4),
                                    ),
                                    child: Text(
                                      'Retry',
                                      style: TextStyle(
                                        fontSize: 10,
                                        color: Colors.orange.shade800,
                                        fontWeight: FontWeight.w600,
                                      ),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],

                        // SizedBox(height: 8),
                        // Text(
                        //   '${widget.selectedLanguage.toUpperCase()} → ${widget.nativeLanguage.toUpperCase()}',
                        //   style: TextStyle(
                        //     fontSize: 14,
                        //     color: Colors.grey.shade500,
                        //   ),
                        // ),
                        // SizedBox(height: 24),

                        // Audio section
                        _buildAudioSection(currentSentence),
                        SizedBox(height: 24),

                        // Answer options
                        Expanded(
                          child: _buildAnswerOptions(currentSentence, quizState),
                        ),

                        // Action button
                        _buildBottomButton(currentSentence, quizState),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildQuizHeader(QuizState quizState) {
    return Row(
      children: [
        IconButton(
          onPressed: () => Navigator.pop(context),
          icon: Icon(Icons.arrow_back, color: Colors.grey.shade700),
        ),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Quiz Progress',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.grey.shade800,
                ),
              ),
              SizedBox(height: 4),
              LinearProgressIndicator(
                value: quizState.progress,
                backgroundColor: Colors.grey.shade300,
                valueColor: AlwaysStoppedAnimation<Color>(Colors.blue.shade600),
              ),
              SizedBox(height: 4),
              Text(
                '${quizState.currentQuestionIndex + 1} of ${quizState.totalQuestions}',
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.grey.shade600,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildAudioSection(QuizSentence sentence) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: Colors.grey.shade50,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.shade200),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              IconButton(
                onPressed: () {
                  ref.read(quizProvider.notifier).playAudio(normal: true);
                },
                icon: Icon(Icons.play_arrow),
                style: IconButton.styleFrom(
                  backgroundColor: Colors.grey.shade100,
                  foregroundColor: Colors.grey.shade700,
                  padding: EdgeInsets.all(8),
                ),
              ),
              IconButton(
                onPressed: () {
                  ref.read(quizProvider.notifier).playAudio(normal: false);
                },
                icon: Icon(Icons.slow_motion_video),
                style: IconButton.styleFrom(
                  backgroundColor: Colors.grey.shade100,
                  foregroundColor: Colors.grey.shade700,
                  padding: EdgeInsets.all(8),
                ),
              ),
            ],
          ),
          if (widget.showText) ...[
            SizedBox(height: 12),
            SelectableText(
              sentence.sentence,
              style: TextStyle(
                fontSize: 36,
                fontWeight: FontWeight.w600,
                color: Colors.grey.shade800,
              ),
              textAlign: TextAlign.center,
            ),
          ],
          if (widget.showTransliteration && sentence.translit != null) ...[
            SizedBox(height: 8),
            SelectableText(
              sentence.translit!,
              style: TextStyle(
                fontSize: 28,
                color: Colors.grey.shade600,
                fontStyle: FontStyle.italic,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ],
      ),
    );
  }



  Widget _buildAnswerOptions(QuizSentence sentence, QuizState quizState) {
    switch (sentence.questionType) {
      case QuizQuestionType.explanation:
      case QuizQuestionType.wordSearch:
        return SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                sentence.sentence,
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
              ),
              if (sentence.translit != null && sentence.translit!.isNotEmpty) ...[
                const SizedBox(height: 8),
                Text(
                  sentence.translit!,
                  style: TextStyle(fontSize: 16, color: Colors.grey.shade700),
                ),
              ],
            ],
          ),
        );
      case QuizQuestionType.multipleChoice:
        return _buildMultipleSelection(sentence, quizState);
      case QuizQuestionType.singleChoice:
        return _buildSingleSelection(sentence, quizState);
    }
  }

  Widget _buildSingleSelection(QuizSentence sentence, QuizState quizState) {
    return ListView.builder(
      itemCount: sentence.options.length,
      itemBuilder: (context, index) {
        final option = sentence.options[index];
        final isSelected = ref.read(quizProvider.notifier).isOptionSelected(index);
        final isAnswered = quizState.isAnswered;
        final isCorrect = ref.read(quizProvider.notifier).isOptionCorrect(index);

        Color backgroundColor = Colors.white;
        Color borderColor = Colors.grey.shade300;
        Color textColor = Colors.grey.shade800;

        if (isAnswered) {
          if (isCorrect) {
            backgroundColor = Colors.green.shade50;
            borderColor = Colors.green.shade300;
            textColor = Colors.green.shade800;
          }
        } else if (isSelected) {
          if (isCorrect) {
            backgroundColor = Colors.green.shade50;
            borderColor = Colors.green.shade300;
            textColor = Colors.green.shade800;
          } else {
            backgroundColor = Colors.red.shade50;
            borderColor = Colors.red.shade300;
            textColor = Colors.red.shade800;
          }
        }

        return Container(
          margin: EdgeInsets.only(bottom: 12),
          child: Material(
            color: Colors.transparent,
            child: InkWell(
              onTap: isAnswered ? null : () {
                ref.read(quizProvider.notifier).selectOption(index);
              },
              borderRadius: BorderRadius.circular(12),
              child: Container(
                padding: EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: backgroundColor,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: borderColor),
                ),
                child: Row(
                  children: [
                    Container(
                      width: 24,
                      height: 24,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: isAnswered && isCorrect
                            ? Colors.green.shade600
                            : isSelected && isCorrect
                                ? Colors.green.shade600
                                : isSelected && !isCorrect
                                    ? Colors.red.shade600
                                    : Colors.grey.shade300,
                      ),
                      child: isAnswered && isCorrect
                          ? Icon(Icons.check, color: Colors.white, size: 16)
                          : isSelected && isCorrect
                              ? Icon(Icons.check, color: Colors.white, size: 16)
                              : isSelected && !isCorrect
                                  ? Icon(Icons.close, color: Colors.white, size: 16)
                                  : Icon(Icons.radio_button_unchecked, color: Colors.grey.shade600, size: 16),
                    ),
                    SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        option.sentence,
                        style: TextStyle(
                          fontSize: 18,
                          color: textColor,
                          fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildMultipleSelection(QuizSentence sentence, QuizState quizState) {
    return ListView.builder(
      itemCount: sentence.options.length,
      itemBuilder: (context, index) {
        final option = sentence.options[index];
        final isSelected = ref.read(quizProvider.notifier).isOptionSelected(index);
        final isAnswered = quizState.isAnswered;
        final isCorrect = ref.read(quizProvider.notifier).isOptionCorrect(index);

        Color backgroundColor = Colors.white;
        Color borderColor = Colors.grey.shade300;
        Color textColor = Colors.grey.shade800;

        if (isAnswered) {
          if (isCorrect) {
            backgroundColor = Colors.green.shade50;
            borderColor = Colors.green.shade300;
            textColor = Colors.green.shade800;
          } else if (isSelected) {
            backgroundColor = Colors.red.shade50;
            borderColor = Colors.red.shade300;
            textColor = Colors.red.shade800;
          }
        } else if (isSelected) {
          backgroundColor = Colors.blue.shade50;
          borderColor = Colors.blue.shade300;
          textColor = Colors.blue.shade800;
        }

        return Container(
          margin: EdgeInsets.only(bottom: 12),
          child: Material(
            color: Colors.transparent,
            child: InkWell(
              onTap: isAnswered ? null : () {
                ref.read(quizProvider.notifier).toggleOption(index);
              },
              borderRadius: BorderRadius.circular(12),
              child: Container(
                padding: EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: backgroundColor,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: borderColor),
                ),
                child: Row(
                  children: [
                    Checkbox(
                      value: isSelected,
                      onChanged: isAnswered ? null : (_) {
                        ref.read(quizProvider.notifier).toggleOption(index);
                      },
                    ),
                    SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        option.sentence,
                        style: TextStyle(
                          fontSize: 18,
                          color: textColor,
                          fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildBottomButton(QuizSentence sentence, QuizState quizState) {
    final isExplanation = sentence.questionType == QuizQuestionType.explanation;
    final isWordSearch = sentence.questionType == QuizQuestionType.wordSearch;
    final isMultiple = sentence.questionType == QuizQuestionType.multipleChoice;

    if (!quizState.isAnswered && (isExplanation || isMultiple || isWordSearch)) {
      return SizedBox(
        width: double.infinity,
        child: ElevatedButton(
          onPressed: () {
            ref.read(quizProvider.notifier).submitAnswer();
          },
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.blue.shade600,
            foregroundColor: Colors.white,
            padding: EdgeInsets.symmetric(vertical: 16),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
          child: Text(
            (isExplanation || isWordSearch) ? 'Continue' : 'Check Answer',
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
          ),
        ),
      );
    }

    if (quizState.isAnswered) {
      return SizedBox(
        width: double.infinity,
        child: ElevatedButton(
          onPressed: () async {
            if (quizState.isLastQuestion) {
              await ref.read(quizProvider.notifier).saveResults();
              _showQuizSummary(context, quizState);
            } else {
              ref.read(quizProvider.notifier).nextQuestion();
              if (widget.autoPlaySound) {
                Future.delayed(Duration(milliseconds: 500), () {
                  if (mounted) {
                    ref.read(quizProvider.notifier).playAudio(normal: true);
                  }
                });
              }
            }
          },
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.blue.shade600,
            foregroundColor: Colors.white,
            padding: EdgeInsets.symmetric(vertical: 16),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
          child: Text(
            quizState.isLastQuestion ? 'Finish Quiz' : 'Next Question',
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
          ),
        ),
      );
    }

    // Default spacing placeholder
    return const SizedBox(height: 8);
  }

  void _showQuizSummary(BuildContext context, QuizState quizState) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Quiz Completed!'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Total Questions: ${quizState.totalQuestions}'),
              Text('Correct Answers: ${quizState.correctAnswers.length}'),
              Text('Wrong Answers: ${quizState.wrongAnswers.length}'),
              Text('Accuracy: ${quizState.accuracy.toStringAsFixed(1)}%'),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
                Navigator.of(context).pop(); // Go back to previous page
              },
              child: Text('Done'),
            ),
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
                ref.read(quizProvider.notifier).loadQuiz(); // Start new quiz
              },
              child: Text('New Quiz'),
            ),
          ],
        );
      },
    );
  }
} 