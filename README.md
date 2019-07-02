# typeidea
《Django企业开发实战》练手项目-Blog



# 5.3Model层 字段介绍

## 5.3.1ORM基本概念

ORM(Object Relational Mapping，对象关系映射)

“对象关系映射”，就是把我们自定义的对象（类）映射到对应的数据库的表上。所以ORM就是代码（软件）层面对于数据库表和关系的一种抽象。

## 5.3.2常用字段类型

### 数值型

+ AutoField int(11)

  自增主键，Django Model提供默认，可以被重写。它的完整定义是`id=models.AutoField(primary_key = True)`

+ BooleanField tinyint(1)

  布尔类型字段，一般用于记录状态标记

+ DecimalField decimal

  开发对数据精度要求较高的业务时考虑使用，比如做支付相关、金融相关。定义时，需要制定精确到多少位，比如 `cash=model.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="消费金额")`，就是定义长度为8位，精度位2位的数字。比方说，你想保存666.66扎样的数字，那么你的max_digits就需要为5，decimal_places需要为2

  同时需要注意，在Python中也要使用Decimal类型来转换数据(`from decimal import Decimal`)

+ IntegerField int(11) 

  它同AutoField一样，唯一的差别就是不自增

+ PositiveIntegerField

  同IntergerField，只包含正整数

+ SmallIntergerField smallint

  小整数时一般会用到

### 字符型

都是用来存储字符数据的，对用到MySQL中有两种类型：longtext 和 varchar

除了TextField时longtext，其他均属于varchar。

那么为什么同样是varchar，又会分出这么多呢？

是因为上层业务的不同展示，比如URLField，非url的数据在业务层就可以拒绝掉，不会存入数据库中。

+ CharField varchar 

  基础的varchar类型

+ URLField

  继承自CharField，但是实现了对URL的特殊处理

+ UUIDField char(32)

  除了在PostgreSQL中使用的是uuid类型外，在其他数据库中均是固定长度char(32)，用来存放唯一生成的id

+ EmailField

  同URLField一样，继承自CharField，多了对Email的特殊处理

+ FileField

  同URLField一样，继承自CharField，多了对文件的特殊护理。当你定义一个字段为FileField时，在admin部分展示时会自动生成一个可上传文件的按钮。

+ TextField longtext

  一般用来存放大量文本内容，比如新闻正文、博客正文

+ ImageField

  继承自CharField。用来处理图片相关的数据，在展示上会有不同

### 日期类型

下面三个都是日期类型，分别对应MySQL中的data、datetime 和 time

+ DateFiled
+ DateTimeField
+ TimeField

### 关系类型

这是关系型数据库中比较重要的字段类型，用来关联两个表

+ ForeinKey
+ OneToOneField
+ ManyToManyField

其中外键和一对一其实是一种，只是一对一在外间的字段上加了unique。

而多对多会创建一个中间表，来进行多对多的关联。

## 5.3.3 参数

各种字段类型都提供了一些参数供我们使用。

这些类型就是Python中的类，比如models.CharField的定义就是这样:class CharField。这些参数都是类在实例化时传递的。

下面我们列一下参数，并给一个简单的说明

+ null

  可以用blank对比考虑，null用于设定在数据库层面是否允许为空

+ blank

  针对业务层面，该值是否允许为空

+ choices

  配置字段的choices后，在admin页面上就可以看到对应的可选项展示

+ db_column

  默认情况下，我们定义的Field就是对应数据库中的字段名称，通过这个参数可以指定Model中的某个字段对应数据库中的哪个字段

+ db_index

  索引配置。对于业务上需要经常作为查询条件的字段，应该配置此选项。

+ primary_key

  主键，一个Model只允许设置一个字段为primary_key

+ unique

  唯一约束，当需要配置唯一值时，设置unique=True，设置此项后，不需要设置db_index

+ unique_for_date 

  针对date（日期）的联合约束，比如我们需要一天只能有一篇名为《Django》的文章，那么可以再定义title字段时配置参数:unique_for_date="created_time"

  需要注意的是，这并不是数据库层面的约束

+ Unique_for_mooth

  针对月份的联合约束

+ unique_for_year

  针对年份的联合约束

+ verbose_name

  字段对应的展示文案

+ validators

  自定义校验逻辑，同form类似

# 5.4 QuerySet 的使用

## 5.4.1 QuerySet 的概念

我们同数据库的所有查询以及更新交互都是通过它完成的。

Django是标准的MVC框架，因为它的模板和View的概念又被大家戏称为“MTV”的开发模式，但道理都是一样的。

Model层作为基础层（数据层），负责为整个系统提供数据。

在Model层中，Django通过给Model增加一个objects属性来提供数据操作的接口。比如，想要查询所有的文章数据：`Post.objects.all()` ，这样就能拿到QuerySet对象。这个对象包含了我们需要的数据，**当我们用到它时，它才会去DB中获取数据**。

这样的话为什么说是 用到数据的时候才会去DB中查询，而不是执行Post.objects.all()时就去拿数据呢？原因是QuerySet支持链式操作。如果每次执行都要去查询数据库的话，会存在性能问题，因为你可能用不到你执行的代码。举个例子，页顺便说下链式调用。

```python
Posts = Post.objects.all()
available_post = posts.filter(status=1)
```

如果这条语句要立即执行，就会出现这种情况：限制性Post.objects.all()，拿到所有的数据posts，然后进行过滤，拿到所有上线状态的文章available_post，这样就会产生两次数据库请求，并且两次查询存在重复的数据。

当然，平时可能不会出现这么低级的错误，但是当代码比较复杂时，谁也无法保证不会出现类似的问题。

所以，Django的QuerySet本质上是一个懒加载的对象，上面的两行代码执行后，都不会产生数据库查询操作，只是会返回一个QuerySet对象，当你真正用它时才会产生查询操作。

通过代码理解一下：

```python
posts = Post.objects.all()  # 返回一个QuerySet对象并赋值给posts
available_post = posts.filter(status=1)  # 继续返回一个QuerySet对象并赋值给available_post
print(available_post)  # 此时会根据上面的两个条件执行数据查询操作，对应的SQL语句为：SELECT * FROM blog_post where ststus =1;
```

另外上面说的 **链式调用**， 就是 执行一个对象中的方法之后得到的结果还是这个对象，这样可以接着执行对象上的其他方法。比如：

```python
posts = Post.objects.filter(status=1).filter(category_id=2).filter(title__icontains="the5fire")
```

数据就是水流，方法就是管道，把不同的管道连接起来形成“链”，然后让数据流过。

## 5.4.2 常用的QuerySet接口

