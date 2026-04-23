# WSL2 中 Git Clone 失败排查全记录

## 问题背景

在 Windows 11 的 WSL (Ubuntu) 环境下，运行 Hermes Agent 安装脚本时，`git clone` 通过 HTTPS 克隆 GitHub 仓库失败，报错：

```
GnuTLS recv error (-110)
fatal: unable to access 'https://github.com/NousResearch/hermes-agent.git/':
```

这是一次典型的**网络连通性排查**过程，从问题定位到最终解决经历了 6 个步骤。

---

## 术语解释

### 主要术语

#### 1. 仓库（Repository / Repo）
GitHub 上的一个项目文件夹，包含代码、历史记录等所有内容。可以类比为图书馆里的一本书。

#### 2. 克隆（git clone）
把 GitHub 上的仓库完整复制到本地电脑。就像把图书馆的书借回家复印一份。

#### 3. HTTPS vs SSH
两种与 GitHub 通信的方式：

| 特性 | HTTPS | SSH |
|------|-------|-----|
| 验证方式 | 用户名+密码 | SSH 密钥对 |
| 配置难度 | 简单 | 需提前配置密钥 |
| 稳定性 | 易受网络干扰 | 更稳定 |

#### 4. SSH 密钥（SSH Key）
一对数字锁和钥匙：**私钥**存你电脑上（绝不外泄），**公钥**上传到 GitHub。连接时它们互相验证，证明"这台电脑是我的"。

#### 5. 代理（Proxy）
你的请求不直接发给目标网站，而是先发给一台中间服务器，由它转发。Clash、V2Ray 就是代理软件。

### 次要术语

- **TLS/SSL**：HTTPS 背后的加密技术，保证数据传输不被偷看。GnuTLS 是 Linux 上实现这套加密的软件库。
- **防火墙（Firewall）**：网络保安，根据规则拦截某些网络请求。校园网/公司网常有防火墙阻止访问 GitHub。
- **DNS**：互联网的电话簿，把 `github.com` 翻译成 IP 地址（如 `140.82.114.4`）。
- **镜像站（Mirror）**：GitHub 的复制副本，部署在国内，访问更快更稳定。
- **终端（Terminal）**：输入命令的命令行窗口。
- **WSL（Windows Subsystem for Linux）**：在 Windows 里运行 Linux 的子系统，它和 Windows 主机之间有虚拟网络隔阂。

---

## 排查过程（6 步）

### 第 1 步：浏览器测试 — 确认 GitHub 是否可达

**操作**：在 Windows 的 Chrome 浏览器中打开 `https://github.com`

**结果**：✅ 能正常打开

**结论**：网络本身能访问 GitHub，问题出在 WSL 内部。

**底层原理**：浏览器运行在 Windows 主机上，走的是 Windows 的网络栈。能打开 GitHub 说明 Windows → GitHub 的链路是通的。而 WSL 是一个独立的 Linux 虚拟机，有自己独立的网络栈，它的网络和 Windows 主机的网络是隔开的。

---

### 第 2 步：确认代理软件

**问题**：Windows 上是否开了代理软件？

**回答**：有，Clash 正在运行。

**结论**：Windows 的 Chrome 能访问 GitHub 是因为走了 Clash 代理，但 WSL 里的 Git 没有配置代理，所以直连失败。

**底层原理**：代理软件（如 Clash）在 Windows 上监听一个本地端口（如 `127.0.0.1:7890`），Windows 上的浏览器如果配置了代理，会把请求发给这个端口，Clash 再转发到目标服务器。但 WSL 是独立的 Linux 环境，它不会自动使用 Windows 上配置的代理。

---

### 第 3 步：配置 Git 走 127.0.0.1 代理（失败）

**操作**：
```bash
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
```

**结果**：❌ 报错
```
Failed to connect to 127.0.0.1 port 7890 after 0 ms: Couldn't connect to server
```

**分析**：`0 ms` 就失败，说明根本没有目标可连。

**底层原理**：WSL 里的 `127.0.0.1` 指的是 **WSL 自己**，不是 Windows 主机。WSL 和 Windows 是两个独立的网络环境，各有各的 `localhost`。你在 WSL 里访问 `127.0.0.1:7890`，等于在 WSL 内部找端口 7890 的服务——当然找不到，因为 Clash 是运行在 Windows 上的。

**关键认识**：这是 WSL 排查中非常常见的一个陷阱。`127.0.0.1` 在不同环境里指代的对象不同。

---

### 第 4 步：用 resolv.conf 获取 Windows IP（失败）

**操作**：
```bash
cat /etc/resolv.conf | grep nameserver | awk '{print $2}'
```

**结果**：`10.255.255.254`

**操作**：
```bash
git config --global http.proxy http://10.255.255.254:7890
git config --global https.proxy http://10.255.255.254:7890
```

**结果**：❌ 报错
```
Failed to connect to 10.255.255.254 port 7890 after 0 ms: Couldn't connect to server
```

**分析**：`10.255.255.254` 是 WSL2 的特殊 DNS 地址，不是真正的 Windows 主机 IP。

**底层原理**：`/etc/resolv.conf` 里的 `nameserver` 在 WSL2 的不同版本中行为不一致。有些版本输出的是 Windows 主机的虚拟网卡 IP，有些版本输出的是 WSL2 内部的 DNS 转发地址（如 `10.255.255.254`），后者并不是 Windows 主机的真实 IP。用这个地址去找 Clash，自然找不到。

**教训**：`resolv.conf` 方法在 WSL2 中**不可靠**，应该用 `ip route` 方法获取网关 IP。

---

### 第 5 步：用 ip route 获取真正的 Windows IP

**操作**：
```bash
ip route | grep default | awk '{print $3}'
```

**结果**：`172.26.192.1`

**操作**：
```bash
git config --global http.proxy http://172.26.192.1:7890
git config --global https.proxy http://172.172.26.192.1:7890
```

**结果**：❌ 还是失败，但关键变化——等了 **123322 ms**（约 2 分钟）才超时

**分析**：从 `0 ms` 到 `123 秒`，这是一个重要的信号！说明 WSL 确实能"碰到" Windows 主机上的 Clash 了（网络是通的），但 Clash 没有响应。

**底层原理**：`172.26.192.1` 是 WSL2 虚拟交换机的网关地址，也就是 Windows 主机在 WSL 虚拟网络中的 IP。WSL 通过这个 IP 可以访问 Windows 主机。但 Clash 默认只监听 `127.0.0.1`（本机回环地址），不监听来自局域网的请求。WSL 对 Windows 来说相当于局域网内的另一台设备，所以被 Clash 拒绝了。

**关键认识**：连接超时（等了很久才失败）和连接拒绝（立刻失败）是完全不同的错误模式，前者说明网络通了但服务拒绝，后者说明网络不通。

---

### 第 6 步：开启 Clash 的"允许局域网连接"（成功）

**问题定位**：Clash 的 "Allow LAN" 开关处于关闭状态（红色）。

**操作**：将 Clash 的"允许局域网"开关打开（变绿色）。

**底层原理**：
- Clash 默认只接受来自 `127.0.0.1` 的连接（本机）
- 开启 "Allow LAN" 后，Clash 开始监听 `0.0.0.0`（所有网络接口），包括来自 WSL 虚拟网络的请求
- WSL（IP `172.26.x.x`）→ Windows 主机（IP `172.26.192.1`）→ Clash（端口 7890）→ GitHub

**结果**：✅ 克隆成功！

---

## 网络拓扑图

```
┌─────────────────────────────────────────────────────┐
│  Windows 主机                                       │
│                                                     │
│  ┌──────────┐    ┌──────────────────────────────┐   │
│  │  Chrome   │───→│  Clash 代理 (127.0.0.1:7890)  │───→ GitHub
│  └──────────┘    │  Allow LAN: ✅ (必须开启!)     │   │
│                  └──────────┬───────────────────────┘   │
│                             │ ↑ 172.26.192.1:7890       │
┌─────────────────────────────┼─────────────────────────────┐
│  WSL (Ubuntu)               │                             │
│                             │                             │
│  ┌──────────┐               │                             │
│  │   Git    │───────────────┘                             │
│  │ (proxy:  │   ← git config --global http.proxy         │
│  │ 172.26.  │     http://172.26.192.1:7890               │
│  │ 192.1:   │                                             │
│  │  7890)   │                                             │
│  └──────────┘                                             │
└───────────────────────────────────────────────────────────┘
```

---

## 排查决策树

```
git clone 失败
│
├── Windows 浏览器能打开 GitHub 吗？
│   ├── 否 → 网络本身的问题（开代理、换DNS、用镜像站）
│   └── 是 → 问题在 WSL 内部
│
├── WSL 有没有配代理？
│   ├── 没配 → 先配代理
│   └── 配了 → 代理地址对吗？
│
├── 代理地址是 127.0.0.1 吗？
│   ├── 是 → ❌ 错！WSL 的 127.0.0.1 是自己，不是 Windows
│   └── 否 → IP 地址对吗？
│
├── IP 是从 resolv.conf 取的吗？
│   ├── 是 → ❌ 可能不准！WSL2 特殊 DNS 地址
│   └── 否 → 是从 ip route 取的吗？
│
├── 连接是立刻失败还是超时？
│   ├── 立刻失败(0ms) → IP/端口不对
│   └── 超时(几十秒) → 网络通了但服务拒绝 → 检查 Allow LAN
│
└── 开启 Clash "允许局域网" → ✅ 成功
```

---

## 核心经验总结

### 1. WSL 的 127.0.0.1 ≠ Windows 的 127.0.0.1

这是最关键的认识。WSL2 是一个真正的 Linux 虚拟机，有独立的网络栈。在 WSL 里访问 `127.0.0.1` 只能到达 WSL 自己，无法触及 Windows 上运行的服务。

### 2. 获取 Windows 主机 IP 的正确方法

- ❌ `cat /etc/resolv.conf | grep nameserver` — 不可靠，可能返回 WSL 内部 DNS 地址
- ✅ `ip route | grep default | awk '{print $3}'` — 可靠，返回虚拟网关 IP（即 Windows 主机 IP）

### 3. 错误信息的"超时时长"是重要线索

- **0 ms 失败**：根本连不上目标，IP 或端口错误
- **几十秒超时**：网络能通到目标，但目标拒绝响应，说明服务端配置问题

### 4. 代理软件的 Allow LAN 是关键

WSL 对 Windows 来说就是局域网内的另一台设备。如果代理软件不开启"允许局域网连接"，所有来自 WSL 的请求都会被静默拒绝。

### 5. 排查顺序：从简到难

1. 先确认基本连通性（浏览器测试）
2. 再确认中间链路（代理配置）
3. 最后确认服务端设置（Allow LAN）

---

## 最终解决方案（完整命令）

```bash
# 1. 获取 Windows 主机 IP
WIN_IP=$(ip route | grep default | awk '{print $3}')
echo $WIN_IP
# 输出类似: 172.26.192.1

# 2. 配置 Git 代理
git config --global http.proxy http://$WIN_IP:7890
git config --global https.proxy http://$WIN_IP:7890

# 3. 确保 Clash 开启 "Allow LAN"（允许局域网连接）

# 4. 重新运行安装脚本
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

---

## 感想

这次排查的过程看似简单，实则涉及了**操作系统网络模型**、**虚拟化网络**、**代理协议**等多个层面：

1. **直觉往往是错的**：第一步想当然地把代理设成 `127.0.0.1:7890`，因为在 Windows 上一直这么用。但 WSL 的网络隔离打破了这个直觉。这提醒我们：**在虚拟化环境中，每个"常识"都需要重新验证。**

2. **错误信息会说话**：从 `0 ms` 到 `123 秒` 的变化，是整个排查的转折点。如果只是机械地换 IP 而不分析超时差异，可能会在错误的路上走更远。**读懂错误信息比换方法更重要。**

3. **每一层都可能出问题**：这个问题的排查实际上经过了四个网络层次：
   - **应用层**：Git 配置了代理吗？
   - **传输层**：端口对吗？服务在监听吗？
   - **网络层**：IP 地址对吗？WSL 能路由到 Windows 吗？
   - **服务配置层**：Clash 允许外部连接吗？

   这恰好对应了计算机网络课程中的分层模型，是一次非常生动的实践。

4. **工具方法的可靠性要验证**：`resolv.conf` 方法在网上大量流传，但在 WSL2 的某些版本中并不可靠。这提醒我们：**网上的教程要结合自己环境验证，不能盲目照搬。**

5. **问题的本质是"两个世界"的桥接**：WSL 和 Windows 是两个独立的网络世界，而代理配置就是在两者之间搭桥。桥要能通，需要三件事：**知道对岸地址（IP）、知道对岸入口（端口）、对岸允许你过（Allow LAN）**。缺一不可。
