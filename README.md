# DieFreak

DieFreak is a frequency chart calculator for tabletop gaming dice rolls. (That's "die" and "freq," get it?) 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Python 3 is the only thing required to run die-freak.

```
Give examples
```

### Installing

DieFreak is a free-standing python module with no installation required. For the time being, it is written to be invoked directly.

End with an example of getting some data out of the system or using it for a little demo

### Using die-freak

Using DieFreak is simple. It understands "Xdy" and "XdY choose Z" phrasing of tabletop dice rolls. (Alternatively "XdYcZ" will work, if you want something a little more compact.)

```
C:\Users\myuser>python DieFreak.py --roll "3d6"
Roll            Frequency
=========================
3               1
4               3
5               6
6               10
7               15
8               21
9               25
10              27
11              27
12              25
13              21
14              15
15              10
16              6
17              3
18              1
```

DieFreak will write directly to CSV files if you prefer, for convenient manipulation in your spreadsheet program of choice.

```
C:\Users\myuser>python DieFreak.py --roll "3d6" -o "3d6.csv"
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Eric Kolb** - *Initial work* - [goodsnek](https://github.com/goodsnek)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details