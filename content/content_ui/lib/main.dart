import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Alphabet Learning Challenges',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const AlphabetLearningPage(),
    );
  }
}

class AlphabetLearningPage extends StatefulWidget {
  const AlphabetLearningPage({Key? key}) : super(key: key);

  @override
  State<AlphabetLearningPage> createState() => _AlphabetLearningPageState();
}

class _AlphabetLearningPageState extends State<AlphabetLearningPage> {
  int _selectedTab = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Alphabet Learning Challenges'),
      ),
      body: IndexedStack(
        index: _selectedTab,
        children: const [
          ReadingContextGame(),
          LetterTransformationJourney(),
          MemoryCardPairsGame(),
          KanjiStrokeOrderWidget(),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedTab,
        onTap: (index) => setState(() => _selectedTab = index),
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.abc),
            label: 'Reading Context',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.transform),
            label: 'Letter Forms',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.cards),
            label: 'Memory Cards',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.edit),
            label: 'Stroke Order',
          ),
        ],
      ),
    );
  }
}

// 1. READING CONTEXT GAME - For Kanji with multiple readings
class ReadingContextGame extends StatefulWidget {
  const ReadingContextGame({Key? key}) : super(key: key);

  @override
  State<ReadingContextGame> createState() => _ReadingContextGameState();
}

class _ReadingContextGameState extends State<ReadingContextGame> {
  final List<Map<String, String>> _challenges = [
    {
      'sentence': '私は毎日学校に行きます。',
      'target': '行',
      'correct': 'いき',
      'options': 'いき|ぎょう|こう',
    },
    {
      'sentence': '先生は本を読んでいます。',
      'target': '先',
      'correct': 'せん',
      'options': 'せん|さき|まず',
    },
    {
      'sentence': '生まれたばかりの赤ちゃん。',
      'target': '生',
      'correct': 'うま',
      'options': 'うま|い|せい',
    },
  ];

  int _currentIndex = 0;
  int _score = 0;
  int? _selectedAnswer;

  void _checkAnswer() {
    final correct = _challenges[_currentIndex]['correct'];
    final options = _challenges[_currentIndex]['options']!.split('|');
    final isCorrect = options[_selectedAnswer!] == correct;

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(isCorrect ? '✓ Correct!' : '✗ Incorrect'),
        content: Text(isCorrect
            ? 'The reading "$correct" is correct in this context!'
            : 'The correct reading is "$correct". Context matters!'),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              if (isCorrect) {
                setState(() => _score++);
              }
              if (_currentIndex < _challenges.length - 1) {
                setState(() {
                  _currentIndex++;
                  _selectedAnswer = null;
                });
              } else {
                _showGameOver();
              }
            },
            child: const Text('Next'),
          ),
        ],
      ),
    );
  }

  void _showGameOver() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Game Over'),
        content: Text('Score: $_score/${_challenges.length}'),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              setState(() {
                _currentIndex = 0;
                _score = 0;
                _selectedAnswer = null;
              });
            },
            child: const Text('Play Again'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final challenge = _challenges[_currentIndex];
    final options = challenge['options']!.split('|');

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          LinearProgressIndicator(
            value: (_currentIndex + 1) / _challenges.length,
          ),
          const SizedBox(height: 20),
          Text(
            'Question ${_currentIndex + 1}/${_challenges.length}',
            style: Theme.of(context).textTheme.titleSmall,
          ),
          const SizedBox(height: 20),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'What is the reading of the highlighted Kanji in this context?',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 16),
                  Text.rich(
                    TextSpan(
                      children: challenge['sentence']!.split('').map((char) {
                        return TextSpan(
                          text: char,
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: char == challenge['target']
                                ? FontWeight.bold
                                : FontWeight.normal,
                            color: char == challenge['target']
                                ? Colors.red
                                : Colors.black,
                            backgroundColor: char == challenge['target']
                                ? Colors.yellow[200]
                                : null,
                          ),
                        );
                      }).toList(),
                    ),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          Column(
            children: List.generate(
              options.length,
              (index) => Padding(
                padding: const EdgeInsets.only(bottom: 12),
                child: ElevatedButton(
                  onPressed: () => setState(() => _selectedAnswer = index),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: _selectedAnswer == index
                        ? Colors.blue
                        : Colors.grey[300],
                    foregroundColor:
                        _selectedAnswer == index ? Colors.white : Colors.black,
                    minimumSize: const Size(double.infinity, 50),
                  ),
                  child: Text(
                    options[index],
                    style: const TextStyle(fontSize: 16),
                  ),
                ),
              ),
            ),
          ),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: _selectedAnswer != null ? _checkAnswer : null,
            style: ElevatedButton.styleFrom(
              minimumSize: const Size(double.infinity, 50),
            ),
            child: const Text('Check Answer'),
          ),
        ],
      ),
    );
  }
}

// 2. LETTER TRANSFORMATION JOURNEY - For Arabic letter forms
class LetterTransformationJourney extends StatefulWidget {
  const LetterTransformationJourney({Key? key}) : super(key: key);

  @override
  State<LetterTransformationJourney> createState() =>
      _LetterTransformationJourneyState();
}

class _LetterTransformationJourneyState
    extends State<LetterTransformationJourney>
    with SingleTickerProviderStateMixin {
  late AnimationController _animationController;
  final List<Map<String, dynamic>> _letters = [
    {
      'letter': 'ب',
      'isolated': 'ب',
      'initial': 'بـ',
      'medial': 'ـبـ',
      'final': 'ـب',
      'name': 'Ba',
      'word': 'كتب',
      'positions': ['isolated', 'final', 'medial', 'initial'],
    },
    {
      'letter': 'ك',
      'isolated': 'ك',
      'initial': 'كـ',
      'medial': 'ـكـ',
      'final': 'ـك',
      'name': 'Kaf',
      'word': 'كتاب',
      'positions': ['initial', 'medial', 'final'],
    },
  ];

  int _currentLetterIndex = 0;
  int _currentPositionIndex = 0;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 500),
      vsync: this,
    );
    _animationController.forward();
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  void _nextPosition() {
    final letter = _letters[_currentLetterIndex];
    if (_currentPositionIndex < letter['positions'].length - 1) {
      setState(() => _currentPositionIndex++);
      _animationController.reset();
      _animationController.forward();
    } else if (_currentLetterIndex < _letters.length - 1) {
      setState(() {
        _currentLetterIndex++;
        _currentPositionIndex = 0;
      });
      _animationController.reset();
      _animationController.forward();
    }
  }

  @override
  Widget build(BuildContext context) {
    final letter = _letters[_currentLetterIndex];
    final positions = letter['positions'] as List<String>;
    final currentPosition = positions[_currentPositionIndex];
    final formMap = {
      'isolated': letter['isolated'],
      'initial': letter['initial'],
      'medial': letter['medial'],
      'final': letter['final'],
    };

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          LinearProgressIndicator(
            value: (_currentLetterIndex + 1) / _letters.length,
          ),
          const SizedBox(height: 20),
          Text(
            'Letter ${_currentLetterIndex + 1}: ${letter['name']} (${letter['letter']})',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 30),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  const Text('Current Position:'),
                  const SizedBox(height: 12),
                  ScaleTransition(
                    scale: Tween<double>(begin: 0.5, end: 1.0)
                        .animate(_animationController),
                    child: Text(
                      formMap[currentPosition] ?? '',
                      style: const TextStyle(fontSize: 80),
                      textDirection: TextDirection.rtl,
                    ),
                  ),
                  const SizedBox(height: 20),
                  Text(
                    currentPosition.toUpperCase(),
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.blue[700],
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          const Text('All Forms:'),
          const SizedBox(height: 12),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildFormBox('Isolated', letter['isolated']),
              _buildFormBox('Initial', letter['initial']),
              _buildFormBox('Medial', letter['medial']),
              _buildFormBox('Final', letter['final']),
            ],
          ),
          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: _nextPosition,
            style: ElevatedButton.styleFrom(
              minimumSize: const Size(double.infinity, 50),
            ),
            child: Text(
              _currentLetterIndex == _letters.length - 1 &&
                      _currentPositionIndex == (_letters[_currentLetterIndex]['positions'] as List).length - 1
                  ? 'Complete'
                  : 'Next Form',
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFormBox(String label, String form) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            border: Border.all(color: Colors.grey),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Text(
            form,
            style: const TextStyle(fontSize: 32),
            textDirection: TextDirection.rtl,
          ),
        ),
        const SizedBox(height: 8),
        Text(
          label,
          style: const TextStyle(fontSize: 12),
        ),
      ],
    );
  }
}

// 3. MEMORY CARD PAIRS GAME
class MemoryCardPairsGame extends StatefulWidget {
  const MemoryCardPairsGame({Key? key}) : super(key: key);

  @override
  State<MemoryCardPairsGame> createState() => _MemoryCardPairsGameState();
}

class _MemoryCardPairsGameState extends State<MemoryCardPairsGame> {
  final List<Map<String, String>> _pairs = [
    {'id': '1a', 'pair': '1', 'content': '生', 'type': 'kanji'},
    {'id': '1b', 'pair': '1', 'content': 'い', 'type': 'hiragana'},
    {'id': '2a', 'pair': '2', 'content': 'ب', 'type': 'arabic'},
    {'id': '2b', 'pair': '2', 'content': 'ـب', 'type': 'arabic_final'},
    {'id': '3a', 'pair': '3', 'content': '水', 'type': 'kanji'},
    {'id': '3b', 'pair': '3', 'content': 'みず', 'type': 'hiragana'},
    {'id': '4a', 'pair': '4', 'content': 'ك', 'type': 'arabic'},
    {'id': '4b', 'pair': '4', 'content': 'ـك', 'type': 'arabic_final'},
  ];

  late List<Map<String, dynamic>> _gameCards;
  List<String> _flipped = [];
  List<String> _matched = [];
  int _moves = 0;

  @override
  void initState() {
    super.initState();
    _initializeGame();
  }

  void _initializeGame() {
    _gameCards = _pairs.map((pair) => {...pair, 'flipped': false}).toList();
    _gameCards.shuffle();
    _flipped = [];
    _matched = [];
    _moves = 0;
  }

  void _toggleCard(int index) {
    if (_matched.contains(_gameCards[index]['id']) ||
        _flipped.contains(_gameCards[index]['id'])) {
      return;
    }

    setState(() {
      _flipped.add(_gameCards[index]['id']);
    });

    if (_flipped.length == 2) {
      _checkMatch();
    }
  }

  void _checkMatch() {
    final card1 = _gameCards.firstWhere(
        (card) => card['id'] == _flipped[0]);
    final card2 = _gameCards.firstWhere(
        (card) => card['id'] == _flipped[1]);

    setState(() => _moves++);

    if (card1['pair'] == card2['pair']) {
      setState(() {
        _matched.addAll(_flipped);
        _flipped.clear();
      });

      if (_matched.length == _gameCards.length) {
        _showGameOver();
      }
    } else {
      Future.delayed(const Duration(milliseconds: 800), () {
        setState(() => _flipped.clear());
      });
    }
  }

  void _showGameOver() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('🎉 You Won!'),
        content: Text('Completed in $_moves moves'),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              setState(() => _initializeGame());
            },
            child: const Text('Play Again'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('Pairs: ${_matched.length ~/ 2}/${_pairs.length}'),
              Text('Moves: $_moves'),
            ],
          ),
          const SizedBox(height: 20),
          GridView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 4,
              childAspectRatio: 1,
              mainAxisSpacing: 8,
              crossAxisSpacing: 8,
            ),
            itemCount: _gameCards.length,
            itemBuilder: (context, index) {
              final card = _gameCards[index];
              final isFlipped = _flipped.contains(card['id']);
              final isMatched = _matched.contains(card['id']);

              return GestureDetector(
                onTap: isMatched ? null : () => _toggleCard(index),
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 300),
                  decoration: BoxDecoration(
                    color: isFlipped || isMatched
                        ? Colors.blue[100]
                        : Colors.blue[300],
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(
                      color: isMatched ? Colors.green : Colors.blue,
                      width: isMatched ? 3 : 1,
                    ),
                  ),
                  child: Center(
                    child: isFlipped || isMatched
                        ? Text(
                            card['content'],
                            style: const TextStyle(
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                            ),
                            textDirection: TextDirection.rtl,
                          )
                        : const Icon(Icons.help),
                  ),
                );
              });
            },
          ),
        ],
      ),
    );
  }
}

// 4. KANJI STROKE ORDER WIDGET
class KanjiStrokeOrderWidget extends StatefulWidget {
  const KanjiStrokeOrderWidget({Key? key}) : super(key: key);

  @override
  State<KanjiStrokeOrderWidget> createState() => _KanjiStrokeOrderWidgetState();
}

class _KanjiStrokeOrderWidgetState extends State<KanjiStrokeOrderWidget>
    with SingleTickerProviderStateMixin {
  final List<Map<String, dynamic>> _kanji = [
    {
      'character': '火',
      'meaning': 'Fire',
      'strokes': 4,
      'description': 'Top to bottom, left to right',
    },
    {
      'character': '木',
      'meaning': 'Tree',
      'strokes': 4,
      'description': 'Vertical line first, then branches',
    },
    {
      'character': '人',
      'meaning': 'Person',
      'strokes': 2,
      'description': 'Left diagonal, then right diagonal',
    },
  ];

  int _currentIndex = 0;
  late AnimationController _animationController;
  int _currentStroke = 0;
  bool _showAnswer = false;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
  }

  void _playAnimation() {
    _animationController.reset();
    _animationController.forward();
  }

  void _nextStroke() {
    if (_currentStroke < _kanji[_currentIndex]['strokes'] - 1) {
      setState(() => _currentStroke++);
      _playAnimation();
    }
  }

  void _nextKanji() {
    if (_currentIndex < _kanji.length - 1) {
      setState(() {
        _currentIndex++;
        _currentStroke = 0;
        _showAnswer = false;
      });
      _playAnimation();
    }
  }

  @override
  Widget build(BuildContext context) {
    final kanji = _kanji[_currentIndex];

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          LinearProgressIndicator(
            value: (_currentIndex + 1) / _kanji.length,
          ),
          const SizedBox(height: 20),
          Text(
            'Kanji ${_currentIndex + 1}/${_kanji.length}',
            style: Theme.of(context).textTheme.titleSmall,
          ),
          const SizedBox(height: 20),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  Text(
                    kanji['character'],
                    style: const TextStyle(fontSize: 120),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    '${kanji['meaning']} • ${kanji['strokes']} strokes',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Stroke Order:',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  Text('Stroke ${_currentStroke + 1}/${kanji['strokes']}'),
                  const SizedBox(height: 12),
                  ScaleTransition(
                    scale: Tween<double>(begin: 0.8, end: 1.0)
                        .animate(_animationController),
                    child: Container(
                      width: double.infinity,
                      height: 150,
                      decoration: BoxDecoration(
                        border: Border.all(color: Colors.grey),
                        borderRadius: BorderRadius.circular(8),
                        color: Colors.grey[50],
                      ),
                      child: Center(
                        child: Text(
                          '${_currentStroke + 1}',
                          style: const TextStyle(
                            fontSize: 60,
                            fontWeight: FontWeight.bold,
                            color: Colors.blue,
                          ),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),
                  Text(kanji['description']),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          Row(
            children: [
              Expanded(
                child: ElevatedButton(
                  onPressed: _currentStroke > 0
                      ? () => setState(() => _currentStroke--)
                      : null,
                  child: const Text('Previous'),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: ElevatedButton(
                  onPressed: _nextStroke,
                  child: const Text('Next Stroke'),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          ElevatedButton(
            onPressed: _nextKanji,
            style: ElevatedButton.styleFrom(
              minimumSize: const Size(double.infinity, 50),
            ),
            child: Text(
              _currentIndex == _kanji.length - 1 ? 'Complete' : 'Next Kanji',
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }
}