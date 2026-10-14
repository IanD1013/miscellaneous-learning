### PRIMARY KEY 约束

PRIMARY KEY（主键）唯一标识表中的每一行。
它强制执行两条规则：值必须是唯一的，且不能为 NULL。

### 单列主键

最常见的方法，用单个列作为唯一标识符：

```sql
-- 内联语法（写在列定义之后）
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);

-- 表约束语法（写在末尾）
CREATE TABLE products (
    product_id INTEGER,
    name VARCHAR(100),
    PRIMARY KEY (product_id)
);
```

### 复合主键

当单个列不足以唯一标识行时，可以组合多个列：

```sql
-- 选课表：一个学生可以选修多门课程，
-- 一门课程可以有多个学生，但每个组合是唯一的
CREATE TABLE enrollments (
    student_id INTEGER,
    course_id INTEGER,
    enrolled_date DATE,
    PRIMARY KEY (student_id, course_id)
);
```

### 用于自增键的 SERIAL

PostgreSQL 的 SERIAL 类型会自动生成唯一整数：

```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    total NUMERIC(10,2)
);
-- 第一次插入得到 id=1，第二次得到 id=2，依此类推
```

### 关键区别

| 方式 | 适用场景 | 示例 |
| --- | --- | --- |
| 单列主键 | 大多数表 | `id INTEGER PRIMARY KEY` |
| 复合主键 | 交叉连接表（Junction tables）、自然键 | `PRIMARY KEY (col1, col2)` |
| SERIAL 主键 | 自动生成的 ID | `id SERIAL PRIMARY KEY` |

### 你的任务

创建一个名为 `students` 的表，包含以下列：

- `id` - 作为 PRIMARY KEY 的整数
- `email` - 用于存储学生邮箱的 VARCHAR(255)，必须为 NOT NULL
- `first_name` - 用于存储名字的 VARCHAR(100)
- `last_name` - 用于存储姓氏的 VARCHAR(100)

在 `id` 列上使用内联 PRIMARY KEY 语法。

### 预期表结构

```sql
students
├── id (INTEGER, PRIMARY KEY)
├── email (VARCHAR(255), NOT NULL)
├── first_name (VARCHAR(100))
└── last_name (VARCHAR(100))
```

### 解答

```sql
-- 创建以 id 为 PRIMARY KEY 的 students 表
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100)
);
```
