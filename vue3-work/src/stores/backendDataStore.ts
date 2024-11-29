// stores/backendDataStore.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';

// 定义 store 的类型
export const useBackendDataStore = defineStore('backendData', () => {
    // 使用 ref 定义 backendData 的类型为 string
    const backendData = ref<string>('');

    // 设置数据的方法，确保参数类型为 string
    const setBackendData = (data: string): void => {
        backendData.value = data;
    };

    // 返回 backendData 和 setBackendData 方法
    return { backendData, setBackendData };
});
