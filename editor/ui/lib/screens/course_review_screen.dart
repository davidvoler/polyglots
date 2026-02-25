import 'package:flutter/material.dart';
import '../services/course_generation_service.dart';

/// Full course tree for post-generation editing.
/// Shows Module > Lesson > Exercises; user can uncheck exercises to delete them.
class CourseReviewScreen extends StatefulWidget {
  const CourseReviewScreen({super.key, required this.courseId});
  final int courseId;

  @override
  State<CourseReviewScreen> createState() => _CourseReviewScreenState();
}

class _CourseReviewScreenState extends State<CourseReviewScreen> {
  CourseDetail? _course;
  bool _loading = true;
  String? _loadError;

  // Set of exercise IDs that the user has UNchecked (to be deleted on save)
  final Set<int> _unchecked = {};
  bool _saving = false;
  String? _saveError;

  @override
  void initState() {
    super.initState();
    _loadCourse();
  }

  Future<void> _loadCourse() async {
    setState(() { _loading = true; _loadError = null; });
    try {
      final course = await CourseGenerationService.getCourseDetail(widget.courseId);
      if (mounted) setState(() { _course = course; _loading = false; });
    } catch (e) {
      if (mounted) setState(() { _loadError = e.toString(); _loading = false; });
    }
  }

  int get _totalExercises => _course?.modules
      .expand((m) => m.lessons)
      .expand((l) => l.exercises)
      .length ?? 0;

  int get _uncheckedCount => _unchecked.length;

  Future<void> _saveChanges() async {
    if (_unchecked.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('No changes to save.')),
      );
      return;
    }
    setState(() { _saving = true; _saveError = null; });
    try {
      final deleted = await CourseGenerationService.deleteExercises(_unchecked.toList());
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Deleted $deleted exercise${deleted == 1 ? '' : 's'}.')),
      );
      // Reload to show updated state
      setState(() { _unchecked.clear(); _saving = false; });
      _loadCourse();
    } catch (e) {
      if (mounted) setState(() { _saveError = e.toString(); _saving = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_course != null ? _course!.title : 'Course Review'),
        elevation: 0,
        actions: [
          if (_uncheckedCount > 0)
            Padding(
              padding: const EdgeInsets.only(right: 8),
              child: Center(
                child: Text(
                  '$_uncheckedCount to delete',
                  style: const TextStyle(color: Colors.red, fontSize: 13),
                ),
              ),
            ),
          TextButton.icon(
            onPressed: _saving ? null : _saveChanges,
            icon: _saving
                ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                : const Icon(Icons.save_outlined, size: 18),
            label: const Text('Save changes'),
          ),
        ],
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_loading) return const Center(child: CircularProgressIndicator());
    if (_loadError != null) {
      return Center(
        child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
          Text(_loadError!, textAlign: TextAlign.center, style: const TextStyle(color: Colors.red)),
          const SizedBox(height: 16),
          ElevatedButton(onPressed: _loadCourse, child: const Text('Retry')),
        ]),
      );
    }
    if (_course == null) return const SizedBox.shrink();

    return Column(children: [
      _buildCourseSummaryBar(),
      if (_saveError != null)
        Container(
          width: double.infinity,
          color: Colors.red[50],
          padding: const EdgeInsets.all(8),
          child: Text(_saveError!, style: const TextStyle(color: Colors.red)),
        ),
      Expanded(
        child: ListView.builder(
          itemCount: _course!.modules.length,
          itemBuilder: (ctx, i) => _buildModuleSection(_course!.modules[i], i),
        ),
      ),
    ]);
  }

  Widget _buildCourseSummaryBar() {
    final modules = _course!.modules.length;
    final lessons = _course!.modules.expand((m) => m.lessons).length;
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      color: Colors.grey[100],
      child: Text(
        '$modules module${modules == 1 ? '' : 's'} · '
        '$lessons lesson${lessons == 1 ? '' : 's'} · '
        '$_totalExercises exercise${_totalExercises == 1 ? '' : 's'}'
        '${_uncheckedCount > 0 ? ' ($_uncheckedCount marked for deletion)' : ''}',
        style: const TextStyle(fontWeight: FontWeight.w600),
      ),
    );
  }

  Widget _buildModuleSection(ModuleDetail module, int moduleIdx) {
    final exerciseCount = module.lessons.expand((l) => l.exercises).length;
    final uncheckedInModule =
        module.lessons.expand((l) => l.exercises).where((e) => _unchecked.contains(e.id)).length;
    return ExpansionTile(
      initiallyExpanded: true,
      tilePadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      backgroundColor: Colors.deepPurple[50],
      title: Row(children: [
        Text(
          module.title.isEmpty ? 'Module ${moduleIdx + 1}' : module.title,
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
        ),
        const SizedBox(width: 8),
        Text(
          '${module.lessons.length} lessons · $exerciseCount exercises'
          '${uncheckedInModule > 0 ? ' · $uncheckedInModule to delete' : ''}',
          style: TextStyle(color: Colors.grey[600], fontSize: 12),
        ),
      ]),
      children: module.lessons
          .map((lesson) => _buildLessonSection(lesson))
          .toList(),
    );
  }

  Widget _buildLessonSection(LessonDetail lesson) {
    final uncheckedInLesson =
        lesson.exercises.where((e) => _unchecked.contains(e.id)).length;
    return ExpansionTile(
      initiallyExpanded: false,
      tilePadding: const EdgeInsets.symmetric(horizontal: 24, vertical: 2),
      title: Row(children: [
        Text(lesson.title, style: const TextStyle(fontWeight: FontWeight.w600)),
        const SizedBox(width: 8),
        Text(
          '${lesson.exercises.length} exercises'
          '${uncheckedInLesson > 0 ? ' · $uncheckedInLesson to delete' : ''}',
          style: TextStyle(color: Colors.grey[600], fontSize: 12),
        ),
      ]),
      children: lesson.exercises
          .map((ex) => _buildExerciseRow(ex))
          .toList(),
    );
  }

  Widget _buildExerciseRow(ExerciseDetail ex) {
    final checked = !_unchecked.contains(ex.id);
    return CheckboxListTile(
      dense: true,
      contentPadding: const EdgeInsets.symmetric(horizontal: 32),
      value: checked,
      onChanged: _saving
          ? null
          : (v) => setState(() {
                if (v == true) {
                  _unchecked.remove(ex.id);
                } else {
                  _unchecked.add(ex.id);
                }
              }),
      title: Row(children: [
        _typeBadge(ex.exerciseType),
        const SizedBox(width: 8),
        Expanded(
          child: Text(
            ex.sentence.isNotEmpty ? ex.sentence : ex.toSentence,
            style: TextStyle(
              fontSize: 13,
              color: checked ? null : Colors.grey[400],
              decoration: checked ? null : TextDecoration.lineThrough,
            ),
            overflow: TextOverflow.ellipsis,
          ),
        ),
      ]),
      subtitle: ex.toSentence.isNotEmpty
          ? Text(
              ex.toSentence,
              style: TextStyle(
                fontSize: 11,
                color: checked ? Colors.grey[600] : Colors.grey[400],
                decoration: checked ? null : TextDecoration.lineThrough,
              ),
              overflow: TextOverflow.ellipsis,
            )
          : null,
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
      child: Text(
        label,
        style: TextStyle(fontSize: 9, color: color, fontWeight: FontWeight.w600),
      ),
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
}
