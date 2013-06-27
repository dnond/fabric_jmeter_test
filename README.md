fabric_jmeter_test
==================

* 負荷試験は、サーバーの各種パラメータの調整を行いながら、同じテスト条件で何回も行なったりします。
* sshで毎度jmeterを叩いても良いのですが、fabricで楽に出来るようにしてみました。


# 使用例

````
$ fab env_vagrant doTest:jmx=/Users/hoge/Documents/jmx/test.jmx,config=auto,thread=10,loop=10,rampup=10
````
* ローカルのjmxファイルを指定して実行します。
* jmxは実行ごとにサーバーに転送（上書き）し、サーバー上でjmeterを実行します。
* logファイル等は、ExecConfigの各属性を設定します。
* config=autoを指定すると、jmxのファイル名・thread、rampup、loopの各値・日付から、出力ログファイル名を自動的に設定します。連番対応なので、jmeterを叩きまくってもOKです。

# 注意点など

* pythonの勉強がてら作ったので、文法等はビミョウかと思います。
* テストの環境はvagrantです。使用時は、任意のクラウドサーバー等にenvを変更してやってください。
