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

# 所感

　[unittest][]フレームワークとの相性が悪いのか？　それとも私が何か勘違いしている？

　テストコードを静的チェックなんてしないものなの？　わからん。

　`python mypy unittest`とかでググっても同じケースは見つからなかった。まさか標準ライブラリである[unittest][]なんて誰も使ってないから発生してない、なんてわけないだろうし。

[unittest]:https://docs.python.org/ja/3/library/unittest.html

