



# <div align = "right">ReD-DSL用户手册</div>















































**<div align = "right">2022 年 11月 20日</div>**

<div style="page-break-after:always"></div>


<div style="page-break-after:always"></div>

## 简介

Robotic efficiency Driven - Domain Specific Language(ReD-DSL)定义了一个定义一个领域特定脚本语言，这个语言能够描述在线客服机器人（机器人客服是目前提升客服效率的重要技术，在银行、通信和商务等领域的复杂信息系统中有广泛的应用）的自动应答逻辑，并设计实现一个解释器，可以解释执行这个脚本。该解释器可以根据用户的不同输入，根据脚本的逻辑设计给出相应的应答。

ReD-DSL主要有以下几个特点：

* ReD-DSL使用ply完备地描述了一个文法，可以进行用户输入值或变量的比较，并存在错误检出与恢复功能。
* ReD-DSL按照Google开源项目风格指南进行代码编写，各模块代码可读性强。
* ReD-DSL采用面向对象的编程方法，各个模块之间耦合度低，并且每个模块皆可独立运行。

* ReD-DSL将输入和应答逻辑封装为Restful API以供调用，接口作用明确，定义清晰。
* ReD-DSL实现了一个Web应用，因此可以将需要的机器人客服作为插件，嵌入在任意的网页中以满足不同的客户需求。

* ReD-DSL提供了各个模块的完整测试和测试桩，以及自动测试脚本。

* ReD-DSL支持多用户多并发处理，使用ORM的方式进行不同用户的数据管理，并且保证了线程的安全。
* ReD-DSL的演示程序中支持调用一个基于深度学习的自然语言预训练模型([ blenderbot-400M-distill](https://huggingface.co/facebook/blenderbot-400M-distill))，从而使得用户可以与机器人进行任意自然语言的交流，从而优化了程序的人机接口。

<img src="./README.assets/preview.gif" alt="移动端" style="zoom:50%;" />

<div style="page-break-after:always"></div>

## 语法定义

使用C语言标准BNF(*The C programming language*, 2nd edition, by Brian W. Kernighan and Dennis M. Ritchie,Prentice Hall, 1988.)进行定义

```
<script>				::= "script" <id> <variables_defination> <states_defination>
<variables_defination>  ::= "variable" <var_clauses> "endVariable"
<var_clauses>			::= <var_clause> | <var_clauses>  <var_clause>
<var_clause>			::= <identifier> "real" <variable> | <identifier> "integer" <variable> | <identifier> "text" <variable>
<states_defination> 	::= <state> | <states> <state>
<state>					::= "state" <identifier> <expressions> "endState"
<expressions>			::= <expression> | <expressions> <expression>
<expression>			::= <speak> | <switch> | <goto> | <timeout> | <exit> | <update>
<speak>					::= "speak" <terms>
<terms>					::= <term> | <terms> "+" <term> | <term> "PLUS" <term> | <term> "MINUS" <term>
<term>					::= <string> | <variable> | <identifier> | <return>
<switch> 				::= "switch" <cases> <default> "endSwitch" | "switch" <cases> "endSwitch"
<cases>					::= <case> | <cases> <case>
<case> 					::= "case" <string> <expressions> | "case" <return> <expressions> | "case" <compare> <expressions>
<compare>				::= <identifier> '>' <term> | <identifier> '<' <term> | <identifier> '>=' <term> | <identifier> '<=' <term> | <return> '>' <term> | <return> '<' <term> | <return> '>=' <term> | <return> '<=' <term>
<goto>					::= "goto" <identifier>
<timeout> 				::= "timeout" <variable> <expressions> "endTimeout"
<exit>					::= "exit"
<update>				::= "update" <identifier> "=" <terms>
<identifier> 			::= <letter_> | <identifier> <letter_> | <identifier> <number>
<variable>				::= "$" <letter_> | "$" <number> | <variable> <letter_>| <variable> <number>
<string> 				::= <letter_> | <number> | <string> <letter_> | <string> <number>
<letter_>				::= "_" | "A" | "B" | ... | "Z"| "a" | "b" | ... | "z"
<number>				::= "0" | "1" | "2" | ... | "9"
```

### 语法规定

* 每个语言脚本必须有一个welcome状态，作为程序的默认开始状态。
* 每个expressions可以由多个动作语句组成，包括speak、goto、timeout、exit、update等。
* 每个case状态内可以执行多条动作语句。
* case后可以使用字符串判定、用户输入判定和条件比较判定（判定用户输入值或某个用户变量是否符合条件）。

### 语法例子

用户手册提供一个语法例子，程序模拟了银行存取客户的逻辑。
```
script bank
variable
    x real $100
    y integer $100
    z text "hello"
endVariable

state welcome
    speak "Hello, welcome to the bank script"
    speak "Input [balance] to check your account's balance"
    speak "Input [topup] to top up your account"
    speak "Input [withdraw] to withdraw money from your account"
    speak "Input [exit] to exit the script"
    switch
        case "hello" 
            speak "hello"
            goto welcome
        case "balance"
            speak "Your balance is " + x
            goto welcome
        case "topup" 
            goto topup
        case "withdraw"
            goto withdraw
        case "exit" 
            goto goodbye
        default 
            speak "Unknown command, please try again"
            goto welcome
    endSwitch
    timeout $30 
        speak "You have been idle for 30 seconds. Restarting service ..."
        goto welcome
    endTimeout
endState

state withdraw
    speak "How much would you like to withdraw?"
    switch
        case _return <= x
            speak "You have withdrawn " + _return + " dollars"
            update x = x MINUS _return
            goto welcome
        case _return > x
            speak "You do not have enough money in your account!"
            goto welcome
    endSwitch
    timeout $30 
        speak "You have been idle for 30 seconds. Restarting service ..."
        goto welcome
    endTimeout
endState


state topup
    speak "How much would you like to top up?"
    switch
        case _return >= $0
            speak "You have topped up " + _return + " dollars"
            update x = x PLUS _return
            goto welcome
        case _return < $0
            speak "You cannot top up a negative amount!"
            goto welcome
    endSwitch
    timeout $30 
        speak "You have been idle for 30 seconds. Restarting service ..."
        goto welcome
    endTimeout
endState

state goodbye
    speak "Are you sure you want to exit?[yes/no]"
    switch 
        case "yes"
            exit
        case "no"
            goto welcome
        default
            speak "not quite understood"
    endSwitch
    timeout $30 
            goto welcome
    endTimeout
endState
```

<div style="page-break-after:always"></div>

## 部署指南

安装依赖：

```bash
pip install -r requirements.txt
```

编辑`server/config.json`:

```json
{
  "key": "secret", // jwt鉴权的secret
  "db_path": "database.db", // 数据库目录
  "script_path": "../test/script/test.txt", // 运行脚本目录
  "port": 9001 // 服务端运行端口
}
```

启动服务端：

```bash
cd ./server
python app.py
```

启动客户端：

```bash
cd ../client
yarn start
```

<div style="page-break-after:always"></div>

## 文件结构

```c
.
├── README.md //ReD-DSL用户手册
├── client //客户端文件夹
│   ├── README.md //客户端用户手册
│ 	│   ...
│   └── yarn.lock
├── config.json //ReD-DSL配置文件
├── script //可运行的脚本
│   ├── bank_service.txt //银行服务脚本
│   ├── echo.txt //echo脚本
│   ├── hello.txt //hello脚本
│   └── mobile_fee.txt //移动设备流量充值查询脚本
├── server //服务端文件夹
│   ├── __init__.py //python init标识
│   ├── app.py //后端flask API
│   ├── controller.py //控制器
│   ├── database.db	//默认数据库
│   ├── interpreter.py //解释器
│   ├── lexer.py //词法分析器
│   ├── parser.out //LALR1分析结果
│   ├── parsetab.py //ply中间文件
│   └── yacc.py //语法分析器
└── test //测试文件夹
    ├── __init__.py //python init标识
    ├── script //测试脚本
    │   ├── app_test //测试api
    │   │   ├── output1.txt
    │   │   ├── output2.txt
    │   │   └── output3.txt
    │   ├── controller_test //测试控制器
    │   │   ├── output1.txt
    │   │   ├── result1.txt
    │   │   └── test1.txt
    │   ├── interpreter_test //测试解释器
    │   │   ├── result1.txt
    │   │   ├── result2.txt
    │   │   ├── test1.txt
    │   │   └── test2.txt
    │   ├── parser_test //测试语法分析器
    │   │   ├── result1.txt
    │   │   ├── result2.txt
    │   │   ├── test1.txt
    │   │   ├── test2.txt
    │   │   ├── test3.txt
    │   │   └── test4.txt
    │   └── test.txt
    ├── stub //测试桩文件
    │   ├── ast.stub //语法树测试桩文件
    │   └── state_machine.stub //状态机测试桩文件
    ├── test_app.py //后端API自动测试脚本
    ├── test_client.py //测试客户端的测试桩
    ├── test_controller.py //控制器自动测试脚本
    ├── test_parser.py //语法分析器自动测试脚本
    ├── test_pressure.py //压力测试测试脚本
    ├── test_server.py //测试服务端的测试桩
    └── test_state_machine.py //状态机自动测试脚本
```

