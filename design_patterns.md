# 高级程序员必须掌握的设计模式

设计模式分为三大类：**创建型**、**结构型**、**行为型**。以下是最重要的几种：

---

## 🏗️ 创建型模式

### 1. 单例模式（Singleton）
确保一个类只有一个实例，并提供全局访问点。

```javascript
class Database {
  static instance = null;

  static getInstance() {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }
}

const db1 = Database.getInstance();
const db2 = Database.getInstance();
console.log(db1 === db2); // true
```
**适用场景：** 配置管理、日志系统、数据库连接池

---

### 2. 工厂模式（Factory）
将对象的创建逻辑封装起来，调用方无需关心具体实现。

```javascript
class PaymentFactory {
  static create(type) {
    const map = {
      alipay: AlipayPayment,
      wechat: WechatPayment,
      card: CardPayment,
    };
    const Cls = map[type];
    if (!Cls) throw new Error(`Unknown payment: ${type}`);
    return new Cls();
  }
}

const payment = PaymentFactory.create('alipay');
payment.pay(100);
```
**适用场景：** 支付系统、通知系统、渲染引擎

---

### 3. 建造者模式（Builder）
将复杂对象的构建过程拆分为链式调用。

```javascript
class QueryBuilder {
  constructor() { this.query = {}; }

  select(fields)  { this.query.fields = fields; return this; }
  from(table)     { this.query.table = table;  return this; }
  where(cond)     { this.query.where = cond;   return this; }
  limit(n)        { this.query.limit = n;      return this; }

  build() { return this.query; }
}

const q = new QueryBuilder()
  .select(['name', 'email'])
  .from('users')
  .where('age > 18')
  .limit(10)
  .build();
```
**适用场景：** SQL 构造器、HTTP 请求封装、复杂配置对象

---

## 🔧 结构型模式

### 4. 代理模式（Proxy）
为对象提供一个替代品，控制对原对象的访问（缓存、权限、懒加载）。

```javascript
const apiHandler = {
  cache: {},
  get(target, key) {
    if (this.cache[key]) {
      console.log('命中缓存');
      return () => Promise.resolve(this.cache[key]);
    }
    return async (...args) => {
      const result = await target[key](...args);
      this.cache[key] = result;
      return result;
    };
  }
};

const cachedApi = new Proxy(api, apiHandler);
```
**适用场景：** 缓存层、权限校验、日志拦截、Vue3 响应式原理

---

### 5. 装饰器模式（Decorator）
在不修改原类的前提下，动态地为对象添加功能。

```javascript
function readonly(target, key, descriptor) {
  descriptor.writable = false;
  return descriptor;
}

function log(target, key, descriptor) {
  const original = descriptor.value;
  descriptor.value = function (...args) {
    console.log(`调用 ${key}，参数:`, args);
    return original.apply(this, args);
  };
  return descriptor;
}

class UserService {
  @log
  @readonly
  getUser(id) { /* ... */ }
}
```
**适用场景：** AOP 切面编程、Express 中间件、TypeScript 装饰器

---

### 6. 适配器模式（Adapter）
将不兼容的接口转换为可可协作的形式。

```javascript
// 旧接口
class OldLogger {
  writeLog(msg) { console.log('[OLD]', msg); }
}

// 新系统期望的接口
class LoggerAdapter {
  constructor(oldLogger) { this.logger = oldLogger; }
  log(level, msg) { this.logger.writeLog(`[${level}] ${msg}`); }
}

const logger = new LoggerAdapter(new OldLogger());
logger.log('INFO', '系统启动'); // 新接口调用旧实现
```
**适用场景：** 第三方库集成、旧系统迁移、跨平台 SDK 封装

---

## 🎭 行为型模式

### 7. 观察者模式（Observer）
定义一对多的依赖关系，状态变化时自动通知所有订阅者。

```javascript
class EventEmitter {
  constructor() { this.listeners = {}; }

  on(event, fn)  { (this.listeners[event] ??= []).push(fn); }
  off(event, fn) { this.listeners[event] = this.listeners[event]?.filter(f => f !== fn); }
  emit(event, data) { this.listeners[event]?.forEach(fn => fn(data)); }
}

const emitter = new EventEmitter();
emitter.on('login', user => console.log(`${user} 已登录`));
emitter.emit('login', 'Alice');
```
**适用场景：** 事件系统、Vue/React 状态管理、消息队列

---

### 8. 策略模式（Strategy）
将算法封装成独立类，运行时动态切换，消除大量 if-else。

```javascript
const sortStrategies = {
  bubble: arr => { /* 冒泡 */ },
  quick:  arr => { /* 快排 */ },
  merge:  arr => { /* 归并 */ },
};

class Sorter {
  constructor(strategy) { this.strategy = strategy; }
  sort(data) { return sortStrategies[this.strategy](data); }
}

const sorter = new Sorter('quick');
sorter.sort([3, 1, 4, 1, 5]);
```
**适用场景：** 排序算法、表单验证、折扣计算、权限策略

---

### 9. 命令模式（Command）
将操作封装为对象，支持撤销/重做、队列执行。

```javascript
class CommandManager {
  constructor() { this.history = []; }

  execute(command) {
    command.execute();
    this.history.push(command);
  }

  undo() {
    const cmd = this.history.pop();
    cmd?.undo();
  }
}
```
**适用场景：** 编辑器撤销重做、事务操作、任务队列

---

## 📊 总结对比

| 模式 | 类型 | 核心思想 | 典型应用 |
|------|------|----------|----------|
| 单例 | 创建型 | 唯一实例 | 配置、连接池 |
| 工厂 | 创建型 | 封装创建逻辑 | 支付、通知 |
| 建造者 | 创建型 | 链式构建 | SQL、配置对象 |
| 代理 | 结构型 | 控制访问 | 缓存、权限 |
| 装饰器 | 结构型 | 动态扩展 | AOP、中间件 |
| 适配器 | 结构型 | 接口转换 | 旧系统集成 |
| 观察者 | 行为型 | 事件驱动 | 状态管理 |
| 策略 | 行为型 | 算法替换 | 验证、折扣 |
| 命令 | 行为型 | 操作对象化 | 撤销/重做 |

> **核心原则：** 设计模式不是银弹，过度使用反而增加复杂度。关键是理解每种模式解决的**具体问题**，在合适的场景自然运用。
