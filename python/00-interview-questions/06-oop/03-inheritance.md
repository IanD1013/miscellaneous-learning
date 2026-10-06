继承（inheritance）让一个新类可以复用并特化一个已有的类。
新类（子类，subclass）获得它所继承的类（基类 base class 或超类 superclass）的属性和方法，并且可以添加新行为或替换继承来的行为。
本课涵盖子类化、重写（override）方法、用 `super()` 回调基类、运行时检查 `isinstance` 和 `issubclass`、每个类最终都继承自 `object` 这一事实、初步了解多重继承（multiple inheritance）和方法解析顺序（method resolution order，MRO），以及在继承不合适时作为替代方案的组合（composition）。

### 子类化

通过在括号中写出基类的名字来声明子类。
子类一开始就拥有基类提供的一切。

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"{self.name} is an animal"

class Dog(Animal):
    def speak(self):
        return "Woof"

d = Dog("Rex")
print(d.describe())   # Rex is an animal  （继承来的）
print(d.speak())      # Woof              （由 Dog 添加）
```

`Dog` 没有定义 `__init__` 或 `describe`，所以它使用 `Animal` 中的版本。
在子类上找不到的名字会到它的基类上查找。

### 重写方法

子类可以重新定义它继承来的方法。
对象实际类型上的版本优先。
这就是为什么同一个调用会根据对象的不同而做不同的事情，这正是人们所说的多态（polymorphism）。

```python
class Animal:
    def speak(self):
        return "..."

class Cat(Animal):
    def speak(self):
        return "Meow"

for a in [Animal(), Cat()]:
    print(a.speak())   # ...  然后  Meow
```

### `super().__init__` 和 super() 方法调用

当子类定义了自己的 `__init__` 时，基类的 `__init__` 就不再自动运行。
如果你希望执行基类的初始化设置，就用 `super().__init__(...)` 调用它。
对于任何你想扩展而不是替换的继承方法，同样的 `super()` 调用也适用。

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)   # 先运行 Animal 的初始化设置
        self.breed = breed

d = Dog("Rex", "Husky")
print(d.name, d.breed)   # Rex Husky
```

如果你忘了调用 `super().__init__(name)`，`self.name` 就永远不会被设置，访问 `d.name` 会抛出 `AttributeError`。
`super()` 返回一个分派到基类的代理（proxy），所以你不需要硬编码父类的名字。

### isinstance 和 issubclass

`isinstance(obj, Class)` 检查一个对象是否是某个类或其任意子类的实例。
`issubclass(A, B)` 检查类 `A` 是否就是 `B` 或派生自 `B`。
两者都接受一个类的元组，以便一次针对多个类进行检查。

```python
class Animal: pass
class Dog(Animal): pass

d = Dog()
print(isinstance(d, Dog))       # True
print(isinstance(d, Animal))    # True，Dog 派生自 Animal
print(issubclass(Dog, Animal))  # True
print(isinstance(d, (int, str)))# False，不是其中任何一个
```

`isinstance` 是推荐的检查方式，因为它考虑了继承。
`type(d) is Animal` 在这里会是 `False`，因为它忽略了子类化，要求精确匹配。

### 每个类都继承自 object

如果你写 `class Animal:` 而不指定基类，Python 仍然会把 `object` 作为基类。
所以每个类都是 `object` 的子类，每个值都是 `object` 的实例。

```python
class Animal: pass
print(issubclass(Animal, object))   # True
print(isinstance(42, object))       # True
```

在你重写之前，`__init__`、`__str__` 和 `__eq__` 等默认实现就来自这里。

### 多重继承和 MRO

一个类可以列出多个基类。
这时 Python 需要一个确定的顺序来在这些基类中查找属性。
这个顺序就是方法解析顺序（MRO），可以通过 `ClassName.__mro__` 或 `ClassName.mro()` 查看。

```python
class A:
    def who(self): return "A"

class B:
    def who(self): return "B"

class C(A, B):
    pass

print(C().who())     # A，在第一个列出的基类上找到
print([c.__name__ for c in C.__mro__])   # ['C', 'A', 'B', 'object']
```

Python 会为你计算出一个唯一且一致的顺序；你不需要手动推算。
左边列出的基类会先于右边列出的基类被查找，并且 `object` 总是排在最后。

### 组合作为替代方案

继承表示子类"是一种（is a）"基类。
当这一点不成立时，优先使用组合：把另一个对象作为属性持有，并委托（delegate）给它（"有一个，has a"）。
组合使类之间的耦合更松散，并避免很深的继承树。

```python
class Engine:
    def start(self):
        return "engine running"

class Car:
    def __init__(self):
        self.engine = Engine()   # Car 拥有一个 Engine

    def start(self):
        return self.engine.start()

print(Car().start())   # engine running
```

`Car` 不是一种 `Engine`，所以使用继承是错误的。
当"是一种"关系真正成立时才使用继承，否则使用组合。
