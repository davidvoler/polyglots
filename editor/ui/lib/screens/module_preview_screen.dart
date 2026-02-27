import 'package:flutter/material.dart';
import '../services/course_generation_service.dart';

// ─────────────────────────────────────────────────────────
// Data types used to pass module data from EditorFlowScreen
// ─────────────────────────────────────────────────────────

class WordExercisesForModule {
  final String word;
  final List<GeneratedExercisePreview> exercises;
  const WordExercisesForModule({required this.word, required this.exercises});
}

class ModuleSaveResult {
  final int courseId;
  final int lessonCount;
  final int exerciseCount;
  const ModuleSaveResult({
    required this.courseId,
    required this.lessonCount,
    required this.exerciseCount,
  });
}

// ─────────────────────────────────────────────────────────
// ModulePreviewScreen
// ─────────────────────────────────────────────────────────

class ModulePreviewScreen extends StatefulWidget {
  const ModulePreviewScreen({
    super.key,
    required this.lang,
    required this.toLang,
    required this.courseTitle,
    required this.courseDescription,
    required this.moduleNumber,
    required this.initialCourseId,
    required this.wordsPerModule,
    required this.wordExercises,
  });

  final String lang;
  final String toLang;
  final String courseTitle;
  final String courseDescription;
  final int moduleNumber;
  final int initialCourseId;
  final int wordsPerModule;
  final List<WordExercisesForModule> wordExercises;

  @override
  State<ModulePreviewScreen> createState() => _ModulePreviewScreenState();
}

class _ModulePreviewScreenState extends State<ModulePreviewScreen> {
  // For each word, track which exercise indices are selected (default: all)
  late final Map<String, Set<int>> _selected;
  // Duplicate keys (toSentenceId|exerciseType) that appear more than once across the module
  late final Set<String> _duplicateToIds;

  bool _saving = false;
  String? _saveError;

  @override
  void initState() {
    super.initState();
    // Pre-select all exercises
    _selected = {
      for (final we in widget.wordExercises)
        we.word: Set<int>.from(
          List.generate(we.exercises.length, (i) => i),
        ),
    };
    // Compute duplicate toSentenceIds
    _duplicateToIds = _computeDuplicates();
  }

  Set<String> _computeDuplicates() {
    final counts = <String, int>{};
    for (final we in widget.wordExercises) {
      for (final ex in we.exercises) {
        if (ex.toSentenceId > 0) {
          final key = '${ex.toSentenceId}|${ex.exerciseType}';
          counts[key] = (counts[key] ?? 0) + 1;
        }
      }
    }
    return counts.entries.where((e) => e.value > 1).map((e) => e.key).toSet();
  }

  int get _totalSelected =>
      _selected.values.fold(0, (sum, s) => sum + s.length);

  int get _totalExercises =>
      widget.wordExercises.fold(0, (sum, we) => sum + we.exercises.length);

  int get _duplicateCount => () {
        final seen = <String>{};
        var count = 0;
        for (final we in widget.wordExercises) {
          for (final ex in we.exercises) {
            final key = '${ex.toSentenceId}|${ex.exerciseType}';
            if (_duplicateToIds.contains(key)) {
              if (seen.contains(key)) {
                count++;
              } else {
                seen.add(key);
              }
            }
          }
        }
        return count;
      }();

  Future<void> _saveModule() async {
    setState(() { _saving = true; _saveError = null; });

    int savedCourseId = widget.initialCourseId;
    int savedModuleId = 0;
    int lessonCount = 0;
    int exerciseCount = 0;

    try {
      for (var i = 0; i < widget.wordExercises.length; i++) {
        final we = widget.wordExercises[i];
        final selectedIndices = _selected[we.word] ?? {};
        final exercises = selectedIndices
            .map((idx) => we.exercises[idx])
            .toList();

        final globalWordIndex = (widget.moduleNumber - 1) * widget.wordsPerModule + i;

        final res = await CourseGenerationService.saveLesson(
          courseId: savedCourseId,
          moduleId: savedModuleId,
          lang: widget.lang,
          toLang: widget.toLang,
          word: we.word,
          courseTitle: widget.courseTitle,
          courseDescription: widget.courseDescription,
          lessonsPerModule: widget.wordsPerModule,
          wordIndex: globalWordIndex,
          exercises: exercises,
        );

        // After first lesson, lock in courseId and moduleId for remaining words
        savedCourseId = res.courseId;
        if (savedModuleId == 0) savedModuleId = res.moduleId;

        lessonCount++;
        exerciseCount += exercises.length;
      }

      if (!mounted) return;
      Navigator.pop(
        context,
        ModuleSaveResult(
          courseId: savedCourseId,
          lessonCount: lessonCount,
          exerciseCount: exerciseCount,
        ),
      );
    } catch (e) {
      setState(() { _saving = false; _saveError = e.toString(); });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Module ${widget.moduleNumber} Preview'),
        elevation: 0,
      ),
      body: Column(children: [
        _buildSummaryBar(),
        if (_duplicateCount > 0) _buildDuplicateBanner(),
        if (_saveError != null)
          Container(
            width: double.infinity,
            color: Colors.red[50],
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Text(_saveError!, style: const TextStyle(color: Colors.red)),
          ),
        Expanded(child: _buildExerciseList()),
        _buildBottomBar(),
      ]),
    );
  }

  Widget _buildSummaryBar() {
    final wordCount = widget.wordExercises.length;
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      color: Colors.grey[100],
      child: Text(
        '$wordCount lesson${wordCount == 1 ? '' : 's'} · '
        '$_totalSelected / $_totalExercises exercises selected',
        style: const TextStyle(fontWeight: FontWeight.w600),
      ),
    );
  }

  Widget _buildDuplicateBanner() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      color: Colors.orange[50],
      child: Row(children: [
        Icon(Icons.warning_amber_rounded, color: Colors.orange[700], size: 18),
        const SizedBox(width: 8),
        Expanded(
          child: Text(
            '$_duplicateCount exercise${_duplicateCount == 1 ? '' : 's'} share a duplicate translation — '
            'review below.',
            style: TextStyle(color: Colors.orange[800], fontSize: 13),
          ),
        ),
      ]),
    );
  }

  Widget _buildExerciseList() {
    return ListView.builder(
      itemCount: widget.wordExercises.length,
      itemBuilder: (context, i) => _buildLessonSection(widget.wordExercises[i]),
    );
  }

  Widget _buildLessonSection(WordExercisesForModule we) {
    final selectedCount = (_selected[we.word] ?? {}).length;
    return ExpansionTile(
      initiallyExpanded: true,
      tilePadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 2),
      title: Row(children: [
        Text(we.word, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
        const SizedBox(width: 8),
        Text(
          '$selectedCount / ${we.exercises.length}',
          style: TextStyle(color: Colors.grey[600], fontSize: 12),
        ),
      ]),
      children: List.generate(we.exercises.length, (i) {
        final ex = we.exercises[i];
        return _buildExerciseRow(we.word, i, ex);
      }),
    );
  }

  Widget _buildExerciseRow(String word, int index, GeneratedExercisePreview ex) {
    final selected = _selected[word]?.contains(index) ?? false;
    final isDup = ex.toSentenceId > 0 && _duplicateToIds.contains('${ex.toSentenceId}|${ex.exerciseType}');

    return CheckboxListTile(
      dense: true,
      contentPadding: const EdgeInsets.symmetric(horizontal: 16),
      value: selected,
      onChanged: _saving
          ? null
          : (v) => setState(() {
                if (v == true) {
                  _selected[word]!.add(index);
                } else {
                  _selected[word]!.remove(index);
                }
              }),
      title: Row(children: [
        _typeBadge(ex.exerciseType),
        const SizedBox(width: 8),
        Expanded(
          child: Text(
            ex.sentence.isNotEmpty ? ex.sentence : ex.toSentence,
            style: const TextStyle(fontSize: 13),
            overflow: TextOverflow.ellipsis,
          ),
        ),
        if (isDup) ...[
          const SizedBox(width: 4),
          Tooltip(
            message: 'Duplicate translation',
            child: Icon(Icons.warning_amber_rounded, size: 14, color: Colors.orange[700]),
          ),
        ],
      ]),
      subtitle: _buildExerciseSubtitle(ex),
    );
  }

  Widget? _buildExerciseSubtitle(GeneratedExercisePreview ex) {
    final isIdentify = ex.exerciseType == 'identify_words_in_speech';
    final identifyWords = isIdentify ? ex.correctOptions : <String>[];
    final wrongOpts = isIdentify ? <String>[] : ex.wrongOptions;
    final hasContent = identifyWords.isNotEmpty || wrongOpts.isNotEmpty || ex.toSentence.isNotEmpty;
    if (!hasContent) return null;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        if (ex.toSentence.isNotEmpty)
          Text(
            ex.toSentence,
            style: TextStyle(fontSize: 11, color: Colors.grey[600]),
            overflow: TextOverflow.ellipsis,
          ),
        // Identify words: show words to identify with label
        if (identifyWords.isNotEmpty) ...[
          const SizedBox(height: 4),
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('identify: ', style: TextStyle(fontSize: 10, color: Colors.purple[400], fontWeight: FontWeight.w600)),
              Expanded(
                child: Wrap(
                  spacing: 4,
                  runSpacing: 3,
                  children: identifyWords.map((w) => _wordChip(w)).toList(),
                ),
              ),
            ],
          ),
        ],
        // Wrong options for single-choice
        if (wrongOpts.isNotEmpty) ...[
          const SizedBox(height: 4),
          Wrap(
            spacing: 4,
            runSpacing: 3,
            children: wrongOpts.map((opt) => _optionChip(opt, correct: false)).toList(),
          ),
        ],
      ],
    );
  }

  Widget _wordChip(String text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
      decoration: BoxDecoration(
        color: Colors.purple[50],
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: Colors.purple[200]!),
      ),
      child: Text(text, style: TextStyle(fontSize: 10, color: Colors.purple[700])),
    );
  }

  Widget _optionChip(String text, {required bool correct}) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
      decoration: BoxDecoration(
        color: correct ? Colors.green[50] : Colors.grey[100],
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: correct ? Colors.green[300]! : Colors.grey[300]!),
      ),
      child: Text(
        text,
        style: TextStyle(
          fontSize: 10,
          color: correct ? Colors.green[700] : Colors.grey[600],
        ),
      ),
    );
  }

  Widget _typeBadge(String exerciseType) {
    final label = _typeLabel(exerciseType);
    final color = _typeColor(exerciseType);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 2),
      decoration: BoxDecoration(
        color: color.withOpacity(0.15),
        borderRadius: BorderRadius.circular(3),
        border: Border.all(color: color.withOpacity(0.4)),
      ),
      child: Text(label, style: TextStyle(fontSize: 9, color: color, fontWeight: FontWeight.w600)),
    );
  }

  String _typeLabel(String type) {
    switch (type) {
      case 'sentence_single_choice': return 'choice';
      case 'identify_words_in_speech': return 'identify';
      case 'translate_sentence': return 'translate';
      case 'fill_in_blank': return 'fill';
      default: return type.length > 8 ? type.substring(0, 8) : type;
    }
  }

  Color _typeColor(String type) {
    switch (type) {
      case 'sentence_single_choice': return Colors.blue;
      case 'identify_words_in_speech': return Colors.purple;
      case 'translate_sentence': return Colors.teal;
      case 'fill_in_blank': return Colors.orange;
      default: return Colors.grey;
    }
  }

  Widget _buildBottomBar() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: Theme.of(context).scaffoldBackgroundColor,
        border: Border(top: BorderSide(color: Colors.grey[200]!)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          TextButton.icon(
            onPressed: _saving ? null : () => Navigator.pop(context, null),
            icon: const Icon(Icons.arrow_back, size: 16),
            label: const Text('Back to words'),
          ),
          ElevatedButton.icon(
            onPressed: _saving || _totalSelected == 0 ? null : _saveModule,
            icon: _saving
                ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                : const Icon(Icons.save_alt, size: 16),
            label: Text(_saving ? 'Saving...' : 'Save Module ${widget.moduleNumber} →'),
          ),
        ],
      ),
    );
  }
}
