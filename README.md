GraphQLサーバの練習

# はじめに

このリポジトリは下記の要素で遊ぶ予定です。

python(language)
  + graphene(GraphQLフレームワーク)
  + pydantic
  + fastapi(webフレームワーク)
  + sqlalchemy(ORM)

# コミットメッセージのプレフィクスルール

https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#type

# pipenvについて

pythonのパッケージ管理ツール

[参考サイト](https://pipenv-ja.readthedocs.io/ja/translate-ja/index.html)

- install

```shell
pipenv install packageName
```

- pipenv環境下でshellを実行

```shell
pipenv shell
```

- pipenv環境下でファイル実行

```shell
pipenv run python sample.py
```

- セキュリティチェック

```shell
pipenv check
```

- pipenv環境下でインストールしたパッケージを開く

```shell
pipenv open packageName
```

- unittest

```shell
pipenv run pytest
```
