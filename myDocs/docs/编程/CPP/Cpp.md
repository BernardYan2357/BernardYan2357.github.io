# Cpp

## Demo

- [ ] 手写一个串口帧收发程序
- [ ] 参考 [dynibo](https://github.com/xiaojie-xue/dynibo) 写一个CPP版机器人运动学库


References:

- [C++ primer]()
- [C++教程 | 菜鸟教程](https://www.runoob.com/cplusplus/cpp-tutorial.html)
- [C++那些事](https://light-city.github.io/stories_things/cplusplusthings-quickstart/)
- [Coreloop](https://space.bilibili.com/525245479)
- [短的C++](https://space.bilibili.com/362867212/lists/6354480?type=season)

## C++标准

## Pointers

初始化指针：

```cpp
void* ptr = nullptr; // nullptr是c++11引入的关键字，等效于 NULL或0（0不是一个有效的地址）
int var = 67;
int* ptr = &var;
```

关于指针的类型：任意类型的指针本质上只是一个存储内存地址的 unsigned integer。如果我们给指针类型，这代表指针指向的地址对应的数据可能是我们给的类型

类型用来告诉编译器写入数据时要改变多大的内存：

```cpp
void* ptr = &var;
*ptr = 42; // 会报错：表达式必须是指向完整对象类型的指针
```

这是因为指针类型为 void，可能是 longlong 类型也可能是 uint8_t 类型，程序改变该地址的数据时不知道该改变多大的内存

## Class

类用于指定对象的**形式**，是一种用户自定义的数据类型，它是一种封装了数据和函数的组合
- 类中的数据称为成员变量，函数称为成员函数
- 类可以被看作是一种模板，可以用来创建具有相同属性和行为的多个对象

```cpp
class Player
{

};

Player player; // 类型为Player的变量player
```

类型为类的变量称作对象，创建对象的过程称作实例化

## Namespace

命名空间作为附加信息来区分不同库中相同名称的函数、类、变量等。使用了命名空间即定义了上下文。本质上，命名空间就是定义了一个范围

### 定义命名空间

使用 `namespace` 关键字来定义命名空间：

```cpp
namespace MySpace {
    int value = 100;
    void foo() {
        // function body
    }
}
```

在实践中，我们往往会在头文件中定义一个命名空间，并将类、函数、变量等声明放在命名空间内，然后在源文件中同样将类，函数的具体实现包裹在与头文件相同的命名空间内：

```cpp
namespace MySpace {

} // namespace MySpace (闭合大括号后加注释 // namespace xxx，便于阅读长文件时定位)
```

### 访问命名空间中的成员

- 使用作用域运算符 `::` 来访问命名空间中的成员：

```cpp
MySpace::value // 访问 MySpace 命名空间中的 value 变量
MySpace::foo() // 调用 MySpace 命名空间中的 foo 函数
```

- 使用 `using` 声明，只引入命名空间中的特定成员，之后可以直接使用成员名：

```cpp
using MySpace::value; // 引入 MySpace 命名空间中的 value 变量
value = 200; // 直接使用 value
```

- 使用 `using namespace` 指令，引入整个命名空间：

```cpp
using namespace MySpace; // 引入 MySpace 命名空间中的所有成员
value = 300;
foo();
```

标准 C++ 库的所有标识符都定义在 `std` 命名空间中，例如 `std::cout`、`std::vector`、`std::string` 等。使用 `using namespace std;` 可以直接使用这些标识符而不需要加 `std::` 前缀：

```cpp
using namespace std;
cout << "hello" << endl;
vector<int> vec;
```

实际开发中尽量避免使用 `using namespace std;` 等语句直接引入整个命名空间，否则会因为命名空间污染导致很多不必要的问题，所以更推荐显式使用 `std::` 前缀

### 命名空间的别名

可以使用 namespace 别名来简化长命名空间的引用：

```cpp
namespace MyVeryLongNamespaceName {
    // ...
}
namespace Short = MyVeryLongNamespaceName; // 定义别名
Short::someFunction(); // 使用别名访问
```

### 匿名命名空间

没有名字的命名空间，其成员只在当前编译单元（源文件）内可见，相当于 `static` 的全局变量：

```cpp
namespace {
    int counter = 0; // 只在当前文件中可见
    void helper() { }
}
```

## 线程

Prerequisites:

- [[计算机基础#线程、进程]]

References:

- [C++ 多线程](https://www.runoob.com/cplusplus/cpp-multithreading.html)

C++11 引入了多线程支持，其核心组件包括：

- std::thread：用于创建和管理线程
- std::mutex：用于线程之间的互斥，防止多个线程同时访问共享资源
- std::lock_guard 和 std::unique_lock：用于管理锁的获取和释放
- std::condition_variable：用于线程间的条件变量，协调线程间的等待和通知
- std::future 和 std::promise：用于实现线程间的值传递和任务同步

一个没有显式创建线程的 C++ 程序，运行时也至少有 1 个线程，也就是主线程（执行 main() 的线程），在`main()`函数里你仍可以操作这个线程，例如：

```cpp
#include <thread>
#include <chrono>
#include <iostream>
// 例如使用std::this_thread类中的静态成员函数来获取当前线程的id，并让主线程休眠一段时间：
int main() {
    std::cout << "main thread id = " << std::this_thread::get_id() << '\n';
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    return 0;
}
```

## STL

STL（Standard Template Library）是 C++ 标准库的一部分，提供了一套通用的数据结构和算法的实现，主要包括：容器、迭代器、算法、函数对象、适配器。STL 的设计理念是**泛型编程**，通过模板和迭代器将算法与数据结构解耦，使算法作用于任意满足迭代器要求的范围

STL 是有多个版本的，三个最为普遍的STL版本：

- `HP STL`：其他版本的C++ STL，一般是以HP STL为蓝本实现出来的，HP STL是C++ STL的第一个实现版本，而且开放源代码
- `P.J.Plauger STL`：由P.J.Plauger参照HP STL实现出来的，被Visual C++编译器所采用，不是开源的
- `SGI STL`：由Silicon Graphics Computer Systems公司参照HP STL实现，被Linux的C++编译器GCC所采用，SGI STL是开源软件，源码可读性甚高

### 迭代器

### 容器

references：

- [C++ Primer 第9，10章]()
- [[CoreLoop]浅谈std::vector的实现](https://www.bilibili.com/video/BV11Qv6BkE3t)

所有的容器都是类模板，容器容纳特定类型对象的集合，提供了统一的接口来访问和操作这些对象。C++标准库提供了多种容器类型，主要分为以下几类：

- 顺序容器，元素排列次序与插入顺序相同
  - vector：动态数组，支持随机访问，插入和删除效率较低
  - list：双向链表，不支持随机访问，支持高效的插入和删除
  - deque：双端队列，不支持随机访问，支持高效的插入和删除
- 顺序容器适配器，根据原始容器，定义新的操作接口
  - stack：栈，后进先出（LIFO）
  - queue：队列，先进先出（FIFO）
  - priority_queue：优先级队列，元素按照优先级排序
- 关联容器，元素按照特定规则进行组织
  - set：集合，存储唯一元素，自动排序
  - map：映射，存储键值对，键唯一，自动排序
  - multiset：多重集合，存储允许重复的元素，自动排序
  - multimap：多重映射，存储允许重复的键值对，自动排序

#### 容器的初始化

- 要使用容器，首先需要包含对应的头文件
- 定义容器时需要指定存储的元素类型，使用模板形参表`<typename T>`来指定

构造容器方法，以vector为例：

```cpp
std::vector<int> vec; // 默认构造函数，创建一个空的 vector
std::vector<int> vec2(vec); // 拷贝构造函数，创建一个 vec 的副本
std::vector<int> vec(5); // 创建一个包含 5 个默认值（0）的 vector
std::vector<int> vec(5, 10); // 创建一个包含 5 个值为 10 的 vector
std::vector<int> vec = {1, 2, 3, 4, 5}; // 列表初始化，创建一个包含 5 个元素的 vector
```

#### vector

vector 是一种动态数组，基于 array 实现。动态数组的特点是可以在运行时动态调整数组容量

vector 的成员函数：

```cpp
std::vector<int> vec = {1, 2, 3, 4, 5};

vec.begin() // 返回指向容器第一个元素的迭代器
vec.end() // 返回指向容器最后一个元素之后位置的迭代器
vec.rbegin() // 返回指向容器最后一个元素的反向迭代器
vec.rend() // 返回指向容器第一个元素之前位置的反向迭代器

vec.push_back(6) // 在容器末尾添加一个元素（复制 value，存储的是副本），容器长度加1
std::vector<std::vector<int>> vec2;
vec2.push_back({1, 2, 3}); // 使用大括号列表初始化来构造一个临时的 vector<int> 对象，并将其添加到 vec2 的末尾，容器长度加1
vec.emplace_back(7) // 在容器末尾直接构造一个元素，避免了复制的开销，容器长度加1
vec.push_front(0) // 在容器开头添加一个元素，容器长度加1
vec.pop_back() // 删除容器末尾的元素，容器长度减1
vec.pop_front() // 删除容器开头的元素，容器长度减1
vec.insert(vec.begin(), 10) // 在容器开头插入一个元素，insert函数在迭代器指向位置之前插入，容器长度加1
vec.erase(vec.begin()) // 删除容器开头的元素，容器长度减1
vec.clear() // 清空容器中的所有元素

vec.size() // 返回容器中元素的数量
vec.max_size() // 返回容器能够容纳的最大元素数量
vec.empty() // 返回一个布尔值，表示容器是否为空
vec.resize(10, 1) // 将容器的大小调整为 10，如果新的大小大于当前大小，则在末尾添加元素，添加的元素可以用第二个参数指定，默认为0；如果新的大小小于当前大小，则删除末尾的元素

// 注意，任何修改容器内容的操作都会使所有指向容器元素的迭代器失效，因此在使用这些操作后，应该重新获取迭代器

vec.back() // 返回容器最后一个元素的引用
vec.front() // 返回容器第一个元素的引用
vec[index] // 返回容器中指定位置元素的引用，index 从 0 开始
vec.at(index) // 返回容器中指定位置元素的引用，index 从 0开始，at函数会进行边界检查，如果index超出范围，会抛出std::out_of_range异常
```

#### list

list 是一种双向链表，链表详情查阅[[数据结构与算法#链表]]

list 的成员函数：

```cpp
std::list<int> lst = {1, 2, 3, 4, 5};
lst.begin() // 返回指向容器第一个元素的迭代器
lst.end() // 返回指向容器最后一个元素之后位置的迭代器
lst.rbegin() // 返回指向容器最后一个元素的反向迭代器
lst.rend() // 返回指向容器第一个元素之前位置的反向迭代器
lst.push_back(6) // 在容器末尾添加一个元素，容器长度加1
lst.push_front(0) // 在容器开头添加一个元素，容器长度加1
lst.pop_back() // 删除容器末尾的元素，容器长度减1
lst.pop_front() // 删除容器开头的元素，容器长度减1
lst.insert(lst.begin(), 10) // 在容器开头插入一个元素，insert函数在迭代器指向位置之前插入，容器长度加1
lst.erase(lst.begin()) // 删除容器开头的元素，容器长度减1
lst.clear() // 清空容器中的所有元素
lst.size() // 返回容器中元素的数量
```

#### stack

栈是以底层容器完成其所有的工作，对外提供统一的接口，底层容器是可插拔的（也就是说我们可以控制使用哪种容器来实现栈的功能），这就是为什么 stack 归属于容器适配器。可以选择的底层容器有 vector、deque 和 list，常用的 SGI STL 默认使用 deque 作为栈的底层实现，也可以自己指定：

```cpp
std::stack<int, std::vector<int>> s; // 使用 vector 作为 stack 的底层容器
```

栈提供 push() 和 pop() 等接口，所有元素必须符合**先进后出**规则，所以栈不提供走访功能，也不提供迭代器(iterator)，下面是 stack 的成员函数：

```cpp
std::stack<int> s;
s.push(1) // 在栈顶添加一个元素，栈长度加1
s.pop() // 删除栈顶的元素，栈长度减1
s.top() // 返回栈顶元素的引用
s.size() // 返回栈中元素的数量
s.empty() // 返回一个布尔值，表示栈是否为空
```

stack 转 string 的方法：

```cpp
std::stack<char> s;
std::string str;
while (!s.empty()) {
    str += s.top();
    s.pop();
}
reverse(str.begin(), str.end()); // 反转字符串
```

#### queue

与 stack 类似，queue 也是以底层容器完成其所有的工作，对外提供统一的接口，底层容器可以选择 vector、deque 和 list，SGI STL中队列一样是以 deque 为缺省情况下的底部结构，同样可以自己指定：

```cpp
std::queue<int, std::list<int>> q; // 使用 list 作为 queue 的底层容器
```

queue 提供`push()`和`pop()`等接口，所有元素必须符合**先进先出**规则，所以 queue 不提供走访功能，也不提供迭代器，下面是 queue 的成员函数：

```cpp
std::queue<int> q(0); // 创建一个空的 queue
q.push(1) // 在队列末尾添加一个元素，队列长度加1
q.pop() // 删除队列开头的元素，队列长度减1
q.front() // 返回队列开头元素的引用
q.back() // 返回队列末尾元素的引用
q.size() // 返回队列中元素的数量
q.empty() // 返回一个布尔值，表示队列是否为空
```

priority_queue 是一种特殊的队列，元素按照优先级排序，优先级高的元素先出队，底层容器默认使用 vector 实现，提供`push()`和`pop()`等接口，其成员函数与 queue 类似：

#### set

set，集合，区别于vector，set中的元素是唯一的，不能重复的

| 集合 | 底层实现 | 是否有序 | 数值是否可以重复 | 能否更改数值 | 查询效率 | 增删效率 |
| --- | --- | --- | --- | --- | --- | --- |
| std::set | 红黑树 | 有序 | 否 | 否 | O(log n) | O(log n) |
| std::multiset | 红黑树 | 有序 | 是 | 否 | O(logn) | O(logn) |
| std::unordered_set | 哈希表 | 无序 | 否 | 否 | O(1) | O(1) |

`std::unordered_set`底层实现为哈希表，`std::set`和`std::multiset`的底层实现是红黑树。红黑树是一种平衡二叉搜索树，所以key值是有序的，但key不可以修改，改动key值会导致整棵树的错乱，所以只能删除和增加。

当我们要使用集合来解决哈希问题的时候，优先使用unordered_set，因为它的查询和增删效率是最优的，如果需要集合是有序的，那么就用set，如果要求不仅有序还要有重复数据的话，那么就用multiset

set的成员函数：

```cpp
std::set<int> s = {1, 2, 3, 4, 5}; // 列表初始化，创建一个包含 5 个元素的 set
s.insert(1); // 插入一个元素，如果元素已经存在，则返回一个指向该元素的迭代器，并且不插入新元素；如果元素不存在，则插入新元素并返回一个指向新元素的迭代器
s.erase(1) // 删除一个元素，如果元素不存在，则删除失败
s.find(1) // 返回一个迭代器，指向元素 1，如果元素不存在，则返回 s.end()
s.size() // 返回 set 中元素的数量
s.empty() // 返回一个布尔值，表示 set 是否为空
s.count(1) // 返回元素 1 在 set 中出现的次数，set 中的元素是唯一的，因此返回值只能是 0 或 1
```

数组与set的相互转化：

```cpp
std::vector<int> vec = {1, 2, 3, 4, 5};
std::set<int> s(vec.begin(), vec.end()); // 使用迭代器范围构造函数将 vector 中的元素插入到 set 中，自动去重并排序
std::set<int> s = {1, 2, 3, 4, 5};
std::vector<int> vec(s.begin(), s.end()); // 使用迭代器范围构造函数将 set 中的元素插入到 vector 中，元素顺序与 set 中的顺序相同
```

#### map

map 是一种关联容器，存储键值对，键唯一，自动排序，以下是几种类型对比：

| 映射 | 底层实现 | 是否有序 | 数值是否可以重复 | 能否更改数值 | 查询效率 | 增删效率 |
| --- | --- | --- | --- | --- | --- | --- |
| std::map | 红黑树 | key有序 | key不可重复 | key不可修改 | O(logn) | O(logn) |
| std::multimap | 红黑树 | key有序 | key可重复 | key不可修改 | O(log n) | O(log n) |
| std::unordered_map | 哈希表 | key无序 | key不重复 | key不可修改 | O(1) | O(1) |

三种类型有统一的成员函数：

```cpp
std::unordered_map<char, char> pairs = {
    {')', '('}, {']', '['}, {'}', '{'}
};
pairs[')'] // 返回与键 ')' 对应的值，即 '('
pairs.find(']'); // 返回一个迭代器，指向键 ']' 对应的键值对，如果键不存在，则返回 pairs.end()
pairs.insert({'>', '<'}) // 插入一个键值对，如果键 '>' 已经存在，则插入失败
pairs['>'] = '<'; // 插入或更新键 '>' 对应的值为 '<'，如果键 '>' 已经存在，则更新其对应的值为 '<'；如果键 '>' 不存在，则插入一个新的键值对 {'>', '<'}
pairs.erase('}') // 删除键 '}' 对应的键值对
pairs.size() // 返回 unordered_map 中键值对的数量
pairs.empty() // 返回一个布尔值，表示 unordered_map 是否为空
pairs.count('}') // 返回键 '}' 在 unordered_map 中出现的次数，unordered_map 中的键是唯一的，因此返回值只能是 0 或 1
pairs.first // 返回一个迭代器，指向 unordered_map 中第一个键值对的键，也可以写成 pairs->first
pairs.second // 返回一个迭代器，指向 unordered_map 中第一个键值对的值，也可以写成 pairs->second

```

map 转 vector：

```cpp
for (const auto& pair : pairs) { // 使用范围 for 循环遍历 unordered_map 中的每个键值对，pair 是一个 std::pair<const char, char> 类型的变量，pair.first 是键，pair.second 是值
    vec.push_back(pair.second); // 将值插入到 vector 中
}
```

### 算法

STL 提供了丰富的算法，算法通常以函数模板的形式定义在 `<algorithm>` 头文件中，算法可以作用于任何满足迭代器要求的范围，因此可以与 STL 中的各种容器配合使用

#### 排序算法

- `sort`：基于快速排序算法实现，平均时间复杂度为 O(n log n)，最坏时间复杂度为 O(n^2)，空间复杂度为 O(log n)
- `stable_sort`：基于归并排序算法实现，平均时间复杂度为 O(n log n)，最坏时间复杂度为 O(n log n)，空间复杂度为 O(n)
- `partial_sort`：基于快速排序算法实现，平均时间复杂度为 O(n log k)，最坏时间复杂度为 O(n^2)，空间复杂度为 O(log k)，其中 k 是需要排序的元素数量

用法：

```cpp
sort(arr.begin(), arr.end()); // 使用 sort 对整个数组进行排序，参数为数组的起始迭代器和结束迭代器
stable_sort(arr.begin(), arr.end()); // 使用 stable_sort 对整个数组进行稳定排序
partial_sort(arr.begin(), arr.begin() + k, arr.end()); // 使用 partial_sort 对前 k 个元素进行排序
```

上面的几个排序算法默认返回的是升序排列，可以使用第三个参数指定比较规则。第三个参数是一个函数对象，必须返回一个bool值，bool值为true时表示第一个参数排在第二个参数之前，默认情况下，排序算法使用`std::less<T>()`作为比较函数（less 是一个函数对象，定义在 `<functional>` 头文件中，表示小于关系），例如：

```cpp
sort(arr.begin(), arr.end(), std::less<int>()); // 如果a<b返回true，则a排在b之前，升序排列
```

如果需要降序排列，可以使用`std::greater<T>()`作为第三个参数（greater 是一个函数对象，定义在 `<functional>` 头文件中，表示大于关系），广义上讲，任意的参数为两个类型为要排序的元素的，返回bool值的函数对象都可以作为第三个参数来指定排序规则

例如：你可以在一个二维向量中用列向量的大小关系排列行向量：[根据第 K 场考试的分数排序](https://leetcode.cn/problems/sort-the-students-by-their-kth-score)：

```cpp
vector<vector<int>> sortTheStudents(vector<vector<int>>& score, int k) {
    // 要排序的是score中的行向量，类型为 vector<int>，排序的依据是每个行向量中的第k个元素的大小关系
    sort(score.begin(), score.end(), [&k](const vector<int>& u, const vector<int>& v){ // 使用 & 声明两个形参，是避免 sort 函数比较时反复拷贝，使用 const 是为了预防你在比较函数中修改传入的参数
        return u[k]>v[k];
    });
    return score;
}
```

#### 其它算法

```cpp
reverse(str.begin(), str.end()) // 反转迭代器范围内的元素
swap(a, b) // 交换两个元素的值
```

## 语法

### 类型

- char：字符类型，通常占用 1 字节，表示一个字符，例如：

    ```cpp
    char c = 'A'; // c 的值是字符 'A'
    ```

    一些处理字符的函数：

    ```cpp
    isdigit(c) // 判断字符 c 是否为数字字符
    isalpha(c) // 判断字符 c 是否为字母字符
    isupper(c) // 判断字符 c 是否为大写字母
    islower(c) // 判断字符 c 是否为小写字母
    toupper(c) // 将字符 c 转换为大写字母
    tolower(c) // 将字符 c 转换为小写字母
    ```

- auto：自动类型推断，编译器根据变量的初始化表达式来推断变量的类型，简化代码，增强可读性，尤其在声明复杂类型时非常有用，例如：

    ```cpp
    auto x = 5; // x 的类型被推断为 int
    auto y = 3.14; // y 的类型被推断为 double
    auto z = "Hello"; // z 的类型被推断为 const char*
    ```

- size_t：无符号整数类型，通常用于表示对象的大小或容器的索引，定义在 `<cstddef>` 头文件中，size_t 的大小取决于平台和编译器，通常是 32 位或 64 位，size_t 的值范围从 0 到最大可表示的值，例如：

    ```cpp
    size_t n = 10; // n 的类型是 size_t，可以存储一个非负整数
    std::vector<int> vec(n); // 创建一个包含 n 个元素的 vector
    ```

### 智能指针

- [(CoreLoop)智能指针：防止内存泄漏最有效的手段](https://www.bilibili.com/list/watchlater?bvid=BV1rdAVzAEqf)

在C++中，我们可以使用`new`和`delete`来动态分配和释放内存，这种手动管理内存的方式容易导致**内存泄漏**，有以下几种情况：

- 忘记调用delete来释放内存，导致内存泄漏
- 在new与delete之间发生异常，导致delete无法执行，内存泄漏
- 在另一个线程中访问已经被delete释放的内存，导致悬空指针

在C++11中引入了智能指针（smart pointer），它是一种类模板，封装了原始指针，并提供了自动内存管理功能，智能指针有以下三种：

- std::unique_ptr：独占所有权的智能指针，不能被复制，只能被移动
  - 当指针生命周期结束后自动释放内存
  - 几乎零开销，性能等同于原始指针
- std::shared_ptr：共享所有权的智能指针，多个 shared_ptr 可以指向同一个对象
  - 使用强引用计数(strong_count)来管理对象的生命周期，当最后一个 shared_ptr 的生命周期结束时，自动释放内存
  - 开销较大，只有当确实需要共享所有权时才使用
- std::weak_ptr：弱引用智能指针

原理分析：

- unique_ptr实现独占所有权的方法是在unique_ptr类中将拷贝操作声明为`delete`，使其无法被外部调用。因此，将两个unique_ptr指向同一个地址其实不会在编译时报错：

    ```cpp
    int* p =new int(3);
    unique_ptr<int> up1(p);
    unique_ptr<int> up2(p);
    // 但是在执行时由于up1先析构，p所指内存被释放，会导致up2析构时delete无效指针p，触发堆内存断言失败
    ```

- shared_ptr的成员除了一个原生指针外，还包含一个指向控制块的指针，控制块中维护了一个强引用计数（strong_count）和一个弱引用计数（weak_count）。当shared_ptr被复制时，强引用计数增加；当shared_ptr被销毁时，强引用计数减少；当强引用计数为0时，释放内存，观看下例：

    ```cpp
    int* p =new int(3);
    shared_ptr<int> sp1(p);
    shared_ptr<int> sp2(p);
    // 由于并未经过shared_ptr的拷贝构造函数，所以sp1和sp2的控制块是不同的，sp1和sp2的强引用计数都是1，同样，sp1先delete p，导致sp2析构时delete无效指针p，触发堆内存断言失败
    // 正确的做法应该是：
    int* p =new int(3);
    shared_ptr<int> sp1(p);
    shared_ptr<int> sp2 = sp1; // 通过拷贝构造函数来创建sp2，这样sp1和sp2共享同一个控制块，强引用计数为2，当sp1析构时，强引用计数减1，变为1；当sp2析构时，强引用计数减1，变为0，此时自动释放内存p，不会触发堆内存断言失败
    ```

shared_ptr 和 unique_ptr 的使用：

```cpp
#include <memory>
void foo_s() {
    std::shared_ptr<int> sp1 = std::make_shared<int>(10); // 创建一个 shared_ptr
    std::shared_ptr<int> sp2 = sp1; // sp2 初始化，拷贝构造
    if (sp1) { // or if (sp1 != nullptr)
        std::cout << *sp1 << std::endl; // 输出 10
    }
}
void foo_u() {
    std::unique_ptr<int> up1 = std::make_unique<int>(20); // 创建一个 unique_ptr
    std::unique_ptr<int> up2 = std::move(up1); // up2 接管 up1 的所有权，up1 变为空指针
    if (up1) {
        std::cout << *up1 << std::endl; // 不会执行，因为 up1 已经没有所有权了
    }
}
```

- `<int>`表示指针所指的元素类型，这是类模板的语法
- 不仅可以通过`make_shared()`和`make_unique()`来创建智能指针对象，还可以直接使用构造函数来创建，例如：

    ```cpp
    std::unique_ptr<int> up(new int(10)); // 直接使用构造函数创建 unique_ptr
    int* p = new int(20);
    std::shared_ptr<int> sp(p); // 直接使用构造函数创建 shared_ptr
    // 注意第二种写法，p是一个原始指针，sp接管了p的所有权，sp生命周期结束时会自动释放p指向的内存，因此不应该再使用p来访问内存，否则会导致悬空指针问题
    ```

智能指针的方法：

```cpp
//p是一个shared_ptr
p.use_count() // 当前强引用数
p.reset() //释放当前对象
p.reset(new int(4)) //使指针指向新对象，当前对象的strong_count--
p.get() // 获取裸指针
p.unique() //返回bool,表示是否只有一个引用

// p是一个unique_ptr
p.get() // 获取裸指针
p.release() //返回裸指针,p变为nulLptr,不会自动deLete,需要手动deLete裸指针
p.reset(); // 删除当前对象
p.reset(new T()); // 删除旧对象,接管新对象
p1.swap(p2); // 交换p1和p2的所有权，类似于move语义，效率更高
```

### 所有权

### 左值和右值

references：

- [C++移动语义，右值引用，std::move()深入理解 | coreloop](https://www.bilibili.com/video/BV1UjvZB8En5)
- [彻底搞懂C++移动语义/左值/右值/引用 | 安枫的叶](https://www.bilibili.com/video/BV17ce7zLEzu)

在 C++11 标准中引入了移动语义与右值引用的概念，规定任何一个表达式都精确属于 lvalue、xvalue、prvalue 这三种值类别中的一种

- lvalue（纯左值）：表示一个“有身份”的对象，可以持续地找到它，通常是一个变量或者一个函数返回的引用

  ```cpp
  int x = 5; // x 是一个 lvalue，可以取地址
  int* p = &x; // p 是一个指向 x 的指针，p 是一个 lvalue
  ```

- prvalue（纯右值）：表示一个“没有身份，只关心值”的对象，通常是一个临时对象或者一个函数返回的非引用类型
  
  ```cpp
  42 // 42 是一个 prvalue，表示一个临时对象，没有身份
  x+y // x+y 是一个 prvalue，表示一个临时对象，没有身份
  int add(int a, int b){return a + b;}
  add(1, 2) // add(1, 2) 是一个 prvalue，表示一个临时对象，没有身份
  ```

- xvalue（将亡值）：表示一个“即将销毁”的对象，xvalue 形右实左，是一个贴上了“语义”标签的左值，表明这个资源是“将亡的”，有这个标签，在变量赋值时就会触发移动构造函数，而不是拷贝构造函数，例如：

  ```cpp
  int a  = 5;
  int&& b = std::move(a); // 使用 std::move() 将 a 转换为一个 xvalue，触发 a 的移动构造函数，b 接管了 a 的资源，a 变为空值
  ```

#### 左值引用和右值引用

- 左值引用（lvalue reference）是必须绑定到 lvalue 上的引用类型，使用`&`符号表示，例如：

  ```cpp
  int x = 5;
  int& r = x; // r 是一个左值引用，绑定到一个左值 x 上
  r = 10; // 通过 r 修改 x 的值，x 变为 10
  ```

- 右值引用（rvalue reference）是必须绑定到 xvalue 或 prvalue 上的引用类型，使用`&&`符号表示，例如：

  ```cpp
  int&& r = 5; // r 是一个右值引用，绑定到一个右值 5 上
  r = 10; // 通过 r 修改 5 的值，5 变为 10，但由于 5 是一个临时对象，这种修改没有实际意义
  ```

任意返回右值引用的函数其值类别都为 xvalue，上面提到的`std::move()`函数就是返回右值引用，可以发现，`std::move()`函数的作用就是将传入的 lvalue 类别的变量转换为 xvalue 类别的变量，`std::move()`函数的实现如下：

```cpp
template <typename T>
typename remove_reference<T> :: type&& move(T&& t) { // T&& 是一个万能引用，可以接受T类型，T的引用类型(T&)，T的右值引用类型(T&&)的参数，remove_reference可以去除引用
return static_cast<typename remove_reference<T> :: type&&>(t); // 将参数t转换为一个右值引用
}
```

所以直接调用 std::move() 并不能天然地实现资源的移动，其实现本质上就是一个强制类型转换。移动构造函数内应该自行实现资源所有权转移，并将原始资源设置为空

为什么说 xvalue 本质上是一个贴上了“语义”标签的左值呢？我们可以通过下面的例子来理解：

```cpp
int a = 5;
int& b = a; // b 是一个左值引用，绑定到一个左值 a 上
int&& c = std::move(a); // c 是一个右值引用，绑定到一个 xvalue std::move(a) 上
cout << a << endl; // 5
b = 10;
cout << a << endl; // 10
c = 15;
cout << a << endl; // 15
```

可以发现不论是左值引用还是右值引用，都能够修改 a 的值，这说明 b 和 c 都绑定到了左值 a 上，c 只是一个贴上了“语义”标签的左值

### for 循环

for 循环语法:

```cpp
for (初始化表达式; 条件表达式; 更新表达式) {
    // loop body
}
```

三个表达式中，可以省略任何一个，但分号不能省略，例如：

```cpp
for (int i=0, j=k; i < j;) {
    // loop body
    // 需要在循环体内手动更新 i 和 j 的值，否则会导致死循环
}
```

`range-based for`循环是C++11引入的语法糖，提供了一种简洁而直观的方式来遍历一个序列或容器中的元素

```cpp
for (元素类型 变量名 : 要遍历的容器) {
    // loop body
}
```

例如，遍历一个string中的每个字符：

```cpp
std::string str = "Hello, World!";
for (char c : str) {
    std::cout << c << ' ';
}
```

### Lambda

Lambda 表达式是一种匿名函数，可以直接在需要函数对象的地方定义和使用，语法如下：

```cpp
[capture](parameters) -> return_type {
    // function body
}
// 也可以不要"-> return_type"，编译器会自动推断返回类型
[](parameters){/* function body */}
```

- capture：捕获列表，指定 lambda 表达式可以访问哪些外部变量
- parameters：参数列表，类似于普通函数的参数列表
- return_type：返回类型，可以省略，编译器会自动推断

使用方式：

1. 可以直接给变量赋值，例如：

    ```cpp
    auto add = [](int a, int b) -> int {
        return a + b;
    };
    ```

    利用这一点，可以将lambda表达式直接作为函数的参数或返回值

2. 直接在需要函数对象的地方定义和使用，例如：

    ```cpp
    std::vector<int> vec = {1, 2, 3, 4, 5};
    std::transform(vec.begin(), vec.end(), vec.begin(), [](int x){return x * x;});
    ```

3. 参数绑定与重排：[[Cpp#bind()]]

    lambda 支持类型多态，可以使用auto参数来实现泛型编程，例如：

    ```cpp
    auto add = [](auto a, auto b) {
        return a + b;
    };
    std::cout << add(1, 2) << std::endl; // 输出 3
    std::cout << add(1.5, 2.5) << std::endl; // 输出 4.0
    ```

    这也就是为什么一般lambda表达式可以不写return_type，因为编译器会根据返回语句自动推断返回类型，因此，当要使用lambda给变量赋值时，都指定变量为auto类型

### bind()

std::placeholders 命名空间（自 C++11 引入）提供了一组占位符对象，如 _1,_2, _3, ...,_N。它们主要用于与 std::bind 函数模板一起使用。std::bind 是一个函数模板，可以将一个可调用对象（如函数、成员函数、函数对象）与特定的参数绑定在一起，**生成一个新的可调用对象**。它的语法如下：

```cpp
std::bind(callable, arg1, arg2, ..., argN); // callable 是要绑定的函数或函数对象，arg1, arg2, ..., argN 是要绑定的参数，可以是具体的值，也可以是占位符
```

使用场景：

- 参数绑定: `std::bind()`可以将一个函数与特定的参数绑定在一起，生成一个新的可调用对象。例如将类中的函数剔除`self`参数，生成一个新的函数对象：

    ```cpp
    using namespace std::placeholders;
    ```cpp
    // 在 ROS2 的动作服务器中，使用 std::bind 将成员函数绑定为回调函数
    action_server_ = rclcpp_action::create_server<ActionType>(
        this, "action_name", // 动作名称
        std::bind(&ActionServer::handle_goal, this, _1),
        std::bind(&ActionServer::handle_cancel, this, _1),
        std::bind(&ActionServer::handle_accepted, this, _1)
        );
    // 这里，handle_goal、handle_cancel 和 handle_accepted 是 ActionServer 类的成员函数
    // 把原函数里的第一个this固定位置，同时指定第二个参数为新函数里面的第一个参数，所以新函数里不存在this参数
    // 这样就可以将成员函数作为回调函数传递给 create_server，而不需要担心成员函数的 this 指针问题
    ```

- 参数重排：std::bind 还可以改变参数的顺序，例如：

    ```cpp
    using namespace std::placeholders;
    some_function(int a, int b){return a - b;};
    std::cout << some_function(10, 20); // 输出 -10
    auto func = std::bind(some_function, _2, _1);
    std::cout << func(10, 20); // 输出 10，因为 _1 被替换为 20，_2 被替换为 10
    ```

自C++11引入了 lambda 表达式后，lambda表达式就可以替代 std::bind 的很多功能了，自C++14后，lambda表达式支持了类型多态与移动语义，可以完全取代 std::bind 的功能了，通常来说，如果你能用 Lambda 表达式实现需求，那就应该优先选择 Lambda：

```cpp
// 原函数
somefunction(int a, int b){return a - b;};
// lambda实现参数绑定
auto func = [](int a) {return some_function(a, 42);}; // 直接在 lambda 内部重排参数
// lambda实现参数重排
auto func = [](int a, int b) {return some_function(b, a);}; // 直接在 lambda 内部重排参数
```

### 结构体

在 C++ 中，结构体（struct）是一种用户定义的数据类型，用于将不同类型的数据组合在一起。结构体与类（class）非常相似，唯一的区别是结构体的成员默认是 public 的，而类的成员默认是 private 的

结构体可以拥有成员变量和成员函数，构造函数，析构函数，访问控制等特性。结构体的定义和使用方式如下：

```cpp
struct Person {
    std::string name;
    int age;
    Person(const std::string& n, int a) : name(n), age(a) {}
};
```

- 定义结构体时使用关键字 struct，后跟结构体名称和花括号
- 结构体成员可以是任何类型，包括基本类型、指针、数组、其他结构体等
- 结构体可以定义构造函数来初始化成员变量，语法为`StructName(parameters) : member1(value1), member2(value2) {}`，在构造函数体内可以执行其他初始化操作，这样，在实例化结构体时就可以直接传递参数来初始化成员变量，例如：

```cpp
Person person("Alice", 30); // 创建一个 Person 实例，name 初始化为 "Alice"，age 初始化为 30
```

### string

string 是 C++ 标准库提供的一个类，用于表示和操作字符串。string 类有如下成员函数:

```cpp
std::string str = "Hello, World!";
str.length() // 返回字符串的长度
str.size() // 返回字符串的长度，length 和 size 是等价的
str.empty() // 返回一个布尔值，表示字符串是否为空
str.append("How are you?") // 在字符串末尾添加一个子字符串，返回修改后的字符串
str.substr(0, 5) // 返回字符串的子串，从索引 0开始，长度为 5，即 "Hello"
str.find("World") // 返回子字符串 "World" 在字符串中的索引位置，如果找不到，则返回 std::string::npos
str.replace(7, 5, "Universe") // 替换字符串中从索引 7 开始，长度为 5 的子串为 "Universe"，返回修改后的字符串
str[0] // 返回字符串中索引为 0 的字符，即 'H'
str.at(0) // 返回字符串中索引为 0 的字符，即 'H'，与 operator[] 不同的是，at函数会进行边界检查，如果索引超出范围，会抛出 std::out_of_range 异常
```

> 在 C++ 中，用`“”`括起来的表示string，用`''`括起来的表示char

string 可以认为是 `vector<char>`的一个特例，string 内部维护了一个动态数组来存储字符，因此，它也可以使用 vector 的一些成员函数，例如：

```cpp
string path;
path.push_back('/');
path.pop_back();
```

string 转 char/int 的方法：

```cpp
std::string str = "H";
char c = str[0]; // 将 string 中的第一个字符赋值给 char 变量
int i = std::stoi(str); // 将 string 转换为 int 变量
```

## 库

### chrono

chrono 是 C++11 引入的一个库，用于处理时间和日期，提供了高精度的时间点、时间段和时钟等功能。chrono 库中的核心概念包括：

- time_point：表示一个特定的时间点，通常与某个时钟相关联
- duration：表示两个时间点之间的时间长度，可以使用不同的时间单位（如秒、毫秒、微秒等）
- clock：提供了获取当前时间点的功能，常用的时钟有 system_clock（系统时钟）和 steady_clock（稳态时钟）

一个简单的超时触发器的实现：

```cpp
using namespace std::chrono_literals; // 启用时间字面量，例如 5s 表示 5 秒，1ms 表示 1 毫秒
const auto timeout = 5s; // 设置超时时间为 5 秒
const auto start = steady_clock::now(); // 记录开始时间
  while (steady_clock::now() - start > timeout) {
      // 执行一些操作
  }
```

### Eigen

References: [Eigen](https://libeigen.gitlab.io/)

Eigen 是一个 C++ 模板库，用于线性代数、矩阵和向量运算，提供了高效的矩阵和向量操作，支持各种矩阵分解和求解方法，广泛应用于计算机视觉、机器学习、物理模拟等领域

### Boost

References: 

- [Boost](https://www.boost.org/)
- [Boost C++ 库](https://wizardforcel.gitbooks.io/the-boost-cpp-libraries/content/1.html)

The Boost C++ Libraries are open source, peer-reviewed, portable and free. 包含 160 余个库 / 组件 , 涵盖字符串与文本处理、容器、迭代器、算法、图像处理、模板元编程、并发编程等多个领域。也被称为准 C++ 标准库

#### Asio

Boost.Asio is a cross-platform C++ library for network and low-level I/O programming that provides developers with a consistent asynchronous model using a modern C++ approach