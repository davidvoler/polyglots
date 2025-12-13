"""
Pure Python Japanese Compound and Pattern Extractor
NO EXTERNAL DEPENDENCIES - Works on any Python 3.6+
Perfect when installation issues prevent using NLP libraries
"""

from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
import json
import re
from batch_tools.analyze_sentence.ja.translit import translit_single
from batch_tools.analyze_sentence.ja.ja_spacy import get_root

try:
    from fugashi import Tagger
    FUGASHI_AVAILABLE = True
except ImportError:
    FUGASHI_AVAILABLE = False




@dataclass
class Compound:
    """Detected compound expression"""
    text: str
    category: str
    meaning: str
    position: int


@dataclass
class Pattern:
    """Detected grammar pattern"""
    text: str
    pattern_type: str
    meaning: str
    position: int


class PureJapaneseAnalyzer:
    """
    Japanese text analyzer using only built-in Python
    NO external libraries needed
    """
    
    def __init__(self):
        self.compounds = self._load_compounds()
        self.particles = self._load_particles()
        self.patterns = self._load_patterns()
    
    def _load_compounds(self) -> Dict[str, Tuple[str, str]]:
        """
        Load compound expressions
        Format: {compound: (category, meaning)}
        """
        return {
            # Conjunctions
            'それで': ('conjunction', 'therefore/so'),
            'だから': ('conjunction', 'therefore/because'),
            'でも': ('conjunction', 'but/however'),
            'しかし': ('conjunction', 'however'),
            'けれども': ('conjunction', 'but/however'),
            'けれど': ('conjunction', 'but'),
            'けど': ('conjunction', 'but (casual)'),
            'そして': ('conjunction', 'and/then'),
            'また': ('conjunction', 'also/again'),
            'それから': ('conjunction', 'and then'),
            'すると': ('conjunction', 'then/thereupon'),
            'そこで': ('conjunction', 'so/therefore'),
            'ところが': ('conjunction', 'however/unexpectedly'),
            'なぜなら': ('conjunction', 'because'),
            'つまり': ('conjunction', 'in other words'),
            'ただし': ('conjunction', 'however/provided that'),
            'しかも': ('conjunction', 'moreover'),
            'そのうえ': ('conjunction', 'moreover'),
            'それに': ('conjunction', 'besides/moreover'),
            
            # Time expressions
            '今すぐ': ('time', 'right now'),
            'もうすぐ': ('time', 'soon'),
            'たったいま': ('time', 'just now'),
            'ついさっき': ('time', 'just a moment ago'),
            'さっき': ('time', 'a while ago'),
            'このあいだ': ('time', 'the other day'),
            'このまえ': ('time', 'last time'),
            'いつも': ('time', 'always'),
            'ときどき': ('time', 'sometimes'),
            'たまに': ('time', 'occasionally'),
            'とうとう': ('time', 'finally/at last'),
            'ようやく': ('time', 'finally/at last'),
            'やっと': ('time', 'at last/finally'),
            
            # Adverbs
            'ちょっと': ('adverb', 'a little/a bit'),
            'とても': ('adverb', 'very'),
            'すごく': ('adverb', 'very/extremely'),
            'かなり': ('adverb', 'quite/considerably'),
            'たいへん': ('adverb', 'very/extremely'),
            'わざわざ': ('adverb', 'expressly/specially'),
            'きっと': ('adverb', 'surely/certainly'),
            'たぶん': ('adverb', 'probably/perhaps'),
            'もちろん': ('adverb', 'of course'),
            'やはり': ('adverb', 'as expected/after all'),
            'やっぱり': ('adverb', 'as expected (casual)'),
            'さすが': ('adverb', 'as expected/admirable'),
            'なんと': ('adverb', 'what/how'),
            'まさか': ('adverb', 'surely not/no way'),
            'どうも': ('adverb', 'thanks/somehow'),
            'なんだか': ('adverb', 'somehow/for some reason'),
            
            # Transitions
            'ところで': ('transition', 'by the way'),
            'ちなみに': ('transition', 'by the way/incidentally'),
            'さて': ('transition', 'well/now'),
            'では': ('transition', 'well then'),
            'じゃあ': ('transition', 'well then (casual)'),
            'それじゃ': ('transition', 'well then'),
            'そういえば': ('transition', 'come to think of it'),
            'ともかく': ('transition', 'anyway'),
            'とにかく': ('transition', 'anyway/in any case'),
            
            # Additional words from provided list
            **self._load_additional_compounds()
        }
    
    def _load_additional_compounds(self) -> Dict[str, Tuple[str, str]]:
        """
        Load additional compound expressions from provided list
        Maps category abbreviations to full category names
        """
        # Category mapping from abbreviations to full names
        category_map = {
            'cp.': 'compound_pattern',
            'interj.': 'interjection',
            'adv.': 'adverb',
            'conj.': 'conjunction',
            'adn.': 'adnominal',
            'p.': 'particle',
            'pron.': 'pronoun',
            'n.': 'noun',
            'i-adj.': 'adjective',
            'na-adj.': 'adjective',
            'p. conj.': 'particle_conjunction',
            'p. case': 'particle_case',
            'p. disc.': 'particle_discourse',
            'suffix': 'suffix',
            'v.': 'verb',
        }
        
        # Raw data from user's list
        word_list = """ている、てる	cp. CONTINUATION
という、つう	cp. called, named
えー、ええ	interj. eh?, what?; well, yes
のです、んです	cp. ASSERTION (polite)
あの、あのう、あのー	interj. Excuse me; uh, eh, um, ah, er
まー、まあ	interj. Wow!, Oh my God!
その	adn. that
けれど	conj. though, although
から	p. case from
そう	adv. so, such
てしまう	cp. end up doing ...
それ	pron. that
とか	p. and; or
この	adn. this
のだ、んだ	cp. ASSERTION
これ	pron. this
もう	adv. already; soon; again
である	cp. COPULA (formal)
ので、んで	p. conj. as, because, since
こう	adv. so, like this
まで	p. to, till, until
たり	p. and
あー	interj. er, uh, um, hmm, ah, oh
やはり、やっぱり	adv. as (one) expected, still
など	p. and so on, etc.
として	cp. as
また	[1] adv. additionally, moreover [2] conj. again; too, and
ちょっと	adv. (just) a little, a bit
てくる	cp. go and ...
だけ	p. only, alone, merely
くらい、ぐらい	p. about, around
ではない	cp. it is not the case that ...
えーと	interj. well, let me see
ていく、てく	cp. go and ...
どう	adv. how, what
ため	n. for
すごい	i-adj. fantastic, wonderful; terrible
そこ	pron. there; then
ておる	cp. CONTINUATION (polite)
について	cp. about, concerning, as to
それで	conj. and then; so; that is why
てみる	cp. try ... ing
そして	conj. and, so
てくれる	cp. [do something as a favor]
ながら	p. conj. with, over, while
そんな	adn. that, such
おー	interj. Oh, Wow!
のではない、んではない	cp. it is not that ...
よく	adv. good, well; often
ても	p. conj. even if
うち	n. inside; of; before
より	p. case than; from
それから	conj. and then, after that, and
うー	interj. Woo, Oooh
みたい	na-adj. like
でも	conj. but, however
ここ	pron. here
とても、とっても	adv. very
いろいろ	adv., na-adj. various
まず	adv. first; anyway
によって	cp. by, because of; depend on, depending on
かもしれない	cp. perhaps, maybe
ほど	p. about; extent
しかし	conj. but, however
てくださる	cp. [do something as a favor (honorific)]
いつ	pron. when
どこ	pron. where
ただ	[1] conj. just [2] adv. only, just, merely
だから	conj. so, therefore, because
なんか	p. such as, like
まだ	n. yet, still
てもらう	cp. [receive a favor]
のである	cp. ASSERTION (formal)
いろんな	adn. various
かなり	adv. considerably, rather
しか	p. only, just, no more than
こんな	adn. such, like that
すぐ	adv. soon
あなた、あんた	pron. you
なんて	p. [expresses belittlement]
において	cp. at; in; on
あるいは	conj. or; perhaps, probably, maybe
もっと	adv. more
による	cp. be due to, be based on
ほとんど	adv. almost, nearly
あの	adn. that, those
ていただく	cp. [receive a favor (humble)]
ずっと	adv. all the time, for a long time
さらに	adv. again, still more, moreover
たくさん	adv. many, much
いー	interj. good, great
もちろん	adv. of course, needless to say
うん	interj. yes, yeah
すべて	n. everything, all
ておく	cp. do something in advance, in preparation for something
ばかり	p. only, just, almost
なぜ	adv. why
にとって	cp. for
なかなか	adv. very, quite; (not) easily
ことができる	cp. can, be able to
もし	adv. if, in case
あれ	pron. that
たぶん	adv. probably, perhaps, maybe
どんな	adn. what, what kind of
ことになる	cp. it happens that ... , it is decided that
どの	adn. which, what
こちら	pron. this place, here; this way; this
いわゆる	adn. what is called, what you call, so-called
により	cp. by; with; depending on
きれい	na-adj. beautiful, pretty; clean
ために	cp. for
おいしい	i-adj. delicious, tasty
または	conj. or
じゃ	conj. well, so, then
うまい	i-adj. delicious, tasty; good at
てある	cp. [describes a state resulting from someone's action]
における	cp. in
それぞれ	n. each
はず	n. ought to, should
なければいけない	cp. must, have to, need to
ちょうど	adv. just, exactly
ですから	conj. so, therefore
どんどん	adv. rapidly, fast, soon
とにかく	adv. anyway, regardless
まわり	n. circumference; surroundings, neighborhood, around
つまり	adv. in short, that is to say, after all
だんだん	adv. gradually, more and more, less and less
こそ	p. EMPHATIC
てもいい	cp. (I) don't mind if
しかも	conj. moreover, besides
でない	cp. COPULA (NEGATIVE)
すでに	adv. already, before
だめ	na-adj. useless, hopeless, impossible
といった	cp. like, such as
これら	pron. these
なければならない	cp. must
いや	interj. No
はい	interj. yes; all right
どうしても	adv. by all means, at any cost, no matter what, after all
のに	p. conj. although, though; in order to
つらい	i-adj. hard, difficult, painful
どちら	pron. where; which; who
ちゃんと	adv. exactly, regularly, properly
てほしい	cp. want /ask someone to do
でございます	cp. be (formal)
ずつ	p. each, ... by ...
ところが	conj. however
それでも	conj. but, still
はっきり	adv. clearly, certainly
のみ	p. only, merely
だが	conj. but, however
いずれ	[1] adv. anyway, sooner or later [2] pron. either
さえ	p. even; besides; if only
きっと	adv. surely, certainly
どうして	adv. why
なお	adv. more, still
ほしい	i-adj. want, desire
しっかり	adv. hard, tight
しばらく	adv. for a while, a minute, for a long time
いくら	adv. how much, however
どれ	pron. which
ものすごい	[1] i-adj. terrible [2] adv. terribly
せい	n. fault, cause for blame, because of
たまたま	adv. accidentally, by chance
ただし	conj. but, however, though
つもり	n. intention
びっくり（する）	[1] n. surprise [2] v. be surprised, be amazed
やっと	adv. at last
つつ	p. conj. while doing; though
ひどい	i-adj. cruel, serious, terrible
まあ	adv. Oh!, well, now
では	conj. then, well
てあげる	cp. do something for somebody
ことがある	cp. have done; there are sometimes
てやる	cp. do something for somebody/something
もと	n. under
おそらく	adv. probably, likely
きっかけ	n. opportunity, motive
ずいぶん	adv. very, pretty, quite
んと	interj. well
ゆっくり	adv. slowly, leisurely; plenty of time
したがって	conj. accordingly, consequently
（お）ばあさん	n. old lady; grandmother
きちんと	adv. precisely, accurately, neatly
そちら	pron. your place; there; you
ちなみに	conj. by the way, incidentally
おかしい	i-adj. funny, amusing
かしら	p. disc. I wonder
すなわち	conj. that is (to say), namely
だけれど	conj. despite, though
そば	n. side, beside
たまに	adv. occasionally, once in a while
もしくは	conj. or, otherwise
たび	n. every time
まさに	adv. exactly
むしろ	adv. rather, if anything
まるで	adv. just like, quite
こともある	cp. sometimes, can be
てはいけない、ちゃいけない	cp. must not, should not
ほぼ	adv. about, nearly, almost
やら	p. and, or
おなか	n. stomach, belly
それら	pron. those, these, they
さすが	adv. as might be expected, as one would expect
なし	n. without, no
さて	conj. well, now
いかに	adv. how, in what way
ありがとう	interj. thank you
かつ	conj. besides, also, as well
いきなり	adv. suddenly, without notice
いまだ	adv. still, yet, so far
ああ	adv. like that
やがて	adv. soon, before long, after all
ではありません、じゃありません	cp. not, no
かつて	adv. once, before, ever, former
ごみ	n. rubbish, garbage, trash
わずか	[1] na-adj. a few, a little, a bit [2] adv. only
それでは、それじゃ	conj. then, well, so
とともに	cp. together with, with
うそ	n. lie, falsehood
ものの	p. conj. but, although, despite
おかげ	n. thanks, virtue
としても	cp. assuming, even if
あんな	adn. such, like that
まだまだ	adv. still, still more
よろしく	adv. well, properly, best regards
それなり	n. in itself, as it is, in its way
なるべく	adv. as ... as possible, if possible
ようやく	adv. at last, gradually, barely
せっかく	adv. with effort, take the trouble to
あそこ	pron. there, over there
あらゆる	adn. every, all, any
にしても	cp. even if, even though
によると	cp. according to
ますます	adv. more and more, increasingly
（お）じいさん	n. grandfather
しようがない、しょうがない	i-adj. it can't be helped, nothing can be done
なり	p. or, whether or not
でもって	cp. by, with, in
あくまで	adv. only, to the last
つい	adv. without thinking, unintentionally
それとも	conj. or
ついに	adv. at last, finally
そもそも	adv., n. in the first place
たとえ	adv. even if
すっかり	adv. entirely, completely
なんら	adv. nothing
にて	p. case by; in; at
CD (CD)	n. CD, compact disk
さあ	interj. come on, now, well
だけでなく	cp. not only
がん	n. cancer.
いよいよ	adv. finally, at last
そこで	conj. so
すら	p. even
すみません	interj. Thank you; I am sorry; Excuse me
やや	adv. a little, slightly
いかが	na-adj. how
わざわざ	adv. take the trouble, especially
じっと（する）	adv., v. still, fixedly, intently
きり	p. only
すると	conj. then, if so
けんか（する）	[1] n. fight, quarrel [2] v. fight, quarrel
ともかく	adv. in any case, anyway
そろそろ	adv. soon; slowly
けが（する）	[1] n. injury [2] v. hurt, injure
ほんの	adn. just, nothing but, only
きつい	i-adj. tight; hard, severe; strong
どうぞ	adv. please
をもって	cp. by; with; as of
ふと	adv. casually; suddenly
かわいそう	na-adj. pitiful, miserable
なくてはいけない	cp. have to, must
さっき	adv., n. a little while ago
ごく	adv. very
CM (CM)	n. commercial
うわさ（する）	[1] n. gossip, rumor [2] v. talk about
もの	p. because
たいした	adn. not big, not much; great, quite
どころ	p. far from, on the contrary, can't even
あっ	interj. Ah!, Oh!, Hey!
おそれ	n. fear, danger
あえて	adv. dare
いったん	adv. once; for a moment
にあたって	cp. at the time of
まさか	[1] adv. surely not, cannot possibly [2] n. the worst
ごめんなさい	interj. I'm sorry, Excuse me
こっち	pron. here; this; I; we
たっぷり	[1] adv. full, plenty [2] n. fullness
とも	p. all, both
とたん	n. as soon as
かえって	adv. on the contrary, rather
いわば	adv. so to speak, as it were
ありがたい	i-adj. kind, welcome
なるほど	adv. I see, indeed, to be sure, of course
まっすぐ	[1] n. straight, direct [2] adv. honest
よろしい	i-adj. all right, good, may (I) (formal)
りんご	n. apple
まずい	i-adj. not taste good; awkward
しかたない	i-adj. It can't be helped, be beyond any help, I can't help ...
つつある	cp. be in the process of doing, be doing
いざ	adv. when one comes to, if compelled
たって	p. even if
なので	conj. because, as
ところで	conj. by the way, well
うるさい	i-adj. noisy; annoying
まるい	i-adj. round, circular
おしゃれ	na-adj. fashionable, smart
わし	n. I (used by old men)
だって	conj. because, but
もっとも	conj. though, although
あらかじめ	adv. beforehand, in advance
てはならない	cp. must not, should not
しかない	cp. can't but, can only, have no choice
あちらこちら	pron. here and there
しばしば	adv. always, often
のんびり	adv. tranquil, leisurely, easygoing
によれば	cp. according to, ... say
もはや	adv. now, already; not ... any longer
によっては	cp. depending on
ひたすら	adv. determinedly, earnestly
にわたって	cp. throughout, over a period of
ぱっと	adv. suddenly
いじめ	n. bullying
しょっちゅう	adv. often, always
ないし	conj. or, otherwise
とうとう	adv. finally
このごろ	n. these days
JR (JR)	n. Japan Railways (JR)
よほど、よっぽど	adv. very, greatly
どうせ	adv. anyway
ては	p., conj. alternately do ... and ...
どっち	pron. which
なにより	adv. above all, chiefly, more than anything
そっと	adv. softly, lightly
おい	interj. hey
とんでも	adv. unexpected; outrageous, very offensive
NHK (NHK)	n. Nihon Hoso Kyokai (Japan Broadcasting Corporation)
やりとり	n. exchange, interchange
としたら	p. conj. if so
はあ	interj. oh, Oh boy, Oh dear
にもかかわらず	p. conj. in spite of, though, despite
IT (IT)	n. IT
あちら	pron. that way; that place, there; that
ふさわしい	i-adj. suitable, appropriate
といっても	p. even though
つながり	n. connection, relation
ゆえ	n. reason; therefore
PC (PC)	n. personal computer
おまけ	n. addition, free gift
をはじめ	p. starting with ... , including
ついで	n. on one's way, along the way
たった	adv. just, only
およそ	adv. around, about
ぴったり	adv. tight; exactly
にんにく	n. garlic
ですが	conj. but, however
ほら	interj. Look!
いっぺん	n. at the same time; altogether
どなた	pron. who
やばい	i-adj. risky, chancy
にしろ	p. conj. even if
まして	adv. much less, much more
すっきり（する）	adv., v. feel refreshed
あいつ	pron. that fellow; that thing
こいつ	pron. this fellow; this thing
とすれば	p. conj. if that is the case
ねばならない	cp. must, have to
とはいえ	p. conj. though, however
こつ	n. knack
せめて	adv. at least, at most
ないといけない	cp. must, have to
じゃん	p. disc. isn't it?
ただいま	adv. now, just now, at once; I'm back!
につれて	cp. as
ぼおっと	adv. vacantly; dimly
いまさら	adv. now (after such a long time)
とりわけ	adv. especially
いかにも	adv. indeed, really, just
わー	interj. wow!
ですけれど	conj. but
おとなしい	i-adj. gentle, well‐behaved, quiet
さっぱり	adv. not at all
こしょう	n. pepper
おもちゃ	n. toy
よし	interj. All right!, Good!
いまや	adv. now
はがき	n. postcard
いかなる	adn. what kind of, any
あちこち	pron. here and there, everywhere
もったいない	i-adj. wasteful; too good
ぎりぎり	adv. barely
あご	n. jaw, chin
ねた	n. material; ingredient
むろん	adv. of course
なくてはならない	cp. must
ゆったり	adv. comfortably; calm; loose
あら	interj. Oh! (used by female speakers)
OS (OS)	n. operating system
まとも	na-adj. direct; honest; proper
をめぐる	cp. over, concerning
そこらへん	n. around there; such a matter
じっくり	adv. without haste, deliberately
ううん	interj. no; well
ならびに	conj. and, both . . . and
たちまち	adv. in a moment, at once; suddenly
わがまま	[1] na-adj. selfish, disobedient [2] n. selfishness
なおかつ	adv. besides, and yet
つくづく	adv. thoroughly, deeply, carefully
ねえ	interj. hey
せいぜい	adv. at most
いちいち	adv. one by one; everything
えび	n. prawn, shrimp
にわたる	cp. ranging, covering
そこそこ	adv. about; in a hurry; all right
いえ	interj. no
かすか	na-adj. a few, a little
でかい	i-adj. big, huge
やたら	adv. freely, thoughtlessly
いつか	adv. someday
たいして	adv. (not) very much
そいつ	n. that guy
までもない	cp. needless
DVD (DVD)	n. DVD
しも	p. EMPHASIS (Classical)
ゆとり	n. have something to spare
にぎやか	na-adj. busy, bustling
まれ	na-adj. rare
ひそか	[1] na-adj. secret, confidential [2] adv. secretly
ごちそう（する）	[1] n. feast [2] v. give a dinner, treat
さっと	adv. quickly
わざと	adv. intentionally
いいえ	interj. no
まさしく	adv. surely, exactly
だけど	conj. but, however
HP (HP)	n. home page
そっくり	[1] na-adj. resembling, just like [2] adv. altogether
きっちり	adv. tightly
もっぱら	adv. entirely
そうこう	adv. in the meantime
さほど	adv. (not) particularly
よそ	n. other, elsewhere
あっさり	adv. easily, flatly, simple, plain
しっぽ	n. tail
TV (TV)	n. television
しつけ	n. tacking (sewing); discipline
ID (ID)	n. identification, ID
しわ	n. wrinkle, line
ぼんやり（する）	[1] adv. vacantly, vaguely, dimly [2] v. be vague, be blurred
ぐるぐる	adv. round and round
おかしな	adn. funny, ridiculous
あれこれ	adv. this and that
いまいち	adv. not quite, not really
それゆえ	adv. therefore, thus
おしゃべり（する）	[1] n. chat, talk [2] v. chat, talk
ＷＷＷ (ＷＷＷ)	n. World Wide Web
おはよう	interj. good morning
こんにちは	interj. Hello, Good afternoon
ふっと	adv. suddenly
さっさと	adv. quickly
いささか	adv. a little, slightly, rather
すっと	adv. quickly; quietly; straight
まし	[1] na-adj. better [2] n. increase
DNA (DNA)	n. DNA, deoxyribonucleic acid
そりゃ	pron. that is
こだわり	n. concern, obsession
おめでとう	interj. congratulations
いやあ	interj. Well, sorry
〜さん	suffix Mr., Mrs., Miss., Ms.
ぼろぼろ	[1] na-adj. ragged, worn out [2] adv. in drops
いたずら（する）	[1] n. mischief, trick, joke [2] v. be mischievous, play a trick
ふらふら（する）	[1] adv. aimlessly, unsteadily [2] na-adj. unsteady on one's feet [3] v. stagger, be dizzy
おかず	n. food, side dish
のみならず	p. not only ... but, as well as
OB (OB)	n. OB (old boy), alumnus
そんなこんな	adv. what with one thing and another; after many twists and turns
こっそり	adv. secretly, on the sly
きゅうり	n. cucumber
ごと	suffix every
かゆい	i-adj. itchy
URL (URL)	n. URL, Uniform Resource Locator
はたち	n. twenty years old
ただただ	adv. all (someone) can do is, simply, nothing but
うどん	n. udon, thick white noodles
みそ	n. miso; key point
しつこい	i-adj. persistent; over-rich (food)
なじみ	n. familiarity
しみじみ	adv. keenly, heartily, from one's heart
まあまあ	[1] na-adj. so-so, not bad [2] adv. fairly, moderately"""
        
        compounds = {}
        
        for line in word_list.strip().split('\n'):
            if not line.strip():
                continue
            
            # Split by tab to get word and category+meaning
            parts = line.split('\t', 1)
            if len(parts) < 2:
                continue
            
            words_str, rest = parts[0].strip(), parts[1].strip()
            
            # Handle multiple word variations (separated by comma)
            word_variations = [w.strip() for w in words_str.split('、')]
            
            # Parse category and meaning
            # Format: "category. meaning" or "[number] category. meaning"
            rest = rest.strip()
            
            # Remove bracketed numbers like [1], [2]
            rest = re.sub(r'\[\d+\]\s*', '', rest)
            
            # Find category (ends with period or space)
            category_match = re.match(r'^([a-z.-]+(?:\s+[a-z.]+)?)\.?\s+(.+)', rest)
            if not category_match:
                continue
            
            cat_abbr = category_match.group(1).strip()
            meaning = category_match.group(2).strip()
            
            # Map category abbreviation to full name
            # Handle multiple categories separated by comma (like "adv., na-adj.")
            categories = [c.strip() for c in cat_abbr.split(',')]
            # Use the first category for mapping
            primary_cat = categories[0]
            category = category_map.get(primary_cat, primary_cat.replace('.', ''))
            
            # Add each word variation
            for word in word_variations:
                # Skip words with parentheses like "（する）" for now, just use base
                word_clean = re.sub(r'\([^)]*\)', '', word).strip()
                if word_clean:
                    # Don't overwrite existing entries
                    if word_clean not in compounds:
                        compounds[word_clean] = (category, meaning)
        
        return compounds
    
    def _load_particles(self) -> Set[str]:
        """Load Japanese particles"""
        return {
            'は', 'が', 'を', 'に', 'で', 'と', 'へ', 'から', 'まで',
            'の', 'も', 'や', 'か', 'よ', 'ね', 'な', 'わ', 'ぞ', 'ぜ'
        }
    
    def _load_patterns(self) -> Dict[str, Tuple[str, List[str]]]:
        """
        Load grammar patterns
        Format: {pattern_type: (meaning, [pattern_strings])}
        """
        return {
            'desire': ('want to do', [
                'たい', 'たがる', 'たくない', 'たかった',
                'てほしい', 'がほしい', 'ほしい'
            ]),
            'progressive': ('progressive/continuous', [
                'ている', 'でいる', 'てある', 'であった'
            ]),
            'completion': ('completion/regret', [
                'てしまう', 'でしまう', 'ちゃう', 'じゃう', 
                'てしまった', 'ちゃった'
            ]),
            'try': ('try doing', [
                'てみる', 'でみる', 'てみた'
            ]),
            'obligation': ('must/should', [
                'なければならない', 'なければいけない',
                'なくてはならない', 'なくてはいけない',
                'ないといけない', 'ないとだめだ',
                'べきだ', 'べきではない'
            ]),
            'explanatory': ('explanatory emphasis', [
                'んだ', 'のだ', 'んです', 'のです',
                'んじゃない', 'のではない'
            ]),
            'appearance': ('seems/looks like', [
                'そうだ', 'そうです', 'ようだ', 'ようです',
                'みたいだ', 'みたいです', 'らしい'
            ]),
            'conditional': ('if/when', [
                'たら', 'れば', 'なら', 'ても', 'でも', 'と'
            ]),
            'experience': ('have done before', [
                'たことがある', 'たことがない', 'たことがあります'
            ]),
            'intention': ('intend to', [
                'ようとする', 'ようと思う', 'つもりだ', 
                'ことにする', 'ことになる'
            ]),
        }
    
    def find_compounds(self, text: str) -> List[Compound]:
        """Find all compound expressions in text"""
        found = []
        
        # Sort by length (longest first) to match greedily
        for compound in sorted(self.compounds.keys(), key=len, reverse=True):
            pos = 0
            while True:
                pos = text.find(compound, pos)
                if pos == -1:
                    break
                
                category, meaning = self.compounds[compound]
                found.append(Compound(
                    text=compound,
                    category=category,
                    meaning=meaning,
                    position=pos
                ))
                pos += len(compound)
        
        # Sort by position
        found.sort(key=lambda x: x.position)
        return found
    
    def find_particles(self, text: str) -> List[Tuple[str, int]]:
        """Find all particles in text"""
        found = []
        for i, char in enumerate(text):
            if char in self.particles:
                found.append((char, i))
        return found
    
    def find_grammar_patterns(self, text: str) -> List[Pattern]:
        """Find all grammar patterns in text"""
        found = []
        
        for pattern_type, (meaning, pattern_list) in self.patterns.items():
            # Sort by length (longest first) to avoid partial matches
            for pattern in sorted(pattern_list, key=len, reverse=True):
                pos = 0
                while True:
                    pos = text.find(pattern, pos)
                    if pos == -1:
                        break
                    
                    found.append(Pattern(
                        text=pattern,
                        pattern_type=pattern_type,
                        meaning=meaning,
                        position=pos
                    ))
                    pos += len(pattern)
        
        # Sort by position and remove duplicates
        found.sort(key=lambda x: x.position)
        return found
    
    def count_character_types(self, text: str) -> Dict[str, int]:
        """Count different character types"""
        counts = {
            'kanji': 0,
            'hiragana': 0,
            'katakana': 0,
            'ascii': 0,
            'other': 0,
        }
        
        for char in text:
            code = ord(char)
            if 0x4E00 <= code <= 0x9FFF:  # Kanji
                counts['kanji'] += 1
            elif 0x3040 <= code <= 0x309F:  # Hiragana
                counts['hiragana'] += 1
            elif 0x30A0 <= code <= 0x30FF:  # Katakana
                counts['katakana'] += 1
            elif 0x0000 <= code <= 0x007F:  # ASCII
                counts['ascii'] += 1
            else:
                counts['other'] += 1
        
        return counts
    
    def analyze(self, text: str) -> Dict:
        """Complete analysis of text"""
        compounds = self.find_compounds(text)
        # particles = self.find_particles(text)
        particles = []
        #patterns = self.find_grammar_patterns(text)
        patterns = []
        char_counts = self.count_character_types(text)
        
        # Calculate complexity score
        complexity = self._calculate_complexity(text, compounds, patterns, char_counts)
        
        return {
            'text': text,
            'compounds': compounds,
            'particles': particles,
            'grammar_patterns': patterns,
            'character_counts': char_counts,
            'complexity': complexity,
            'stats': {
                'length': len(text),
                'compound_count': len(compounds),
                'pattern_count': len(patterns),
                'particle_count': len(particles),
            }
        }
    
    def _calculate_complexity(self, text: str, compounds: List, 
                             patterns: List, char_counts: Dict) -> float:
        """Calculate text complexity (0-5 scale)"""
        complexity = 0.0
        
        # Length factor
        complexity += len(text) / 30.0
        
        # Kanji density
        if len(text) > 0:
            kanji_ratio = char_counts['kanji'] / len(text)
            complexity += kanji_ratio * 3.0
        
        # Pattern complexity
        complexity += len(patterns) * 0.5
        
        # Compound usage
        complexity += len(compounds) * 0.3
        
        return min(complexity, 5.0)
    
    def compare_sentences(self, sent1: str, sent2: str) -> Dict:
        """Compare two sentences for learning similarity"""
        analysis1 = self.analyze(sent1)
        analysis2 = self.analyze(sent2)
        
        # Find shared compounds
        compounds1 = {c.text for c in analysis1['compounds']}
        compounds2 = {c.text for c in analysis2['compounds']}
        shared_compounds = compounds1 & compounds2
        
        # Find shared patterns
        patterns1 = {p.text for p in analysis1['grammar_patterns']}
        patterns2 = {p.text for p in analysis2['grammar_patterns']}
        shared_patterns = patterns1 & patterns2
        
        # Calculate similarity
        compound_sim = len(shared_compounds) / max(len(compounds1 | compounds2), 1)
        pattern_sim = len(shared_patterns) / max(len(patterns1 | patterns2), 1)
        complexity_sim = 1.0 - abs(analysis1['complexity'] - analysis2['complexity']) / 5.0
        
        total_similarity = (compound_sim * 0.4 + pattern_sim * 0.4 + complexity_sim * 0.2)
        
        return {
            'similarity': total_similarity,
            'shared_compounds': shared_compounds,
            'shared_patterns': shared_patterns,
            'complexity_diff': abs(analysis1['complexity'] - analysis2['complexity']),
        }
    
    def find_similar_sentences(self, target: str, candidates: List[str], 
                               top_k: int = 5) -> List[Tuple[str, float, Dict]]:
        """Find most similar sentences"""
        results = []
        
        for candidate in candidates:
            if candidate == target:
                continue
            
            comparison = self.compare_sentences(target, candidate)
            results.append((
                candidate,
                comparison['similarity'],
                comparison
            ))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def format_analysis(self, analysis: Dict) -> str:
        """Format analysis for display"""
        lines = [
            f"Text: {analysis['text']}",
            f"\nStats:",
            f"  Length: {analysis['stats']['length']} characters",
            f"  Complexity: {analysis['complexity']:.2f}/5.0",
            f"\nCharacter Breakdown:",
        ]
        
        for char_type, count in analysis['character_counts'].items():
            if count > 0:
                lines.append(f"  {char_type.capitalize()}: {count}")
        
        if analysis['compounds']:
            lines.append(f"\nCompound Expressions ({len(analysis['compounds'])}):")
            seen = set()
            for compound in analysis['compounds']:
                if compound.text not in seen:
                    lines.append(f"  • {compound.text:12s} - {compound.meaning} ({compound.category})")
                    seen.add(compound.text)
        
        if analysis['grammar_patterns']:
            lines.append(f"\nGrammar Patterns ({len(analysis['grammar_patterns'])}):")
            seen = set()
            for pattern in analysis['grammar_patterns']:
                if pattern.text not in seen:
                    lines.append(f"  • {pattern.text:15s} - {pattern.meaning} ({pattern.pattern_type})")
                    seen.add(pattern.text)
        
        if analysis['particles']:
            unique_particles = sorted(set(p[0] for p in analysis['particles']))
            lines.append(f"\nParticles: {', '.join(unique_particles)}")
        
        return '\n'.join(lines)


def analyze_sentence_with_fugashi(sentence: str) -> Dict:
    """
    Analyze a Japanese sentence using fugashi for part-of-speech tagging
    and PureJapaneseAnalyzer for pattern/compound detection.
    
    Returns a dictionary with:
    - verbs: list of dicts with {lemma, verb, position, auxiliary_verb}
    - nouns: list of nouns
    - adjectives: list of adjectives
    - adverbs: list of adverbs
    - pure_analyzer: dict from PureJapaneseAnalyzer.analyze()
    
    Args:
        sentence: Japanese sentence to analyze
        
    Returns:
        Dictionary with extracted parts of speech and analysis
    """
    if not FUGASHI_AVAILABLE:
        raise ImportError("fugashi is not installed. Please install it with: pip install fugashi")
    
    tagger = Tagger()
    
    # Part of speech mapping (Japanese -> English)
    POS_MAPPING = {
        "動詞": "verb",
        "形容詞": "adjective",
        "名詞": "noun",
        "助動詞": "auxiliary_verb",
        "副詞": "adverb",
    }
    
    # Initialize result lists
    verbs = []
    nouns = []
    adjectives = []
    adverbs = []
    
    # Tokenize the sentence
    words = tagger(sentence)
    
    # Track current position in the sentence by accumulating token lengths
    current_pos = 0
    
    # Iterate through words and extract parts of speech
    for i, word in enumerate(words):
        surface = word.surface
        
        # Skip unknown words
        if word.is_unk:
            current_pos += len(surface)
            continue
        
        # Skip auxiliary symbols (補助記号)
        if word.feature.pos1 == "補助記号":
            current_pos += len(surface)
            continue
        
        pos_jp = word.feature.pos1
        pos_en = POS_MAPPING.get(pos_jp)
        lemma = word.feature.lemma
        
        # Use current position (accumulated from previous tokens)
        position = current_pos
        
        # Check if next word is an auxiliary verb (for verbs)
        auxiliary_verb = ""
        if pos_en == "verb" and i + 1 < len(words):
            next_word = words[i + 1]
            if not next_word.is_unk and next_word.feature.pos1 == "助動詞":
                auxiliary_verb = next_word.surface
        
        # Add to appropriate list
        if pos_en == "verb":
            verbs.append({
                "lemma": lemma,
                "verb": surface,
                "position": position,
                "auxiliary_verb": auxiliary_verb
            })
        elif pos_en == "noun":
            nouns.append({
                "surface": surface,
                "lemma": lemma,
                "position": position
            })
        elif pos_en == "adjective":
            adjectives.append({
                "surface": surface,
                "lemma": lemma,
                "position": position
            })
        elif pos_en == "adverb":
            adverbs.append({
                "surface": surface,
                "lemma": lemma,
                "position": position
            })
        
        # Update position for next token
        current_pos += len(surface)
    
    # Run PureJapaneseAnalyzer
    analyzer = PureJapaneseAnalyzer()
    pure_analysis = analyzer.analyze(sentence)
    
    # Convert PureJapaneseAnalyzer dataclasses to dict format
    pure_analysis_dict = {
        "text": pure_analysis["text"],
        "compounds": [
            {
                "text": c.text,
                "category": c.category,
                "meaning": c.meaning,
                "position": c.position
            }
            for c in pure_analysis["compounds"]
        ],
        "particles": [
            {"particle": p[0], "position": p[1]}
            for p in pure_analysis["particles"]
        ],
        "grammar_patterns": [
            {
                "text": p.text,
                "pattern_type": p.pattern_type,
                "meaning": p.meaning,
                "position": p.position
            }
            for p in pure_analysis["grammar_patterns"]
        ],
        "character_counts": pure_analysis["character_counts"],
        "complexity": pure_analysis["complexity"],
        "stats": pure_analysis["stats"]
    }
    
    return {
        "verbs": verbs,
        "nouns": nouns,
        "adjectives": adjectives,
        "adverbs": adverbs,
        "pure_analyzer": pure_analysis_dict
    }


def analyze_sentence_unified(sentence: str) -> Dict:
    """
    Analyze a Japanese sentence combining fugashi and PureJapaneseAnalyzer
    into a single unified structure.
    
    Returns a dictionary with:
    - text: the original sentence
    - elements: list of unified elements sorted by position
    
    Each element has:
    - text: surface form
    - lemma: lemma/dictionary form (if available)
    - category: category/type (e.g., 'conjunction', 'verb', 'adverb')
    - meaning: meaning/translation (if available)
    - position: character position in sentence
    - type: element type ('compounds', 'verb', 'noun', 'adjective', 'adverb', 
           'grammar_patterns', 'particles')
    - auxiliary_verb: auxiliary verb if applicable (for verbs)
    
    Args:
        sentence: Japanese sentence to analyze
        
    Returns:
        Dictionary with unified structure
    """
    # Get analysis from both analyzers
    analysis = analyze_sentence_with_fugashi(sentence)
    pure_analyzer = analysis["pure_analyzer"]
    
    elements = []
    
    # Add compounds from PureJapaneseAnalyzer
    for compound in pure_analyzer["compounds"]:
        elements.append({
            "text": compound["text"],
            "lemma": "",
            "category": compound["category"],
            "meaning": compound["meaning"],
            "position": compound["position"],
            "type": "compounds"
        })
    
    # Add verbs from fugashi
    for verb in analysis["verbs"]:
        element = {
            "text": verb["verb"],
            "lemma": verb["lemma"],
            "category": "verb",
            "meaning": "",
            "position": verb["position"],
            "type": "verb"
        }
        if verb["auxiliary_verb"]:
            element["auxiliary_verb"] = verb["auxiliary_verb"]
        elements.append(element)
    
    # Add nouns from fugashi
    for noun in analysis["nouns"]:
        elements.append({
            "text": noun["surface"],
            "lemma": noun["lemma"],
            "category": "noun",
            "meaning": "",
            "position": noun["position"],
            "type": "noun"
        })
    
    # Add adjectives from fugashi
    for adjective in analysis["adjectives"]:
        elements.append({
            "text": adjective["surface"],
            "lemma": adjective["lemma"],
            "category": "adjective",
            "meaning": "",
            "position": adjective["position"],
            "type": "adjective"
        })
    
    # Add adverbs from fugashi
    for adverb in analysis["adverbs"]:
        elements.append({
            "text": adverb["surface"],
            "lemma": adverb["lemma"],
            "category": "adverb",
            "meaning": "",
            "position": adverb["position"],
            "type": "adverb"
        })
    
    # Add grammar patterns from PureJapaneseAnalyzer
    for pattern in pure_analyzer["grammar_patterns"]:
        elements.append({
            "text": pattern["text"],
            "lemma": "",
            "category": pattern["pattern_type"],
            "meaning": pattern["meaning"],
            "position": pattern["position"],
            "type": "grammar_patterns"
        })
    
    # Add particles from PureJapaneseAnalyzer
    for particle in pure_analyzer["particles"]:
        elements.append({
            "text": particle["particle"],
            "lemma": "",
            "category": "particle",
            "meaning": "",
            "position": particle["position"],
            "type": "particles"
        })
    
    # Merge duplicate elements (same position and text)
    elements = _merge_duplicate_elements(elements)
    
    # Sort elements by position
    elements.sort(key=lambda x: x["position"])
    
    # Extract character counts from pure_analyzer
    char_counts = pure_analyzer["character_counts"]
    
    # Extract unique characters
    unique_chars = _extract_unique_characters(sentence)
    
    return {
        "text": sentence,
        "elements": elements,
        "kanji_count": char_counts.get("kanji", 0),
        "hiragana_count": char_counts.get("hiragana", 0),
        "katakana_count": char_counts.get("katakana", 0),
        "other_count": char_counts.get("other", 0) + char_counts.get("ascii", 0),
        "unique_kanji_letters": unique_chars["kanji"],
        "unique_hiragana_letters": unique_chars["hiragana"],
        "unique_katakana_letters": unique_chars["katakana"]
    }


def _extract_unique_characters(text: str) -> Dict[str, List[str]]:
    """
    Extract unique kanji, hiragana, and katakana characters from text.
    
    Args:
        text: Japanese text to analyze
        
    Returns:
        Dictionary with lists of unique characters for each type:
        - kanji: list of unique kanji characters
        - hiragana: list of unique hiragana characters
        - katakana: list of unique katakana characters
    """
    unique_kanji = set()
    unique_hiragana = set()
    unique_katakana = set()
    
    for char in text:
        code = ord(char)
        if 0x4E00 <= code <= 0x9FFF:  # Kanji
            unique_kanji.add(char)
        elif 0x3040 <= code <= 0x309F:  # Hiragana
            unique_hiragana.add(char)
        elif 0x30A0 <= code <= 0x30FF:  # Katakana
            unique_katakana.add(char)
    
    return {
        "kanji": sorted(list(unique_kanji)),
        "hiragana": sorted(list(unique_hiragana)),
        "katakana": sorted(list(unique_katakana))
    }


def _merge_duplicate_elements(elements: List[Dict]) -> List[Dict]:
    """
    Merge duplicate elements that have the same position and text.
    
    When duplicates are found, the merged element will have:
    - Combined types (as a list if multiple)
    - Best available lemma (prefer non-empty)
    - Combined categories if different
    - Combined meanings if different
    - All unique fields from all duplicates
    
    Args:
        elements: List of element dictionaries
        
    Returns:
        List of merged elements without duplicates
    """
    # Group elements by (position, text) key
    element_groups = {}
    
    for elem in elements:
        key = (elem["position"], elem["text"])
        
        if key not in element_groups:
            element_groups[key] = []
        element_groups[key].append(elem)
    
    # Merge each group
    merged_elements = []
    
    for key, group in element_groups.items():
        if len(group) == 1:
            # No duplicates, just add as is
            merged_elements.append(group[0])
        else:
            # Merge duplicates
            merged = _merge_element_group(group)
            merged_elements.append(merged)
    
    return merged_elements


def _merge_element_group(group: List[Dict]) -> Dict:
    """
    Merge a group of duplicate elements into a single element.
    Prefers fugashi types (verb, noun, adjective, adverb) over other types
    as fugashi provides more accurate part-of-speech tagging.
    
    Args:
        group: List of elements with same position and text
        
    Returns:
        Single merged element dictionary
    """
    # Fugashi types are more accurate - prioritize them
    fugashi_types = {"verb", "noun", "adjective", "adverb"}
    
    # Find elements with fugashi types first
    fugashi_elements = [elem for elem in group if elem.get("type", "") in fugashi_types]
    
    # Use fugashi element as base if available, otherwise use first element
    if fugashi_elements:
        merged = fugashi_elements[0].copy()
    else:
        merged = group[0].copy()
    
    # Collect all types, but prefer fugashi type
    types = {elem.get("type", "") for elem in group if elem.get("type")}
    fugashi_type = next((t for t in types if t in fugashi_types), None)
    
    if fugashi_type:
        # Use fugashi type (more accurate)
        merged["type"] = fugashi_type
    elif len(types) == 1:
        merged["type"] = next(iter(types))
    else:
        # Multiple types but no fugashi type - keep the first one
        merged["type"] = merged.get("type", "")
    
    # Find best lemma (prefer non-empty)
    lemmas = [elem.get("lemma", "") for elem in group if elem.get("lemma")]
    if lemmas:
        # Use first non-empty lemma
        best_lemma = next((lem for lem in lemmas if lem), "")
        if best_lemma:
            merged["lemma"] = best_lemma
    
    # Combine categories if different
    categories = {elem.get("category", "") for elem in group if elem.get("category")}
    if len(categories) > 1:
        # Keep primary category, but note additional ones
        merged["category"] = merged.get("category", "")
        merged["additional_categories"] = list(categories - {merged["category"]})
    else:
        merged["category"] = merged.get("category", "")
    
    # Combine meanings if different (separate by semicolon)
    meanings = {elem.get("meaning", "") for elem in group if elem.get("meaning")}
    meanings = {m for m in meanings if m}  # Remove empty
    if len(meanings) > 1:
        merged["meaning"] = "; ".join(sorted(meanings))
    elif meanings:
        merged["meaning"] = next(iter(meanings))
    
    # Merge other fields (like auxiliary_verb)
    for elem in group[1:]:
        for key, value in elem.items():
            if key not in merged and value:
                merged[key] = value
            elif key == "auxiliary_verb" and value and not merged.get("auxiliary_verb"):
                merged["auxiliary_verb"] = value
    
    return merged


def containes(contain, elm):
    pos_contain = contain.get('position')
    pos_elm = elm.get('position')
    contain_len = len(contain.get('text'))
    elm_len = len(elm.get('text'))
    if elm_len > contain_len:
        return False
    if pos_elm > pos_contain + contain_len:
        return False
    if elm.get('text') in contain.get('text'):
        return True
    return False
def remove_substring_elements(elements):
    """Remove elements whose text is contained in another element at the same position"""
    result = []
    
    for elem in elements:
        is_substring = False
        # Check if this element's text is a substring of any other element at the same position
        for other in elements:
            if elem is not other and containes(other, elem) :
                is_substring = True
                break
        if not is_substring:
            result.append(elem)
    
    return result

# Usage


analyzer = PureJapaneseAnalyzer()


def analyze_sentence(text:str, id:int, lang:str) -> Dict:
    u =  analyze_sentence_unified(text)
    filtered_elements = remove_substring_elements(u['elements'])
    for f in filtered_elements:
        f.update(translit_single(f.get('text')))
    u['elements'] = filtered_elements
    print(u)
    verb_count = 0
    noun_count = 0
    adjective_count = 0
    adverb_count = 0
    for element in u['elements']:
        if element['type'] == 'verb':
            verb_count+=1
            u[f'verb{verb_count}'] = element.get('text')
            u[f'verb_aux{verb_count}'] = element.get('text') + element.get('auxiliary_verb','')
            u[f'verb_lemma{verb_count}'] = element.get('lemma')
            u[f'auxiliary_verb{verb_count}'] = element.get('auxiliary_verb')
        elif element['type'] == 'noun':
            noun_count+=1
            u[f'noun{noun_count}'] = element.get('text')
        elif element['type'] == 'adjective':
            adjective_count+=1
            u[f'adjective{adjective_count}'] = element.get('text')
        elif element['type'] == 'adverb':
            adverb_count+=1
            u[f'adverb{adverb_count}'] = element.get('text')
    u['verb_count'] = verb_count
    u['noun_count'] = noun_count
    u['adjective_count'] = adjective_count
    u['adverb_count'] = adverb_count

    unique_kanji_letters = ''.join(sorted(u.get('unique_kanji_letters',     [])))
    unique_hiragana_letters = ''.join(sorted(u.get('unique_hiragana_letters', [])))
    unique_katakana_letters = ''.join(sorted(u.get('unique_katakana_letters', [])))
    #u['unique_kanji_letters'] = unique_kanji_letters
    #u['unique_hiragana_letters'] = unique_hiragana_letters
    #u['unique_katakana_letters'] = unique_katakana_letters
    u['lang_extra'] = {
        'kanji':unique_kanji_letters,
        'hiragana': unique_hiragana_letters,
        'katakana':unique_hiragana_letters,
    }
    u['len_c'] = len(text)
    u['len_e'] = len(filtered_elements)
    u['root'], u['root_lemma'] = get_root(text)
    root, root_lemma = get_root(text)
    u['root'] = root
    u['root_lemma'] = root_lemma
    return u


    return u


# Example usage
if __name__ == "__main__":
    test_text = "でも、今すぐ読みたいんだ。それで、図書館に行くことにした。"
    unified = analyze_sentence_unified(test_text)
    print(json.dumps(unified, indent=2, ensure_ascii=False))
    filtered_elements = remove_substring_elements(unified['elements'])
    for g in unified['elements']:
        print(g.get('text'))
    print("--------------------------------")
    with_t = []
    for f in filtered_elements:
        f.update(translit_single(f.get('text')))
    for f in filtered_elements:
        print(f)
    print("--------------------------------")
