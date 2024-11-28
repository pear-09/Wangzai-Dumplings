<template>
  <div class="note-detail-container">
    <!-- 添加窄白条 -->
    <div class="toolbar-bar">
      <!-- 返回按钮 -->
      <button @click="goBack" class="back-button">返回</button>
      <button @click="saveNote" class="back-button">保存</button>

      <!-- 编辑器工具栏 -->
      <div id="editor-toolbar-container"></div>
    </div>

    <!-- 文档标题 -->
    <h1 class="page-title"> 
      <input v-model="folderName" type="text" class="title-input" placeholder="请输入文档标题" />
    </h1>

    <!-- 文档内容编辑区 -->
    <div class="note-form">
      <div id="editor-container"></div>
    </div>
    <!-- 底部的字数和缩放按钮 -->
    <div class="footer-bar">
      <div class="word-count">字数: {{ wordCount }}</div>
      <div class="zoom-controls">
        <button @click="zoomOut">-</button>
        <span>{{ zoomPercentage }}%</span>
        <button @click="zoomIn">+</button>
      </div>
    </div>
    <!-- 功能弹窗 -->
    <div v-if="showPopup" class="popup">
      <div class="popup-content">
        <h3>{{ popupTitle }}</h3>
        <form @submit.prevent="handleFormSubmit">
          <div v-if="popupType === '段落美化'">
            <label for="text">美化段落：</label>
            <input type="text" v-model="formData.text" id="text" placeholder="请输入文本" />
            <label for="length">AI返回长度：</label>
            <input type="number" v-model="formData.length" id="length" placeholder="请输入长度" />
          </div>

          <div v-if="popupType === '生成段落'">
            <label for="prompt">提示词:</label>
            <input type="text" v-model="formData.prompt" id="prompt" placeholder="请输入提示" />
            <label for="length">AI返回长度：</label>
            <input type="number" v-model="formData.length" id="length" placeholder="请输入段落长度" />
            <label for="tone">AI语调：</label>
            <select v-model="formData.tone" id="tone"class = 'featuresec'>
              <option value="neutral">中性</option>
              <option value="formal">正式</option>
              <option value="informal">非正式</option>
              <option value="humorous">幽默</option>
              <option value="motivational">激励</option>
              <option value="serious">严肃</option>
              <option value="friendly">友好</option>
              <option value="sarcastic">讽刺</option>
              <option value="pessimistic">悲观</option>

            </select>
            <label for="style">段落风格：</label>
            <select v-model="formData.style" id="style"class = 'featuresec'>
              <option value="default">默认</option>
              <option value="academic">学术</option>
              <option value="creative">创意</option>
              <option value="technical">技术</option>
              <option value="narrative">叙事</option>
              <option value="descriptive">描述性</option>
              <option value="concise">简洁</option>
              <option value="emotional">情感</option>
            </select>

          </div>

          <div v-if="popupType === '续写内容'">
            <label for="text">续写文本：</label>
            <input type="text" v-model="formData.text" id="text" placeholder="请输入文本" />
            <label for="length">AI返回长度：</label>
            <input type="number" v-model="formData.length" id="length" placeholder="请输入续写长度" />
          </div>

          <div v-if="popupType === '写作提示'">
            <label for="prompt">提示词：</label>
            <input type="text" v-model="formData.prompt" id="prompt" placeholder="请输入提示" />
            <label for="length">AI返回长度：</label>
            <input type="number" v-model="formData.length" id="length" placeholder="请输入提示长度" />
            <label for="content_type">写作提示类型：</label>
            <select v-model="formData.content_type" id="content_type"class = 'featuresec'>
              <option value="inspiration">生成写作灵感</option>
              <option value="outline">生成写作大纲</option>
              <option value="title">生成吸引人的标题</option>
              <option value="character_bio">生成角色设定</option>
              <option value="scene_description">生成场景描述</option>
              <option value="dialogue">生成对话内容</option>
              <option value="plot_twist">生成情节转折</option>
              <option value="setting">生成环境设定</option>
              <option value="synopsis">生成故事摘要</option>
            </select>

          </div>

          <div v-if="popupType === '文章分析'">
            <label for="text"></label>
            <!-- <input type="text" v-model="formData.text" id="text" placeholder="将默认上传本编辑的所有文本" /> -->
            <label for="length">AI返回长度：</label>
            <input type="number" v-model="formData.length" id="length" placeholder="请输入分析长度" />
            <label for="type">文章分析类型：</label>
            <select v-model="formData.type" id="type" class = 'featuresec'>
              <option value="analysis">分析</option>
              <option value="evaluation">评价</option>
              <option value="correction">纠错</option>
            </select>

          </div>

          <button class="button1"type="submit">提交</button>
          <button class="button1"@click="closePopup" type="button">关闭</button>
        </form>
      </div>
    </div>
  </div>
  <div>
    <div v-if="showBeautifiedContent" class="popupbeauty">
      <textarea v-model="beautifiedText" class="editable-textarea"></textarea>
      <button class="button2"@click="replaceWithBeautifiedContent">插入</button>
      <button class="button2"@click="cancelBeautify">取消</button>
    </div>
  </div>

  <div v-if="showPopupcontent" class="popcontent">
    <div class="popcontent-body">
      <textarea v-model="popInputContent" class="popcontent-textarea" placeholder="请输入内容"></textarea>
      <div class="popcontent-buttons">
        <button class="button2"@click="handleInsert">插入</button>
        <button class="button2"@click="closePopContent">取消</button>
      </div>
    </div>
  </div>
  <!-- 选择文本后的操作按钮 -->
<div v-if="showSelectionButtons" class="selection-buttons">
  <button @click="handleSelectionChoice(true)">√</button>
  <button @click="handleSelectionChoice(false)">×</button>
</div>
<div v-if="showParagraphPopup" class="popcontent">
  <div class="popcontent-body">
    <textarea v-model="popInputContent" class="popcontent-textarea" placeholder="请输入内容"></textarea>
    <div class="popcontent-buttons">
      <button class="button2" @click="handleInsert">插入</button>
      <button class="button2" @click="closeParagraphPopup">取消</button>
    </div>
  </div>
</div>
</template>


<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Quill from 'quill';
import request from '@/utils/request';

const route = useRoute();
const router = useRouter();

const isNew = Number(route.query.isNew) === 1;
const docId = isNew ? null : route.params.id;

const folderId = route.query.folder_id || 0;
const folderName = ref(route.query.docName || '无标题');

let saveInterval: any = null;  // 用于存储定时器ID
const showPopup = ref(false);
const showPopupcontent = ref(false);
const popupTitle = ref('');
const popupType = ref('');
const formData = ref<{
  text: string;
  length: number;
  prompt: string;
  tone: string;
  style: string;
  content_type: string;
  type: string;
  AI_model: number;  // 显式定义为 number 类型
}>({
  text: '',
  length: 0,
  prompt: '',
  tone: '',
  style: '',
  content_type: '',
  type: '',
  AI_model: 0  // 默认值为 0
});

const wordCount = ref(0);  // 存储文档字数
const zoomPercentage = ref(100);  // 存储编辑器的放大缩小百分比
const quillEditor = ref(null);

const beautifiedText = ref<string>(''); // 用来存储后端返回的段落美化内容
const showBeautifiedContent = ref(false);  // 控制是否显示美化后的内容
const selectedRange = ref(null);
const showSelectionButtons = ref(false);
let lastAIModel = formData.value.AI_model;  // 初始化 lastAIModel 来保存上次的值

// 定义响应式状态
const showParagraphPopup = ref(false);  // 用来控制弹窗是否显示
const popInputContent = ref('');  // 用于输入框的双向绑定
const popupPosition = ref({ top: 100, left: 100 });  // 初始弹窗位置
let isDragging = ref(false);
let offsetX = ref(0);
let offsetY = ref(0);

const startDrag = (e: MouseEvent) => {
  isDragging.value = true;
  offsetX.value = e.clientX - popupPosition.value.left;
  offsetY.value = e.clientY - popupPosition.value.top;
  document.addEventListener('mousemove', onDrag);
  document.addEventListener('mouseup', stopDrag);
};

const onDrag = (e: MouseEvent) => {
  if (isDragging.value) {
    popupPosition.value.left = e.clientX - offsetX.value;
    popupPosition.value.top = e.clientY - offsetY.value;
  }
};

const stopDrag = () => {
  isDragging.value = false;
  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mouseup', stopDrag);
};
// 弹窗打开的函数
const openParagraphPopup = () => {
  showParagraphPopup.value = true;
};

// 弹窗关闭的函数
const closeParagraphPopup = () => {
  showParagraphPopup.value = false;
};


// 插入弹窗编辑器的内容到 Quill 编辑器中
const insertIntoQuill = () => {
  console.log('insertIntoQuill called'); // 检查函数是否被调用

  if (quillEditor.value && popInputContent.value) {
    console.log(quillEditor.value);

    // 获取文档的总长度，作为插入位置
    const insertPosition = quillEditor.value.getLength(); // 获取文章末尾位置

    // 插入弹窗内容到文章末尾
    quillEditor.value.insertText(insertPosition, popInputContent.value);

    // 隐藏弹窗
    showParagraphPopup.value = false;
  }
};

const handleInsert = () => {
  insertIntoQuill();
};


onMounted(async () => {
// 初始化 Quill 编辑器
quillEditor.value = new Quill('#editor-container', {
  theme: 'snow',
  placeholder: '编辑你的文档...',
  modules: {
    toolbar: [
      ['bold', 'italic', 'underline', 'strike'],        // 加粗、斜体、下划线、删除线
      [{ 'header': [1, 2, 3, false] }],                // 标题大小
      [{ 'list': 'ordered' }, { 'list': 'bullet' }],   // 列表
      ['link', 'image'],                               // 链接和图片
    ]
  }
});

// 获取 Quill 工具栏容器
const toolbarContainer = quillEditor.value.getModule('toolbar').container;
// 将工具栏添加到页面的特定位置
const toolbarTarget = document.getElementById('editor-toolbar-container');
  if (toolbarTarget && toolbarContainer) {
    toolbarTarget.appendChild(toolbarContainer);
     // 再修改样式
     toolbarContainer.style.align = 'center';  // 居中
  }

// 添加 "model" 工具
const modelButton = document.createElement('span');
modelButton.classList.add('ql-model');
modelButton.innerHTML = '📦';
modelButton.title = '选择模型';
const modelDropdown = document.createElement('select');
['openAI', 'Kimi'].forEach(option => {
  const item = document.createElement('option');
  item.value = option;
  item.innerText = option;
  modelDropdown.appendChild(item);
});

// 将模型按钮和下拉框添加到工具栏
toolbarContainer.appendChild(modelButton);
toolbarContainer.appendChild(modelDropdown);

// 添加每个功能按钮单独存在于工具栏
const addFeatureButton = (icon, title, handler) => {
  const button = document.createElement('span');
  button.classList.add('ql-feature');
  button.innerHTML = icon;
  button.title = title;
  button.style.cursor = 'pointer';  // 设置光标为小手型
  button.addEventListener('click', handler);
  toolbarContainer.appendChild(button);  // 将按钮单独添加到工具栏容器
};

// 功能按钮的点击事件处理
const handleFeatureChange = (selectedFeature) => {
  console.log('Selected feature:', selectedFeature);
  
  switch (selectedFeature) {
    case '段落美化':
      showPopupDetails('段落美化', '段落美化');
      break;
    case '生成段落':
      showPopupDetails('生成段落', '生成段落');
      break;
    case '续写内容':
      showPopupDetails('续写内容', '续写内容');
      break;
    case '写作提示':
      showPopupDetails('写作提示', '写作提示');
      break;
    case '文章分析':
      showPopupDetails('文章分析', '文章分析');
      break;
    default:
      console.log('功能未定义');
  }
};

// 添加功能按钮到工具栏
addFeatureButton('✨', '段落美化', () => handleFeatureChange('段落美化'));
addFeatureButton('💬', '生成段落', () => handleFeatureChange('生成段落'));
addFeatureButton('✏️', '续写内容', () => handleFeatureChange('续写内容'));
addFeatureButton('💡', '写作提示', () => handleFeatureChange('写作提示'));
addFeatureButton('🔍', '文章分析', () => handleFeatureChange('文章分析'));

  // 添加功能逻辑（根据需要处理选择事件）
  modelDropdown.addEventListener('change', handleModelChange);

  if (!isNew && docId) {
    await fetchDocumentContent();
  }

  // 设置定时自动保存，每3秒保存一次
  saveInterval = setInterval(saveNote, 300000);
  quillEditor.value.on('selection-change', function (range) {
    if (range && range.length > 0) {
      // 文本被选中，显示操作按钮
      showTextSelectionOptions(range);
    } else {
      // 没有文本被选中，隐藏按钮
      hideTextSelectionOptions();
    }
  });
  quillEditor.value.on('text-change', updateWordCount); // 每次编辑器内容发生变化时，更新字数
  updateWordCount(); // 初始化字数
  

});


// 工具栏按钮功能（增加和减少缩放）
// 放大缩小操作，增减 zoomPercentage
const zoomIn = () => {
  if (zoomPercentage.value < 200) {
    zoomPercentage.value += 10;  // 增加放大值
    updateEditorZoom();  // 更新缩放
  }
};

const zoomOut = () => {
  if (zoomPercentage.value > 50) {
    zoomPercentage.value -= 10;  // 减小缩放值
    updateEditorZoom();  // 更新缩放
  }
};


// 更新编辑器的缩放
const updateEditorZoom = () => {
  if (quillEditor.value) {
    // // 计算缩放比例
    const zoom = zoomPercentage.value / 100;
    // // 缩放 Quill 编辑器的根元素
    // quillEditor.value.root.style.transform = `scale(${zoom})`;
    // quillEditor.value.root.style.transformOrigin = 'top center';

    // 获取 editor-container 并应用缩放
    const editorContainer = document.getElementById('editor-container');
    if (editorContainer) {
      editorContainer.style.transform = `scale(${zoom})`;
      editorContainer.style.transformOrigin = 'top center';
    }
  }
  
};

// 获取字数
const updateWordCount = () => {
  if (quillEditor.value) {
    wordCount.value = quillEditor.value.getLength() - 1; // 减去1是因为 Quill 默认在末尾有一个换行符
  }
};


const showTextSelectionOptions = (range) => {
  selectedRange.value = range;
  showSelectionButtons.value = true;
};

const hideTextSelectionOptions = () => {
  showSelectionButtons.value = false;
};

const handleSelectionChoice = (isAccepted) => {
  if (isAccepted && selectedRange.value) {
    // 获取选中的文本内容
    const selectedText = quillEditor.value.getText(selectedRange.value.index, selectedRange.value.length);
    formData.value.text = selectedText; // 将选中的文本存储在 text 中
  }
  hideTextSelectionOptions(); // 隐藏按钮
};

onBeforeUnmount(() => {
  // 清除定时器
  if (saveInterval) {
    clearInterval(saveInterval);
  }
});
const handleModelChange = (event) => {
  const selectedModel = event.target.value;
  console.log('Selected model:', selectedModel);

  // 根据选择的模型设置 formData 的 AI_model 字段
  switch (selectedModel) {
    case 'openAI':
      formData.value.AI_model = 0;  // 选择 openAI 时设置为 0
      break;
    case 'Kimi':
      formData.value.AI_model = 1;  // 选择 Kimi 时设置为 1
      break;
    default:
      formData.value.AI_model = -1;  // 默认不发起 AI 请求
      break;
  }

  console.log('AI Model saved to formData:', formData.value.AI_model);
};




const showPopupDetails = (title, type) => {
  popupTitle.value = title;
  popupType.value = type;
  showPopup.value = true;
};

const closePopup = () => {
  showPopup.value = false;
  // 保持上次的 AI_model 值
  formData.value.AI_model = lastAIModel;
  formData.value = {
    text: '',
    length: 0,
    prompt: '',
    tone: '',
    style: '',
    content_type: '',
    type: '',
    AI_model:lastAIModel,
  };
};

const handleFormSubmit = () => {
  // 提交逻辑
  console.log('Form submitted:', formData.value);
  switch (popupType.value) {
    case '段落美化':
      beautifyParagraph();
      break;
    case '生成段落':
      generateParagraph();
      break;
    case '续写内容':
      continueContent();
      break;
    case '写作提示':
      provideWritingTips();
      break;
    case '文章分析':
      // 在选择文章分析时，将编辑器内容保存到 text
      formData.value.text = quillEditor.value.root.innerHTML;  // 保存编辑器内容到 formData.text
      analyzeArticle();
      break;
    default:
      console.log('未知功能');
  }
  closePopup();  // 提交后关闭弹窗
};


const beautifyParagraph = async () => {
  try {
    // 创建 FormData 对象
    const formDataToSend = new FormData();
    formDataToSend.append('text', formData.value.text);  // 添加文本内容
    formDataToSend.append('length', formData.value.length.toString());  // 添加文本长度，确保是字符串类型
    formDataToSend.append('AI_model', formData.value.AI_model.toString());  // 添加选择的 AI 模型，确保是字符串类型

    // 请求后端段落美化接口
    const response = await request.post('/ez-note/AI/beauty', formDataToSend, {
      headers: { 'Content-Type': 'multipart/form-data' }  // 设置请求头为 multipart/form-data
    });

    if (response.code === 0) {
      beautifiedText.value = response.translation;  // 存储后端返回的段落美化后的文本
      showBeautifiedContent.value = true;  // 显示美化后的内容
    } else {
      console.log('段落美化失败');
    }
  } catch (error) {
    console.error('段落美化请求失败:', error);
  }
};
// 替换选中的内容为段落美化后的文本
const replaceWithBeautifiedContent = () => {
  if (selectedRange.value && beautifiedText.value) {
    // 替换选中文本为用户编辑后的美化内容
    quillEditor.value.deleteText(selectedRange.value.index, selectedRange.value.length);
    quillEditor.value.insertText(selectedRange.value.index, beautifiedText.value);
    // 关闭弹窗
    showBeautifiedContent.value = false;
    selectedRange.value = null;
  }
};

// 取消操作
const cancelBeautify = () => {
  // 隐藏弹窗
  showBeautifiedContent.value = false;
  selectedRange.value = null;
};
// // 隐藏选中文本操作按钮
// const hideSelectionButtons = () => {
//   showSelectionButtons.value = false;
//   selectedRange.value = null;
// };

// 生成段落的函数
const generateParagraph = async () => {
      try {
        // 创建 FormData 对象
        const formDataToSend = new FormData();
        formDataToSend.append('prompt', formData.value.prompt);  // 添加生成段落的提示语
        formDataToSend.append('length', formData.value.length.toString());  // 添加段落的长度
        formDataToSend.append('tone', formData.value.tone);  // 添加写作的语气
        formDataToSend.append('style', formData.value.style);  // 添加写作风格
        formDataToSend.append('AI_model', formData.value.AI_model.toString());  // 添加选择的 AI 模型

        // 请求后端生成段落接口
        const response = await request.post('/ez-note/AI/generate', formDataToSend, {
          headers: { 'Content-Type': 'multipart/form-data' }  // 设置请求头为 multipart/form-data
        });

        if (response.code === 0) {
          console.log('生成段落成功', response.data);
          const generatedContent = response.paragraph; // 假设后端返回的段落内容字段名为 `paragraph`

          // 设置弹窗编辑器的内容
          popInputContent.value = generatedContent;

          // 显示弹窗
          showParagraphPopup.value = true;
          openParagraphPopup();
        } else {
          console.log('生成段落失败');
        }
      } catch (error) {
        console.error('生成段落请求失败:', error);
      }
    };



const continueContent = async () => {
  try {
    // 创建 FormData 对象
    const formDataToSend = new FormData();
    formDataToSend.append('text', formData.value.text);  // 添加当前文本内容
    formDataToSend.append('length', formData.value.length.toString());  // 添加续写内容的长度
    formDataToSend.append('AI_model', formData.value.AI_model.toString());  // 添加选择的 AI 模型

    // 请求后端续写内容接口
    const response = await request.post('/ez-note/AI/continue', formDataToSend, {
      headers: { 'Content-Type': 'multipart/form-data' }  // 设置请求头为 multipart/form-data
    });

    if (response.code === 0) {
      console.log('续写内容成功', response.data);
      const generatedContent = response.continuation; // 假设后端返回的段落内容字段名为 `paragraph`

      // 设置弹窗编辑器的内容
      popInputContent.value = generatedContent;

      // 显示弹窗
      showParagraphPopup.value = true;
      openParagraphPopup();
    } else {
      console.log('续写内容失败');
    }
  } catch (error) {
    console.error('续写内容请求失败:', error);
  }
};


const provideWritingTips = async () => {
  try {
    // 创建 FormData 对象
    const formDataToSend = new FormData();
    formDataToSend.append('prompt', formData.value.prompt);  // 添加写作提示的提示词
    formDataToSend.append('content_type', formData.value.content_type);  // 添加内容类型
    formDataToSend.append('length', formData.value.length.toString());  // 添加提示内容的长度
    formDataToSend.append('AI_model', formData.value.AI_model.toString());  // 添加选择的 AI 模型

    // 请求后端写作提示接口
    const response = await request.post('/ez-note/AI/inspiration', formDataToSend, {
      headers: { 'Content-Type': 'multipart/form-data' }  // 设置请求头为 multipart/form-data
    });

    if (response.code === 0) {
      console.log('写作提示成功', response.data);
      const generatedContent = response.inspiration; // 假设后端返回的段落内容字段名为 `paragraph`

      // 设置弹窗编辑器的内容
      popInputContent.value = generatedContent;

      // 显示弹窗
      showParagraphPopup.value = true;
      openParagraphPopup();
    } else {
      console.log('写作提示失败');
    }
  } catch (error) {
    console.error('写作提示请求失败:', error);
  }
};


const analyzeArticle = async () => {
  try {
    // 创建 FormData 对象
    const formDataToSend = new FormData();
    formDataToSend.append('text', formData.value.text);  // 添加文章内容
    formDataToSend.append('type', formData.value.type);  // 添加文章类型
    formDataToSend.append('length', formData.value.length.toString());  // 添加分析的长度
    formDataToSend.append('AI_model', formData.value.AI_model.toString());  // 添加选择的 AI 模型

    // 请求后端文章分析接口
    const response = await request.post('/ez-note/AI/analysis', formDataToSend, {
      headers: { 'Content-Type': 'multipart/form-data' }  // 设置请求头为 multipart/form-data
    });

    if (response.code === 0) {
      console.log('文章分析成功', response.data);
      const generatedContent = response.analysis||response.correction||response.evaluation; 

      // 设置弹窗编辑器的内容
      popInputContent.value = generatedContent;

      // 显示弹窗
      showParagraphPopup.value = true;
      openParagraphPopup();
    } else {
      console.log('文章分析失败');
    }
  } catch (error) {
    console.error('文章分析请求失败:', error);
  }
};




const fetchDocumentContent = async () => {
  if (!docId) return;
  try {
    const response = await request.get(`/ez-note/note/query`, { params: { note_id: docId } });
    if (response.code === 0) {
      folderName.value = response.data.title;
      quillEditor.value.root.innerHTML = response.data.content;
    } else {
      alert('获取文档内容失败');
    }
  } catch (error) {
    console.error('获取文档内容失败:', error);
  }
};

const saveNote = async () => {
  try {
    const content = quillEditor.value.root.innerHTML;

    const formData = new FormData();
    formData.append(isNew ? 'title' : 'note_id', isNew ? folderName.value : docId);
    formData.append('content', content);
    formData.append('folder_id', folderId.toString());

    const endpoint = isNew ? `/ez-note/note/create` : `/ez-note/note/update/content`;
    const response = await request.post(endpoint, formData, { headers: { 'Content-Type': 'multipart/form-data' } });

    if (response.code === 0) {
      console.log(isNew ? '文档新建成功' : '文档更新成功');
    } else {
      console.error(isNew ? '新建失败' : '更新失败');
    }
  } catch (error) {
    console.error('保存文档内容失败:', error);
  }
};

const goBack = () => {
  // 返回到 Write.vue 页面
  router.push({ name: 'xiezuo' });
};

</script>

<style scoped>

/* 按钮间距：除了最后一个按钮，其他按钮右侧有50px间距 */
.button2:not(:last-child) {
  margin-top: 20px;
  margin-right: 50px; /* 按钮间距调整 */
}

/* 按钮的公共样式 */
.button2 {
  display: inline-block;
  padding: 12px 24px; /* 上下12px，左右24px */
  background-color: #d9534f; /* 红色背景 */
  color: #fff; /* 文字颜色 */
  border: none; /* 去掉默认边框 */
  border-radius: 10px; /* 圆角边框 */
  font-size: 16px; /* 文字大小 */
  font-weight: 600; /* 字体加粗 */
  cursor: pointer; /* 鼠标悬浮时显示为手形 */
  text-align: center; /* 文字居中 */
  transition: all 0.3s ease-in-out; /* 平滑过渡效果 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 柔和阴影 */
}

/* 鼠标悬停时的效果 */
.button2:hover {
  background-color: #c9302c; /* 鼠标悬浮时稍微暗一点的红色 */
  transform: scale(1.05); /* 轻微放大 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* 增加阴影深度 */
}

/* 鼠标按下时的效果 */
.button2:active {
  background-color: #ac2925; /* 鼠标按下时的红色 */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15); /* 阴影缩小 */
  transform: scale(1); /* 还原按钮大小 */
}

/* 按钮失去焦点时 */
.button2:focus {
  outline: none; /* 移除默认焦点边框 */
  box-shadow: 0 0 4px 2px rgba(219, 50, 50, 0.7); /* 添加聚焦时的阴影 */
}

/* 按钮的公共样式 */
.button1:not(:last-child) {
  margin-top: 20px;
  margin-right: 50px; /* 除了最后一个按钮，其他按钮右侧有20px间距 */
}
.button1 {
  display: inline-block;
  padding: 12px 24px; /* 上下12px，左右24px */
  background-color: #2d6a4f; /* 深绿色背景 */
  color: #fff; /* 文字颜色 */
  border: none; /* 去掉默认边框 */
  border-radius: 10px; /* 圆角边框 */
  font-size: 16px; /* 文字大小 */
  font-weight: 600; /* 字体加粗 */
  cursor: pointer; /* 鼠标悬浮时显示为手形 */
  text-align: center; /* 文字居中 */
  transition: all 0.3s ease-in-out; /* 平滑过渡效果 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 柔和阴影 */
}

/* 鼠标悬停时的效果 */
.button1:hover {
  background-color: #1a4f34; /* 鼠标悬浮时稍微暗一点的绿色 */
  transform: scale(1.05); /* 轻微放大 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* 增加阴影深度 */
}

/* 鼠标按下时 */
.button1:active {
  background-color: #164f2b; /* 鼠标按下时的绿色 */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15); /* 阴影缩小 */
  transform: scale(1); /* 还原按钮大小 */
}

/* 按钮失去焦点时 */
.button1:focus {
  outline: none; /* 移除默认焦点边框 */
  box-shadow: 0 0 4px 2px rgba(45, 106, 79, 0.7); /* 添加聚焦时的阴影 */
}


.popcontent-textarea {
  width: 100%; /* 使文本框宽度充满父容器 */
  height: 150px; /* 适当的高度，可以根据需要调整 */
  padding: 12px 16px; /* 内边距，使得文本内容不紧贴边框 */
  background: rgba(255, 255, 255, 0.6); /* 半透明白色背景 */
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.2)); /* 细腻的渐变背景 */
  border: 1px solid rgba(255, 255, 255, 0.3); /* 微弱的边框 */
  border-radius: 10px; /* 圆角边框 */
  color: #2e3d34; /* 深灰色文字 */
  font-size: 16px; /* 文字大小 */
  line-height: 1.5; /* 行高，增加文本的可读性 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 轻微阴影效果 */
  resize: vertical; /* 允许垂直拖动调整大小 */
  backdrop-filter: blur(8px); /* 背景磨砂玻璃效果 */
  transition: all 0.3s ease-in-out; /* 平滑过渡效果 */
  box-sizing: border-box; /* 包括内边距和边框 */
}

.popcontent-textarea:focus {
  outline: none; /* 移除默认的聚焦边框 */
  border-color: #45a049; /* 聚焦时的绿色边框 */
  box-shadow: 0 0 6px rgba(69, 160, 73, 0.8); /* 聚焦时的绿色光晕 */
  background: rgba(255, 255, 255, 0.8); /* 聚焦时的白色背景 */
}

.popcontent-textarea::placeholder {
  color: rgba(0, 0, 0, 0.5); /* 占位符文字颜色 */
  font-style: italic; /* 占位符文字斜体 */
}

.popcontent {
  position: absolute; /* 可改为 fixed 保持位置固定 */
  padding: 20px; /* 内边距，给内容留出空间 */
  background: rgba(255, 255, 255, 0.4); /* 半透明白色背景 */
  background: linear-gradient(135deg, rgba(255, 182, 193, 0.6), rgba(173, 216, 230, 0.6)); /* 渐变粉蓝色背景 */
  color: #2e3d34; /* 文字颜色设置为深灰色 */
  border-radius: 15px; /* 圆角边框 */
  border: 1px solid rgba(255, 255, 255, 0.3); /* 轻微的白色边框 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 细腻的阴影效果 */
  backdrop-filter: blur(10px); /* 背景模糊效果 */
  font-size: 18px; /* 字体大小 */
  font-weight: 500; /* 适中的字体粗细 */
  line-height: 1.6; /* 行高增加文本可读性 */
  box-sizing: border-box; /* 包括内边距和边框的总宽度 */
  left: 50%; /* 水平居中 */
  top: 100px; /* 根据需要调整垂直位置 */
  transform: translateX(-50%); /* 水平居中 */
  transition: all 0.3s ease-in-out; /* 平滑过渡效果 */
}


.popcontent:hover {
  transform: translateX(-50%) scale(1.00); /* 鼠标悬浮时轻微放大 */
}

.popcontent:focus {
  outline: none; /* 移除默认的聚焦轮廓 */
  box-shadow: 0 0 8px rgba(69, 160, 73, 0.8); /* 聚焦时绿色光晕效果 */
}

.popcontent .header {
  font-size: 22px; /* 标题字体稍大 */
  font-weight: bold; /* 标题加粗 */
  margin-bottom: 15px; /* 标题下方的间距 */
}

.popcontent .body {
  font-size: 16px; /* 正文内容字体 */
  line-height: 1.5; /* 行高 */
  color: rgba(0, 0, 0, 0.7); /* 正文文字稍微淡化 */
}

.popcontent .footer {
  margin-top: 20px; /* 底部区域距离内容的间距 */
  text-align: center; /* 底部区域居中 */
}

.popupbeauty {
  position: absolute;  /* 可改为 fixed 保持位置固定 */
  background: linear-gradient(145deg, rgba(152, 255, 152, 0.3), rgba(255, 210, 225, 0.3),rgba(255,255,255,0.3)); /* 淡浅绿色、淡粉色、淡紫色渐变 */
  color: #2e3d34; /* 文字颜色 */
  border-radius: 15px; /* 圆角边框 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 轻微阴影效果 */
  padding: 20px; /* 内边距 */
  box-sizing: border-box; /* 包括内边距和边框 */
  left: 50%; /* 居中对齐 */
  top: 500px; /* 可以根据需要调整 */
  transform: translateX(-50%); /* 水平居中 */
  display: block;
  flex-direction: column; /* 垂直排列 */
  justify-content: center;
  align-items: center;
  font-size: 18px;
  font-weight: 600;
  transition: all 0.3s ease-in-out; /* 平滑过渡 */
  backdrop-filter: blur(10px); /* 背景磨砂玻璃效果 */
  border: 1px solid rgba(255, 255, 255, 0.2); /* 添加微弱的边框 */
}
.editable-textarea {
  display: block; /* 确保文本框占一整行 */
  background: rgba(255, 255, 255, 0.9); /* 半透明白色背景 */
  border-radius: 10px; /* 圆角边框 */
  border: 1px solid rgba(255, 255, 255, 0.2); /* 轻微的边框 */
  padding: 15px; /* 内边距，给内容一些空间 */
  width: 100%; /* 宽度为父容器的100% */
  min-height: 120px; /* 最小高度 */
  font-size: 16px; /* 字体大小 */
  color: #333; /* 文字颜色 */
  line-height: 1.5; /* 行高，增加文本间距 */
  font-family: 'Arial', sans-serif; /* 字体样式 */
  box-sizing: border-box; /* 包括边框和内边距的总宽度 */
  transition: all 0.3s ease-in-out; /* 平滑过渡效果 */
  backdrop-filter: blur(10px); /* 背景磨砂玻璃效果 */
  overflow: auto; /* 内容溢出时显示滚动条 */
}

.editable-textarea:focus {
  outline: none; /* 移除默认的聚焦轮廓 */
  border-color: rgba(69, 160, 73, 0.8); /* 聚焦时的边框颜色（绿色） */
  box-shadow: 0 0 4px rgba(69, 160, 73, 0.6); /* 聚焦时的光晕效果 */
  background: rgba(255, 255, 255, 0.6); /* 聚焦时背景稍微变亮 */
}

.editable-textarea::placeholder {
  color: rgba(0, 0, 0, 0.5); /* 提示文字的颜色，淡灰色 */
  font-style: italic; /* 提示文字为斜体 */
}


.featuresec {
  appearance: none;
  display: block;
  width: 100%;
  padding: 8px 12px; /* 内边距调整 */
  margin-bottom: 10px; /* 下方间距 */
  background: rgba(255, 255, 255, 0.6); /* 半透明背景 */
  border: 1px solid rgba(255, 255, 255, 0.3); /* 半透明边框 */
  border-radius: 6px; /* 圆角边框 */
  font-size: 14px; /* 字体大小 */
  color: #333; /* 输入框文字颜色 */
  transition: all 0.3s ease-in-out; /* 平滑过渡效果 */
  backdrop-filter: blur(5px); /* 背景模糊效果 */
  appearance: none; /* 去除浏览器默认的下拉箭头 */
  -webkit-appearance: none; /* 适配Safari */
  -moz-appearance: none; /* 适配Firefox */
}

.featuresec :focus {
  outline: none; /* 移除焦点时的边框 */
  border-color: #45a049; /* 聚焦时的边框颜色 */
  box-shadow: 0 0 4px rgba(69, 160, 73, 0.8); /* 聚焦时的绿色光晕 */
  background: rgba(255, 255, 255, 0.8); /* 聚焦时的背景色 */
}

.featuresec::before {
  content: " "; /* 添加伪元素，模拟自定义下拉箭头 */
  position: absolute;
  right: 12px; /* 右侧距离 */
  top: 50%;
  transform: translateY(-50%);
  width: 0; 
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 6px solid #45a049; /* 下拉箭头的颜色 */
}


.featuresec select {
  background-color: rgba(255, 255, 255, 0.6);
}

.featuresec select option:checked {
  background-color: rgba(69, 160, 73, 0.6) !important; /* 强制应用深绿色背景 */
  color: white !important; /* 强制应用白色文字 */
}


label, input {
  display: block;
  margin-bottom: 10px; /* 给元素之间适度的间距 */
  font-size: 14px; /* 更小的字体大小 */
  color: #4a4a4a; /* 深绿色字体 */
}

label {
  margin-bottom: 5px; /* 标签和输入框之间的间距 */
  font-weight: bold;  /* 标签文字加粗 */
}

input {
  width: 100%;  /* 输入框宽度占满父元素 */
  padding: 8px;  /* 更小的内边距 */
  background: rgba(255, 255, 255, 0.6);  /* 半透明背景 */
  border: 2px solid rgba(255, 255, 255, 0.3);  /* 半透明边框 */
  border-radius: 6px;  /* 圆角边框 */
  font-size: 14px;  /* 更小的字体 */
  color: #333;  /* 输入框文字颜色 */
  transition: all 0.3s ease-in-out;  /* 平滑过渡效果 */
  backdrop-filter: blur(5px);  /* 背景模糊效果 */
}

input:focus {
  outline: none;  /* 移除焦点时的边框 */
  border-color: #333;  /* 聚焦时的边框颜色 */
  box-shadow: 0 0 4px rgba(#333 0.8); /* 聚焦时的绿色光晕 */
  background: rgba(255, 255, 255, 0.8); /* 聚焦时的背景色 */
}


/* popup 样式 */
.popup {
  position: absolute;  /* 可改为 fixed 保持位置固定 */
  width: 300px;  /* 增大宽度 */
  background-color: rgba(117, 154, 139, 0.5); /* 浅绿色并加上透明度以实现磨砂效果 */
  color: #2e3d34; /* 文字颜色设置为白色 */
  border-radius: 15px; /* 圆角边框 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 轻微阴影效果 */
  padding: 20px; /* 增加内边距 */
  box-sizing: border-box; /* 包括内边距和边框 */
  left: 50%; /* 居中对齐 */
  top: 500px; /* 可以根据需要调整 */
  transform: translateX(-50%); /* 水平居中 */
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  font-weight: 600;
  transition: all 0.3s ease-in-out; /* 平滑过渡 */
  backdrop-filter: blur(10px); /* 背景磨砂玻璃效果 */
  border: 1px solid rgba(255, 255, 255, 0.2); /* 添加微弱的边框 */
}

/* popup-content 样式 */
.popup-content {
  width: 100%;  /* 使内容宽度填充整个弹窗 */
  height: 100%;  /* 内容占满整个弹窗高度 */
  padding: 20px;  /* 内部间距 */
}

/* 可选的动画效果 */
.popup:hover {
  transform: translateX(-50%) scale(1.00); /* 鼠标悬浮时轻微放大 */
  backdrop-filter: blur(7px); /* 背景磨砂玻璃效果 */
}


.toolbar-bar {
  display: flex;
  align-items: center;
  justify-content: flex-start; /* 或者 justify-content: center; */
  background-color: white;
  padding: 10px 0px;
  height: 40px;
  border-bottom: 1px solid #ddd;
}
.toolbar-bar > .back-button{
  margin-right: 80px;
}
.back-button:first-child {
  margin-right: 30px; /* 最后一个按钮右侧不需要间距 */
}

.toolbar-bar > .ql-toolbar {
  margin: 0 auto; /* 使 center 元素居中 */
}

#editor-container {
  width: 60%;
  margin: 0 auto;
  height: 800px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
  transform: scale(1.1); /* 用来放大 */
  transition: transform 0.3s ease; /* 动画效果，平滑缩放 */
  transform-origin: top center; /* 设置缩放原点 */
}

.footer-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  padding: 10px 20px;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
}

.word-count {
  font-size: 14px;
  color: #555;
}

.zoom-controls {
  display: flex;
  align-items: center;
}

/* 红色按钮样式 */
.zoom-controls button {
  font-size: 16px;
  padding: 8px;
  background-color: #e74c3c; /* 红色背景 */
  color: #fff; /* 文字颜色为白色 */
  border: none; /* 去掉边框 */
  border-radius: 10px; /* 圆角边框 */
  cursor: pointer; /* 鼠标悬浮时为手型 */
  transition: all 0.3s ease-in-out; /* 平滑过渡 */
}

.zoom-controls button:hover {
  background-color: #c0392b; /* 鼠标悬浮时稍微暗一点的红色 */
  transform: scale(1.05); /* 鼠标悬浮时按钮轻微放大 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 增加阴影效果 */
}

.zoom-controls button:active {
  background-color: #e74c3c; /* 鼠标按下时背景色恢复为原红色 */
  transform: scale(1); /* 鼠标按下时还原按钮大小 */
}


.zoom-controls span {
  font-size: 16px;
  margin: 0 10px;
}

.editable-textarea {
  width: 100%;
  height: 150px;
  margin-bottom: 10px;
  font-size: 14px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.selection-buttons {
  position: absolute;
  top: 300px;
  left: 300px;
  z-index: 9999;
  background-color: rgba(255, 255, 255, 0.8);
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
}

.selection-buttons button {
  margin-right: 10px;
  padding: 5px 10px;
}

/* Quill 工具栏样式调整 */
.ql-toolbar {
  margin: 0 auto;
  width: 70%;
  cursor: pointer !important;
  border-radius: 4px 4px 0 0;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
}

/* Quill 编辑器容器 */
.note-detail-container {
  padding: 0px 10px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.title-input {
  font-size: 28px;
  color: black;
  border: none;
  border-bottom: 1px solid #ddd;
  outline: none;
  padding: 5px;
  text-align: center;
}

.note-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 0px;
  padding: 0;
}

.actions {
  margin-top: 20px;
}

.actions button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #4caf50;
  color: white;
}

.actions button:hover {
  background-color: #45a049;
}

/* 返回按钮样式 */
.back-button {
  padding: 5px 15px;
  font-size: 16px;
  background-color: #2d6a4f; /* 深绿色背景 */
  border: 1px solid #2d6a4f; /* 与背景色一致的边框 */
  border-radius: 20%; /* 圆形边框 */
  color: #fff; /* 文字颜色为白色 */
  cursor: pointer; /* 鼠标悬浮时为手型 */
  transition: all 0.3s ease-in-out; /* 平滑过渡 */
}

.back-button:hover {
  background-color: #1a4f34; /* 鼠标悬浮时稍微暗一点的绿色 */
  transform: scale(1.05); /* 鼠标悬浮时按钮轻微放大 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 增加阴影效果 */
}

</style>

