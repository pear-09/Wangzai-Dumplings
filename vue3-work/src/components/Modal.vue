<template>
  <div class="modal-overlay" v-if="visible">
    <transition name="modal-fade">
      <div class="modal-content" v-if="visible">
        <!-- 标题区域 -->
        <div class="modal-header">
          <h2>{{ title }}</h2>
          <!-- 可以选择是否显示关闭按钮 -->
          <button v-if="showClose" class="close-button" @click="closeModal">&times;</button>
        </div>
        <!-- 内容区域 -->
        <div class="modal-body">
          <slot></slot>
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
    // 添加是否显示关闭按钮的属性
    showClose: {
      type: Boolean,
      default: false,
    },
    // 添加是否允许点击遮罩关闭的属性
    maskClosable: {
      type: Boolean,
      default: false,
    }
  },
  emits: ['close', 'update:modelValue'],
  setup(props, { emit }) {
    const visible = ref(props.modelValue);

    watch(
      () => props.modelValue,
      (newVal) => {
        visible.value = newVal;
      }
    );

    const closeModal = () => {
      // 只有当允许关闭时才执行关闭操作
      if (props.maskClosable || props.showClose) {
        visible.value = false;
        emit('close');
        emit('update:modelValue', false);
      }
    };

    return {
      visible,
      closeModal,
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
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* 模态框内容 */
.modal-content {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  position: relative;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
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
  color: #2f4f4f;
}

/* 关闭按钮 */
.close-button {
  border: none;
  background: none;
  font-size: 24px;
  cursor: pointer;
  color: #2f4f4f;
  transition: color 0.3s ease;
}

.close-button:hover {
  color: #ff4d4f;
}

/* 内容区域 */
.modal-body {
  flex-grow: 1;
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
  color: #2f4f4f;
}

.modal-body input,
.modal-body textarea {
  padding: 10px;
  border: 1px solid #dcdcdc;
  border-radius: 5px;
  font-size: 16px;
  background-color: #f8f8f8;
  color: #333;
}

.modal-body input:focus,
.modal-body textarea:focus {
  outline: none;
  border-color: #7bd389;
}
</style>
