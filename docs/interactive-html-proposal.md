# Kiro IDE 交互式 HTML 报告功能设计方案

## 1. 项目概述

### 1.1 目标
在 Kiro IDE 中实现交互式 HTML 报告功能，允许 AI 生成可交互的 HTML 内容，用户在 HTML 中的操作可以自动反馈给 AI，形成连续的对话流程。

### 1.2 核心价值
- 提升 AI 输出的可交付性和专业度
- 支持复杂的多步骤交互流程
- 增强用户体验，减少重复输入
- 适用于报告、问卷、配置向导等场景

### 1.3 典型使用场景
```
场景 1: 投资组合配置向导
用户: "帮我配置一个投资组合"
AI: 生成交互式表单（风险偏好、投资金额、期限等）
用户: 在表单中填写并提交
AI: 基于用户输入生成个性化投资建议

场景 2: 数据分析报告
用户: "分析这些股票数据"
AI: 生成带图表的 HTML 报告，包含筛选器
用户: 调整筛选条件
AI: 更新分析结果

场景 3: 代码审查清单
用户: "生成代码审查清单"
AI: 生成可勾选的 HTML 清单
用户: 勾选完成项
AI: 生成审查总结报告
```

---

## 2. 技术架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                    Kiro IDE 主界面                        │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────┐         ┌──────────────────────┐   │
│  │   对话面板       │         │  交互式 HTML 面板     │   │
│  │                 │         │                      │   │
│  │  用户消息       │         │  ┌────────────────┐  │   │
│  │  AI 回复        │◄────────┤  │  HTML 渲染器   │  │   │
│  │  [HTML 预览]    │         │  │  (Sandboxed)   │  │   │
│  │                 │         │  └────────────────┘  │   │
│  │                 │         │         ▲            │   │
│  └─────────────────┘         │         │            │   │
│         │                    │  ┌──────┴─────────┐  │   │
│         │                    │  │  交互捕获层     │  │   │
│         │                    │  │  (Event Bridge) │  │   │
│         │                    │  └────────────────┘  │   │
│         │                    └──────────────────────┘   │
│         │                              │                │
│         └──────────────────────────────┘                │
│                     上下文管理器                          │
└─────────────────────────────────────────────────────────┘
```

### 2.2 核心组件

#### 2.2.1 HTML 渲染器 (Renderer)
```typescript
interface HTMLRenderer {
  // 渲染 HTML 内容
  render(html: string, artifactId: string): void;
  
  // 注入通信桥接
  injectBridge(): void;
  
  // 清理和销毁
  destroy(): void;
}
```

**技术选型**:
- 使用 `<iframe sandbox>` 实现安全隔离
- 支持的 sandbox 权限: `allow-scripts`, `allow-forms`, `allow-same-origin`
- 禁止: 网络请求、弹窗、顶层导航

#### 2.2.2 交互捕获层 (Event Bridge)
```typescript
interface EventBridge {
  // 监听 HTML 内部事件
  onInteraction(callback: (event: InteractionEvent) => void): void;
  
  // 向 HTML 注入 API
  injectAPI(): void;
}

interface InteractionEvent {
  type: 'form_submit' | 'button_click' | 'input_change';
  artifactId: string;
  data: Record<string, any>;
  timestamp: number;
}
```

**实现方式**:
```javascript
// 注入到 HTML 的全局 API
window.kiro = {
  // 提交数据到 AI
  submit: (data) => {
    window.parent.postMessage({
      type: 'kiro:submit',
      artifactId: '${artifactId}',
      data: data
    }, '*');
  },
  
  // 更新状态
  updateState: (state) => {
    window.parent.postMessage({
      type: 'kiro:state_update',
      artifactId: '${artifactId}',
      state: state
    }, '*');
  }
};
```

#### 2.2.3 上下文管理器 (Context Manager)
```typescript
interface ContextManager {
  // 保存 HTML artifact
  saveArtifact(id: string, html: string, metadata: ArtifactMetadata): void;
  
  // 获取 artifact
  getArtifact(id: string): Artifact | null;
  
  // 构造提交消息
  buildSubmitMessage(artifactId: string, interactionData: any): string;
}

interface Artifact {
  id: string;
  html: string;
  metadata: ArtifactMetadata;
  createdAt: Date;
  interactions: InteractionEvent[];
}

interface ArtifactMetadata {
  title: string;
  description: string;
  version: number;
}
```

---

## 3. 实现细节

### 3.1 AI 生成 HTML 的规范

#### 3.1.1 HTML 模板结构
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{title}}</title>
  <style>
    /* 内联样式 */
    body { font-family: Arial, sans-serif; padding: 20px; }
    .kiro-form { max-width: 600px; margin: 0 auto; }
    .kiro-button { 
      background: #667eea; 
      color: white; 
      border: none; 
      padding: 10px 20px; 
      border-radius: 5px; 
      cursor: pointer; 
    }
  </style>
</head>
<body>
  <div class="kiro-form">
    <h2>{{title}}</h2>
    <form id="main-form">
      <!-- 表单内容 -->
      <button type="submit" class="kiro-button">提交</button>
    </form>
  </div>
  
  <script>
    // 使用 Kiro API
    document.getElementById('main-form').addEventListener('submit', (e) => {
      e.preventDefault();
      const formData = new FormData(e.target);
      const data = Object.fromEntries(formData.entries());
      
      // 提交到 AI
      window.kiro.submit(data);
    });
  </script>
</body>
</html>
```

#### 3.1.2 AI Prompt 模板
```markdown
当用户需要交互式内容时，生成符合以下规范的 HTML:

1. 使用 `window.kiro.submit(data)` 提交数据
2. 数据格式为 JSON 对象
3. 包含清晰的标题和说明
4. 使用语义化的表单元素
5. 提供友好的错误提示

示例:
```html
<form id="risk-assessment">
  <label>
    风险承受能力:
    <select name="risk_tolerance" required>
      <option value="low">保守型</option>
      <option value="medium">平衡型</option>
      <option value="high">激进型</option>
    </select>
  </label>
  <button type="submit">下一步</button>
</form>
<script>
  document.getElementById('risk-assessment').onsubmit = (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    window.kiro.submit(Object.fromEntries(data));
  };
</script>
```
```

### 3.2 消息流程

#### 3.2.1 生成阶段
```
用户输入: "帮我配置投资组合"
    ↓
AI 识别需要交互式内容
    ↓
生成 HTML + metadata
    ↓
返回特殊格式的响应:
{
  type: 'interactive_html',
  artifact_id: 'artifact_123',
  title: '投资组合配置向导',
  html: '<html>...</html>'
}
    ↓
IDE 渲染到交互式面板
```

#### 3.2.2 交互阶段
```
用户在 HTML 中填写表单
    ↓
点击"提交"按钮
    ↓
触发 window.kiro.submit(data)
    ↓
Event Bridge 捕获事件
    ↓
Context Manager 构造消息:
"
参考 artifact_123 (投资组合配置向导)
用户提交了以下信息:
- 风险承受能力: 平衡型
- 投资金额: 100000
- 投资期限: 3年

请基于这些信息生成投资建议。
"
    ↓
自动发送到 AI 对话框
    ↓
AI 生成新的响应（可以是文本或新的 HTML）
```

### 3.3 安全机制

#### 3.3.1 Sandbox 配置
```html
<iframe 
  sandbox="allow-scripts allow-forms allow-same-origin"
  src="about:blank"
  style="width: 100%; height: 100%; border: none;"
></iframe>
```

#### 3.3.2 内容安全策略 (CSP)
```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'unsafe-inline'; 
               style-src 'unsafe-inline'; 
               img-src data: https:; 
               connect-src 'none';">
```

#### 3.3.3 HTML 净化
```typescript
import DOMPurify from 'dompurify';

function sanitizeHTML(html: string): string {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: [
      'div', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
      'form', 'input', 'select', 'option', 'textarea', 'button', 'label',
      'table', 'thead', 'tbody', 'tr', 'th', 'td',
      'ul', 'ol', 'li', 'a', 'br', 'hr', 'strong', 'em', 'code', 'pre'
    ],
    ALLOWED_ATTR: [
      'id', 'class', 'name', 'type', 'value', 'placeholder', 
      'required', 'disabled', 'checked', 'selected',
      'href', 'target', 'style'
    ],
    ALLOW_DATA_ATTR: false
  });
}
```

---

## 4. 数据结构设计

### 4.1 Artifact 存储格式
```typescript
interface ArtifactStore {
  artifacts: Map<string, Artifact>;
  
  // 持久化到文件系统
  persist(): Promise<void>;
  
  // 从文件系统加载
  load(): Promise<void>;
}

// 存储位置: .kiro/artifacts/
// 文件格式: {artifact_id}.json
{
  "id": "artifact_123",
  "title": "投资组合配置向导",
  "description": "帮助用户配置个性化投资组合",
  "html": "<html>...</html>",
  "version": 1,
  "created_at": "2026-02-27T10:00:00Z",
  "updated_at": "2026-02-27T10:05:00Z",
  "interactions": [
    {
      "type": "form_submit",
      "timestamp": "2026-02-27T10:05:00Z",
      "data": {
        "risk_tolerance": "medium",
        "amount": 100000,
        "duration": 3
      }
    }
  ]
}
```

### 4.2 消息协议
```typescript
// HTML -> IDE
interface HTMLToIDEMessage {
  type: 'kiro:submit' | 'kiro:state_update' | 'kiro:error';
  artifactId: string;
  data?: any;
  state?: any;
  error?: string;
}

// IDE -> HTML
interface IDEToHTMLMessage {
  type: 'kiro:init' | 'kiro:update' | 'kiro:reset';
  artifactId: string;
  config?: any;
  data?: any;
}
```

---

## 5. 用户界面设计

### 5.1 对话面板中的 HTML 预览
```
┌─────────────────────────────────────┐
│ 🤖 AI                               │
│                                     │
│ 我为你生成了一个投资组合配置向导。   │
│ 请填写以下信息:                      │
│                                     │
│ ┌─────────────────────────────┐    │
│ │ 📊 投资组合配置向导          │    │
│ │                             │    │
│ │ [交互式 HTML 预览]           │    │
│ │                             │    │
│ │ [在新窗口中打开] [查看代码]  │    │
│ └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

### 5.2 独立的交互式面板
```
┌──────────────────────────────────────────┐
│ 📊 投资组合配置向导        [最小化] [×]  │
├──────────────────────────────────────────┤
│                                          │
│  [HTML 内容渲染区域]                      │
│                                          │
│  风险承受能力: [下拉选择]                 │
│  投资金额: [输入框]                       │
│  投资期限: [滑块]                         │
│                                          │
│  [提交]                                  │
│                                          │
├──────────────────────────────────────────┤
│ 💡 提交后将自动发送到 AI 对话框           │
└──────────────────────────────────────────┘
```

---

## 6. 实现路线图

### Phase 1: 基础功能 (2周)
- [ ] HTML 渲染器实现 (iframe + sandbox)
- [ ] 基础通信桥接 (postMessage)
- [ ] 简单表单提交支持
- [ ] Artifact 存储机制

**交付物**:
- 支持基本的表单提交
- 数据能自动发送到 AI 对话框

### Phase 2: 安全增强 (1周)
- [ ] HTML 净化 (DOMPurify)
- [ ] CSP 策略实施
- [ ] 错误处理和日志
- [ ] 用户权限确认

**交付物**:
- 安全的 HTML 执行环境
- 完善的错误提示

### Phase 3: 用户体验优化 (1周)
- [ ] 独立的交互式面板
- [ ] 版本历史和回滚
- [ ] 导出功能 (HTML/PDF)
- [ ] 响应式设计

**交付物**:
- 完整的用户界面
- 流畅的交互体验

### Phase 4: AI 集成 (1周)
- [ ] AI Prompt 模板优化
- [ ] 上下文构造优化
- [ ] 多轮交互支持
- [ ] 示例和文档

**交付物**:
- AI 能生成标准的交互式 HTML
- 完整的使用文档

**总工期**: 5周

---

## 7. 技术栈

### 7.1 前端
- TypeScript
- React (用于 IDE 界面)
- DOMPurify (HTML 净化)
- PostCSS (样式处理)

### 7.2 通信
- postMessage API (跨 iframe 通信)
- Custom Events (内部事件)

### 7.3 存储
- 文件系统 API (Artifact 持久化)
- IndexedDB (可选，用于缓存)

---

## 8. 风险和挑战

### 8.1 安全风险
**风险**: XSS 攻击、恶意脚本执行
**缓解**: 严格的 HTML 净化、Sandbox 隔离、CSP 策略

### 8.2 性能问题
**风险**: 大型 HTML 渲染卡顿
**缓解**: 虚拟滚动、懒加载、内容分页

### 8.3 兼容性
**风险**: 不同浏览器的 iframe 行为差异
**缓解**: 充分测试、降级方案

### 8.4 AI 生成质量
**风险**: AI 生成的 HTML 不符合规范
**缓解**: 严格的 Prompt 工程、模板库、验证机制

---

## 9. 成功指标

### 9.1 功能指标
- [ ] 支持至少 5 种常见交互类型（表单、按钮、选择器等）
- [ ] HTML 渲染成功率 > 95%
- [ ] 交互响应时间 < 200ms

### 9.2 安全指标
- [ ] 0 个已知的安全漏洞
- [ ] 100% 的 HTML 经过净化
- [ ] 通过安全审计

### 9.3 用户体验指标
- [ ] 用户满意度 > 4.5/5
- [ ] 交互成功率 > 90%
- [ ] 平均完成时间减少 50%

---

## 10. 后续扩展

### 10.1 高级交互
- 图表库集成 (ECharts, Chart.js)
- 拖拽排序
- 实时协作

### 10.2 模板市场
- 预制模板库
- 社区分享
- 模板评分和推荐

### 10.3 导出和分享
- 导出为独立 HTML
- 生成分享链接
- 嵌入到外部网站

---

## 11. 参考实现

### 11.1 类似产品
- Claude Artifacts
- ChatGPT Code Interpreter
- Notion AI

### 11.2 技术参考
- [DOMPurify 文档](https://github.com/cure53/DOMPurify)
- [iframe sandbox 规范](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe)
- [postMessage API](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage)

---

## 附录 A: 示例代码

### A.1 完整的交互式 HTML 示例
见 `examples/interactive-form.html`

### A.2 Event Bridge 实现
见 `src/event-bridge.ts`

### A.3 Context Manager 实现
见 `src/context-manager.ts`
