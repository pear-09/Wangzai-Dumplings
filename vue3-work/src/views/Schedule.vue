<template>
  <div class="schedule-container">
    <div id="calendar"></div>
    <!-- 弹窗表单 -->
    <Modal v-model="modalVisible" title="日程管理" @confirm="handleFormSubmit">
      <div class="modal-form">
        <!-- 表单字段 -->
        <div>
          <label>标题：</label>
          <input v-model="currentEvent.title" required />
        </div>
        <div>
          <label>描述：</label>
          <textarea v-model="currentEvent.description"></textarea>
        </div>
        <div>
          <label>时间：</label>
          <input type="datetime-local" v-model="currentEvent.time" required />
        </div>
        <div>
          <label>状态：</label>
          <button v-if="currentEvent.status === '未完成'" @click="toggleStatus('完成')">完成</button>
          <button v-else @click="toggleStatus('未完成')">未完成</button>
        </div>
        <!-- 删除按钮 -->
        <div v-if="currentEvent.id">
          <button @click="deleteEvent">删除</button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { Calendar } from "@fullcalendar/core";
import type { EventInput } from "@fullcalendar/core";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import type { DateClickArg } from "@fullcalendar/interaction";
import type { EventClickArg } from "@fullcalendar/core";
import request from "@/utils/request"; // 自定义的请求实例
import Modal from "@/components/Modal.vue";

// 引入 TaskData 类型
import type { TaskData } from "@/types/api/UpdateTask.d.ts"; // 请根据实际路径调整

export default defineComponent({
  name: "ScheduleView",
  components: { Modal },
  setup() {
    const modalVisible = ref(false);
    const currentEvent = ref<{
      id: string | null | undefined;
      title: string;
      description: string;
      time: string;
      status: string;
    }>({
      id: null,
      title: "",
      description: "",
      time: "",
      status: "未完成", // 默认状态为未完成
    });

    const calendar = ref<Calendar | null>(null);
    const events = ref<EventInput[]>([]);

    /**
     * 从后端获取所有日程并处理
     */
    const fetchEvents = async () => {
      try {
        const response = await request.get("/ez-note/date/get-all");
        if (response.code === 0) {
          // 将后端返回的数据转换为 FullCalendar 的事件格式
          events.value = response.data.map((event: TaskData) => ({
            id: event.id.toString(),
            title: event.title,
            start: event.time.split("T")[0], // 提取日期部分，忽略时间
            backgroundColor: event.status === "完成" ? "lightblue" : "darkblue", // 设置不同颜色
            extendedProps: {
              status: event.status,
            },
          }));
        }
      } catch (error) {
        console.error("Error fetching events:", error);
      }
    };

    /**
     * 初始化 FullCalendar
     */
    const initializeCalendar = async () => {
      await fetchEvents(); // 获取事件数据
      const calendarEl = document.getElementById("calendar");

      if (calendarEl) {
        calendar.value = new Calendar(calendarEl, {
          plugins: [dayGridPlugin, interactionPlugin],
          initialView: "dayGridMonth",
          events: events.value, // 设置事件数据源
          dateClick(info: DateClickArg) {
            // 点击日期，创建新日程
            currentEvent.value = {
              id: null,
              title: "",
              description: "",
              time: info.dateStr,
              status: "未完成", // 新建时默认未完成
            };
            modalVisible.value = true; // 弹出“创建日程”弹窗
          },
          eventClick(info: EventClickArg) {
            // 点击已创建事件，弹出“日程管理弹窗”
            const eventId = info.event.id || ""; // 确保 eventId 为字符串
            getSingleEvent(eventId); // 获取单个日程详情
          },
          eventContent(info: EventClickArg) {
            const statusBox = document.createElement('div');
            statusBox.style.display = 'inline-block';
            statusBox.style.width = '20px';
            statusBox.style.height = '20px';
            statusBox.style.marginLeft = '10px';
            statusBox.style.border = '1px solid #ccc';
            statusBox.style.borderRadius = '4px';
            statusBox.style.textAlign = 'center';
            statusBox.style.lineHeight = '20px';
            statusBox.style.cursor = 'pointer'; // 提示用户可以点击

            if (info.event.extendedProps.status === '完成') {
              statusBox.textContent = '√'; // 显示“√”标记
              statusBox.style.backgroundColor = 'green'; // 完成状态使用绿色
            } else {
              statusBox.textContent = ''; // 空白
              statusBox.style.backgroundColor = 'white'; // 未完成状态使用白色
            }

            // 确保状态框点击事件绑定
            statusBox.addEventListener('click', async (event) => {
              event.stopPropagation(); // 阻止事件冒泡
              const newStatus = info.event.extendedProps.status === '完成' ? '未完成' : '完成';
              console.log('点击状态框，更新状态为:', newStatus); // 调试日志
              await toggleStatus(newStatus, info.event); // 切换状态并更新UI
            });

            const eventElement = document.createElement('div');
            eventElement.style.display = 'flex';
            eventElement.style.alignItems = 'center';

            const eventTitle = document.createElement('span');
            eventTitle.textContent = info.event.title;
            eventElement.appendChild(eventTitle);

            eventElement.appendChild(statusBox); // 添加状态框到事件元素中
            return { domNodes: [eventElement] };
          },
        });

        calendar.value.render();
      } else {
        console.error("Calendar element not found");
      }
    };

    /**
     * 获取单个日程的详细信息
     */
    const getSingleEvent = async (eventId: string) => {
      try {
        const response = await request.get(`/ez-note/date/get-single?id=${eventId}`);
        if (response.code === 0 && response.data) {
          currentEvent.value = response.data; // 设置当前日程的详细信息
          modalVisible.value = true; // 弹出“日程管理”弹窗
        }
      } catch (error) {
        console.error("Error fetching single event:", error);
      }
    };

    /**
     * 提交表单（新增或更新日程）
     */
    const handleFormSubmit = async () => {
      try {
        if (currentEvent.value.id) {
          // 更新事件
          await request.post("/ez-note/date/modify", {
            date_id: Number(currentEvent.value.id),
            title: currentEvent.value.title,
            description: currentEvent.value.description,
            time: currentEvent.value.time,
          });
        } else {
          // 新增事件
          await request.post("/ez-note/date/create", {
            title: currentEvent.value.title,
            description: currentEvent.value.description,
            time: currentEvent.value.time,
          });
        }
        modalVisible.value = false;
        // 刷新事件
        if (calendar.value) {
          await fetchEvents();
          calendar.value.removeAllEvents(); // 移除所有现有事件
          calendar.value.addEventSource(events.value); // 添加新的事件数据源
        }
      } catch (error) {
        console.error("Error saving event:", error);
      }
    };

    /**
     * 切换日程状态并更新UI
     */
    const toggleStatus = async (status: string, event: any) => {
      try {
        if (event.id) {
          // 更新日程状态
          await request.post("/ez-note/date/status", {
            date_id: Number(event.id),
            status,
          });
          event.extendedProps.status = status; // 更新本地事件状态
          event.setProp('backgroundColor', status === '完成' ? 'lightblue' : 'darkblue'); // 更新事件背景色
          // 更新 FullCalendar 中的事件状态
          if (calendar.value) {
            calendar.value.refetchEvents(); // 强制刷新事件
          }
        }
      } catch (error) {
        console.error("Error updating status:", error);
      }
    };

    /**
 * 删除日程
 */
const deleteEvent = async () => {
  if (currentEvent.value.id) {
    try {
      await request.post('/ez-note/date/delete', {
        date_id: currentEvent.value.id  // 传递要删除的日程ID
      });
      modalVisible.value = false;
      // 刷新事件
      if (calendar.value) {
        await fetchEvents();
        calendar.value.removeAllEvents(); // 移除所有现有事件
        calendar.value.addEventSource(events.value); // 添加新的事件数据源
      }
    } catch (error) {
      console.error("Error deleting event:", error);
    }
  }
};

    onMounted(() => {
      initializeCalendar(); // 初始化日程日历
    });

    return {
      modalVisible,
      currentEvent,
      fetchEvents,
      handleFormSubmit,
      deleteEvent,
    };
  },
});
</script>



<style scoped>
.schedule-container {
  padding: 20px;
}
#calendar {
  max-width: 900px;
  margin: 0 auto;
}
form div {
  margin-bottom: 10px;
}
.schedule-container .fc-daygrid-event {
  display: flex; 
  align-items: center;
}

.schedule-container .fc-daygrid-event .status-box {
  width: 20px;
  height: 20px;
  margin-left: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  text-align: center;
  line-height: 20px;
}

.schedule-container .fc-daygrid-event.complete .status-box {
  background-color: green;
  color: white;
}

.schedule-container .fc-daygrid-event.pending .status-box {
  background-color: white;
}
</style>
