unittestのコードにmypyしても成功判定されてしまう

　原因不明。

<!-- more -->

# ブツ

* [リポジトリ][]

[リポジトリ]:https://github.com/ytyaru/Python.unittest.mypy.dataclass.20221014141052

## 実行

```sh
NAME='Python.unittest.mypy.dataclass.20221014141052'
git clone https://github.com/ytyaru/$NAME
cd $NAME/src
./run.sh
```

## 結果

```sh
$ ./test.sh
----- mypyを実行する(1件あたり20秒くらいかかる) -----
----- ./data-class-2.py -----
data-class-2.py:10: error: List item 0 has incompatible type "str"; expected "int"
data-class-2.py:10: error: List item 1 has incompatible type "str"; expected "int"
Found 2 errors in 1 file (checked 1 source file)
----- ./record.py -----
record.py:9: error: List item 0 has incompatible type "str"; expected "int"
record.py:9: error: List item 1 has incompatible type "str"; expected "int"
Found 2 errors in 1 file (checked 1 source file)
----- ./test-data-class.py -----
Success: no issues found in 1 source file
........
----------------------------------------------------------------------
Ran 8 tests in 0.002s

OK
===== テスト完了 =====
```

ファイル|結果
--------|----
`data-class-2.py`|`Found 2 errors`
`record.py`|`Found 2 errors`
`test-data-class.py`|`Success`

　3ファイルとも以下のようなエラーになるコードを書いている。なのに[unittest][]なコードだとリント`mypy`がクリアされてしまう。そこでもエラーを出してほしかったのに。

```python
@dataclass
class Record:
    item_ids: list[int]

Record(['A','B']) # int でなく str だろエラー
```

## record.py

```python
from dataclasses import dataclass, field, Field
@dataclass
class Record:
    item_ids: list[int]
if __name__ == '__main__':
    Record([1,2,3])
    Record(['A','B'])
```

## data-class-2.py

```python
#!/usr/bin/env python3
# coding: utf8
from dataclasses import dataclass, field, Field
@dataclass
class Record:
    item_ids: list[int]
if __name__ == '__main__':
    args = [1,2,3]
    Record(args)
    args = ['A','B']
    Record(args)
```

　一旦変数に入れてから試してもやはりちゃんとエラーになってくれる。

## test-data-class.py

```python

#!/usr/bin/env python3
# coding: utf8
import unittest
import dataclasses
from dataclasses import dataclass, field, Field
from decimal import Decimal
from datetime import datetime, date, time
import types
@dataclass
class Record:
    item_ids: list[int]
class TestDataClass(unittest.TestCase):
    def setUp(self): pass
    def tearDown(self): pass
    def test_init_args_0(self):
        item_ids = [1, 2, 3]
        r = Record(item_ids)
        self.assertEqual(item_ids, r.item_ids)
    def test_init_args_1(self):
        args = [[1, 2, 3]]
        r = Record(*args)
        self.assertEqual(args[0], r.item_ids)
    def test_init_kwargs_0(self):
        kwargs = {'item_ids': [1, 2, 3]}
        r = Record(**kwargs)
        self.assertEqual(kwargs['item_ids'], r.item_ids)
    def test_init_args_error_generic_type_0(self): # これパスされちゃ困るんだが……
        item_ids = [1, 2, 'A']
        r = Record(item_ids)
        self.assertEqual(item_ids, r.item_ids)
    def test_init_args_error_generic_type_1(self): # これパスされちゃ困るんだが……
        item_ids = ['A', 'B', 'C']
        r = Record(item_ids)
        self.assertEqual(item_ids, r.item_ids)
    def test_init_args_error_type_int(self): # これパスされちゃ困るんだが……
        item_ids = 1
        r = Record(item_ids)
        self.assertEqual(item_ids, r.item_ids)
    def test_init_args_error_type_str(self): # これパスされちゃ困るんだが……
        item_ids = 'A'
        r = Record(item_ids)
        self.assertEqual(item_ids, r.item_ids)
    def test_init_args_error_type_str_direct(self): # これパスされちゃ困るんだが……
        r = Record('A')
        self.assertEqual('A', r.item_ids)
     

if __name__ == '__main__':
    unittest.main()
```

　たとえば以下とか。明らかに他の2ファイルと同じようなエラーコード。なのにエラーが出ない。なぜ？

```python
item_ids = ['A', 'B', 'C']
r = Record(item_ids)
```

# 原因の予想

　もしや呼び出されていないコードはチェックしないのでは？　たとえば[unittest][]フレームワークの呼出コードだけを見ていると`unittest.main()`が実行されているけど、コードのテキスト内には`main`なんて関数がない。だから何もチェックしてやがらないのでは？

　……すごくそんな気がしてきた。

## not-call.py

　エラーコード`Record(['A','B'])`を関数`not_call`内に定義する。そして`not_call`はその名の通り呼び出さない。

```python
#!/usr/bin/env python3
# coding: utf8
from dataclasses import dataclass, field, Field
@dataclass
class Record:
    item_ids: list[int]
if __name__ == '__main__':
    def not_call():
        Record([1,2,3])
        Record(['A','B'])
```

```sh
mypy not-call.py
```
```sh
Success: no issues found in 1 source file
```

　やっぱりぃぃぃ！

　Pythonで実行したとき呼び出される箇所でないとチェックされないっぽい。

　勘弁してよ。チェックしてよ。定義してるのに一度も呼び出してない時点で警告してよ。その中身もチェックして型エラーかどうか見てくれるのが君の仕事じゃないのか[mypy][]よ。

[mypy]:https://github.com/python/mypy

　え、でも[unittest][]だって実行したらテストメソッド呼び出されるよ？

　と思うが、コードをよく見ると`unittest.main()`で呼び出されるが、コードのテキストとしてはどこにも`main`関数が定義されていない。どんな実装になっているか知らないが、コード（テキスト）を見ただけでは呼び出されていないからチェックしないということなのだろう。それがコードの静的チェックということなのだろう。

　困ります。ふつうにコンパイル型の言語ならこんなマヌケなことは起こらない。たとえ呼び出されていなくてもコンパイルエラーになってくれる。それと同じことを期待していたのだが。知れば知るほど残念さが滲み出るな。

　心配なのは、他にもこうしてテストされないのに`Success`とのたまうケースが起きないか。たとえばクラスの継承とかしてて、親にしか定義していないメソッドを呼び出していて、そこで型エラーを起こしているときとか。

　試してみよう。

## 別ファイルの親クラスにしかないメソッドを呼び出した所で型エラー

### parent.py

```python
#!/usr/bin/env python3
# coding: utf8
class Parent:
    def parent_only(self, value:int):
        print('親にしかないメソッド。引数valueはint型であるべき。')
```

### child.py

```python
#!/usr/bin/env python3
# coding: utf8
from parent import Parent
class Child(Parent): pass
if __name__ == '__main__':
    c = Child()
    c.parent_only(1)
    c.parent_only('A') # str でなく int だろエラーを期待
```

```sh
mypy child.py
```
```sh
Python.unittest.mypy.dataclass.20221014141052/src/child.py:8: error: Argument 1 to "parent_only" of "Parent" has incompatible type "str"; expected "int"
Found 1 error in 1 file (checked 1 source file)
```

　ちゃんとエラーが出た。

　別ファイルに定義しててもコードを追えるのか。

　ならどうして[unittest][]のときはチェックしてくれなかったんだろう。コードの実装次第ではチェックしてくれないことも起こりうると思えて怖い。[mypy][]に`Success`と言われても信用できない。チェックしてないメソッドがあるなら報告してほしい。その時点でもうおかしいから。呼び出されないメソッドなんて定義するわけない。せいぜい消し忘れくらい。なので[unittest][]のときもエラー出して欲しかった。

# まとめ

　[mypy][]を[unittest][]コードに対して実行してもチェックせず無条件で`Success`と報告してしまう。

## [mypy][]は信用できない

　そんな[mypy][]ををどこまで信用していいか分からない。[unittest][]のコードを読んで理解し、こういう作りにはしないでおこうと整理できたらまだいいが、そもそもそんな「注意しよう」とかいうヒューマンエラーが絶対起きるような状況それ自体に問題がある。そこを機械的にチェックし排除してくれるのがツールの役目だと思うのだが。

　少しググっても都合のいいことばかりで批判的なことや疑問は書かれてなかった。なおさら胡散臭い。私はこんなにすぐ問題にぶちあたったのに。

## Pythonは信用できない

　そもそもPythonはインタプリタであり実行しないかぎりエラーを発見できない。もしコンパイル言語なら実行されるかどうかに関わらずすべてのコードをチェックしエラーを出してくれる。Pythonは[unittest][]ですべてのコードを実行するようテストコードを書かなければならない時点で、呼び忘れなどのヒューマンエラーが起こりうる。テスト漏れしたらどうしようと不安になって夜も眠れない。

　そもそも昔は型定義せず楽に書けるのがPythonのウリのひとつだった。なのに結局、静的型付に寄せてきた。しかも型チェックはちゃんと仕事してない。短く書けるという長所を削って冗長になっただけ。ほかにもPython2は`print 'A'`で実行できたのにPython3は`print('A')`にしないと実行できなくなったとか。短くシンプルなスクリプトから、複雑なコードに耐えられるよう構文も複雑化・冗長化されてきた。そのせいで当初の強みが弱みになってきた。静的型付についても同じ。どうも対応が中途半端。

　結局、Python言語仕様が型なしなのが悪い。そこにツギハギで静的型付しようとしても限度がある。元から静的型付の言語に比べるとまったく信用できない。Pythonは標準ライブラリでさえ名前の統一感もなく不信感が漂う曲者。それをPEP8で正当化し、文句をつける者には人間性さえ否定してみせる始末。そのくせドキュメントはPythonを自画自賛。匂い立つ怪しさは他の言語を圧倒する。これほど知名度と比例して胡散臭い言語もない。さすが蛇の名を冠するだけはある。命名規則までスネークケースなのだから極まっている。あきらかに風評被害である。蛇かわいそう。

[unittest]:https://docs.python.org/ja/3/library/unittest.html

呼称|意味
----|----
スネーク|蛇
パイソン|大蛇
ヴァイパー|毒蛇

## ダメな子ほどかわいい

　なら違う言語を使えばいいと思うかもしれない。でも違う。

　「このPythonコードはワシが育てた！」みたいな気持ちがあるからクソ言語を使いたくなるんだと思う。bashとかもクソだけどうまく書けたら楽しいし、してやったりと思う。

　クソゲーだって愛される。ならクソ言語が愛されるのも道理。クソを愛してはじめて人は人になる。クソを愛せない者は人に非ず。人道とはクソにはじまりクソに終わる。クソったれな人生に乾杯。

　愛が問題をムダに複雑化する。厄介きわまりない。度し難きは人間なり。

