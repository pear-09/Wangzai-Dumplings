<template>
  <!-- 将 v-if="visible" 移动到这里 -->
  <div class="modal-overlay" v-if="visible" @click.self="closeModal">
    <transition name="modal-fade">
      <div class="modal-content" v-if="visible">
        <!-- 标题区域 -->
        <div class="modal-header">
          <h2>{{ title }}</h2>
          <button class="close-button" @click="closeModal">&times;</button>
        </div>
        <!-- 内容区域 -->
        <div class="modal-body">
          <slot></slot>
        </div>
        <!-- 按钮区域 -->
        <div class="modal-footer">
          <button class="confirm-button" @click="handleConfirm">确定</button>
          <button class="cancel-button" @click="closeModal">取消</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';

export default defineComponent({
  name: 'Modal',
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
    title: {
      type: String,
      default: '',
    },
  },
  emits: ['close', 'update:modelValue', 'confirm'],
  setup(props, { emit }) {
    const visible = ref(props.modelValue);

    watch(
      () => props.modelValue,
      (newVal) => {
        visible.value = newVal;
      }
    );

    const closeModal = () => {
      visible.value = false;
      emit('close');
      emit('update:modelValue', false);
    };

    const handleConfirm = () => {
      emit('confirm');
      closeModal();
    };

    return {
      visible,
      closeModal,
      handleConfirm,
    };
  },
});
</script>

<style scoped>
/* 模态框遮罩层 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3); /* 轻盈的遮罩 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* 模态框内容 */
.modal-content {
  background-color: #ffffff; /* 白色背景 */
  padding: 20px;
  border-radius: 10px;
  position: relative;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1); /* 轻盈的阴影 */
  display: flex;
  flex-direction: column;
}

/* 标题区域 */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.modal-header h2 {
  margin: 0;
  font-size: 24px;
  color: #2f4f4f; /* 深灰绿色 */
}

/* 关闭按钮 */
.close-button {
  border: none;
  background: none;
  font-size: 24px;
  cursor: pointer;
  color: #2f4f4f; /* 深灰绿色 */
}

/* 内容区域 */
.modal-body {
  flex-grow: 1;
  margin-bottom: 20px;
}

/* 按钮区域 */
.modal-footer {
  display: flex;
  justify-content: flex-end;
}

.confirm-button {
  padding: 10px 20px;
  background-color: #7bd389; /* 清新的绿色 */
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 10px;
}

.confirm-button:hover {
  background-color: #6ccf7d;
}

.cancel-button {
  padding: 10px 20px;
  background-color: #c0c0c0; /* 灰色取消按钮 */
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.cancel-button:hover {
  background-color: #a9a9a9;
}

/* 过渡动画 */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* 表单元素样式 */
.modal-body form {
  display: flex;
  flex-direction: column;
}

.modal-body form div {
  margin-bottom: 15px;
}

.modal-body label {
  font-weight: bold;
  margin-bottom: 5px;
  color: #2f4f4f; /* 深灰绿色 */
}

.modal-body input,
.modal-body textarea {
  padding: 10px;
  border: 1px solid #dcdcdc;
  border-radius: 5px;
  font-size: 16px;
  background-color: #f8f8f8; /* 浅灰色背景 */
  color: #333;
}

.modal-body input:focus,
.modal-body textarea:focus {
  outline: none;
  border-color: #7bd389; /* 焦点时的绿色边框 */
}
</style>
