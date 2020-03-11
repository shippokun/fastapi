GraphQLサーバの練習

# はじめに

このリポジトリは下記の要素で遊ぶ予定です。

python(language)
  + graphene(GraphQLフレームワーク)
  + pydantic
  + fastapi(webフレームワーク)
  + sqlalchemy(ORM)

# 初回構築

## 手順

1. mysqlclientをインストールできるように準備
<details>
<summary>詳細なインストール手順</summary>
実行後、インストールダイアログが表示されるのでインストール

```shell
$ xcode-select --install
```

実行後にログで競合DBをアンインストールする指示が出る場合があるので、その場合はアンインストールする

```shell
$ brew install mysql-connector-c
```

mysql_configファイルの修正(修正しなくていい場合もある)

```shell
sudo vim /usr/local/bin/mysql_config
```

修正前:
```
# Create options
libs="-L$pkglibdir"
libs="$libs -l "
```

修正後:
```
# Create options
libs="-L$pkglibdir"
libs="$libs -lmysqlclient -lssl -lcrypto"
```

opensslの環境変数設定
出力結果に記載されたパスを環境変数に登録する(~/.zshrcなど)

```shell
$ brew info openssl
```

登録後再読み込み

```shell
$ exec $SHELL -l
```

これで完了

</details>

2. dockerを構築

```shell
$ docker-compose build
```

3. イメージをプルして来てコンテナを作成・実行

```shell
$ docker-compose up
$ docker-compose up -d # -d オプションでバックグラウンドで実行
```

4. swagger apiの確認

http://localhost:8000/docs#/

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

# テストコードについて

https://www.magata.net/memo/index.php?pytest%C6%FE%CC%E7
