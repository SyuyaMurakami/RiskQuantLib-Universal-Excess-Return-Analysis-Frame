# Brinson业绩归因以及行业业绩归因
## 安装

本项目基于RiskQuantLib进行二次开发，便于进行Brinson归因，因子归因和行业归因。 安装RiskQuantLib后，使用：

`getRQL RiskQuantLib-Universal-Excess-Return-Analysis-Frame`

进行安装

## 使用

### 录入信息

首先录入持仓信息和持仓的每日涨跌幅，打开Data文件夹中的**holding.xlsx**文件，编辑在不同日期的持仓，tradingDate是持仓的日期，
belongTo是属于哪个组合，code是持仓证券的代码，name是持仓证券的名称，weight是持仓证券在该组合中的权重，rtn是持仓证券在当日的涨跌。
industry是持仓证券的行业。

要进行行业归因，必须要填写行业因子。

同理，打开Data文件夹中的**benchmark.xlsx**文件，其中的列名应该和**holding.xlsx**文件完全一样，在其中填写相应的值。保存后推出即可。

### 在录入信息时增加新的归因因子

您也可以在**holding.xlsx**文件中新增其他的列，但您需要将列名保持为英文，并在**Build_Attr.xlsx**中注册列名。
具体的注册方式为打开**Build_Attr.xlsx**，将新的列名填入AttrName栏，并将Security列填写为Stock（S必须大写），
AttrType可以填写Any，String，Number其中之一（首字母必须大写）。

之后您需要运行**build.py**来使得注册生效。

### Brinson归因
运行 **多期Brinson归因.py** 可以生成Brinson归因的结果。

在 **多期Brinson归因.py** 的源代码中，您可以看到（这些语句并不在源代码中的相邻位置，这里只是摘录）：

`benchmark_list.addSubPortfolioByAttr('industry')`

`fund_list.addSubPortfolioByBenchmark('industry')`

您可以通过更改**addSubPortfolioByAttr**函数里的参数来选择如何进行子组合的划分，Brinson归因中默认使用行业，
您可以更改为任何您想使用的因子，这个因子的名称即是您在**Build_Attr.xlsx**中注册的列名。


### 行业归因
运行 **行业归因.py** 可以生成行业归因的结果。

在 **行业归因.py** 的源代码中，您可以看到（这些语句并不在源代码中的相邻位置，这里只是摘录）：

`benchmark_list.addSubPortfolioByAttr('industry')`

`fund_list.addSubPortfolioByBenchmark('industry')`

`fund_list.calSubPortfolioBreakDown(['金融','冶金','机械制造','能源','电子'])`

您可以通过更改**addSubPortfolioByAttr**函数里的参数来选择如何进行子组合的划分，行业归因中默认使用行业，
您可以更改为任何您想使用的因子，这个因子的名称即是您在Build_Attr.xlsx中注册的列名。

您需要在**calSubPortfolioBreakDown**函数的参数中声明因子的值，未声明的因子将不会参与到归因中。以行业因子为例，
行业因子的值的种类有很多，这里传入了 **['金融','冶金','机械制造','能源','电子']** 作为参与归因的种类。

### 任意因子的归因

您可以通过增加任意的因子，对超额收益在任意因子上进行归因。增加任意因子的做法在上文中已经描述过。

对自定义因子的归因非常类似于行业归因，只需要把行业归因的源代码中涉及行业的部分换为您的自定义因子即可。
比如您在Data文件夹中的文件里增加了'marketCap'作为新的因子，在**行业归因.py**源码中，更改代码为：

`benchmark_list.addSubPortfolioByAttr('marketCap')`

`fund_list.addSubPortfolioByBenchmark('marketCap')`

`fund_list.calSubPortfolioBreakDown(['大盘','中盘','小盘'])`

# License
MIT

