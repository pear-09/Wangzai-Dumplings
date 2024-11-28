<template>
  <div class="schedule-container">
    <!-- 日历部分 -->
    <div class="calendar-left">
      <div id="calendar"></div>
    </div>
    <!-- 日程部分 -->
    <div class="schedule-right">
      <div class="header">
        <h3>{{ selectedDate }} 日程</h3>
        <button class="add-btn" @click="openCreateEventModal">+</button>
      </div>
      <div v-for="event in selectedEvents" :key="event.id" class="event-item"
           :class="{ 'completed': event.status === '完成', 'pending': event.status === '未完成' }">
        <div class="event-box">
          <div class="event-title">{{ event.title }}</div>
          <!-- <div class="event-time">{{ event.time }}</div> -->
          <div class="status-box-container">
            <div class="status-box"
                 :class="{
                   complete: event.status === '完成',
                   pending: event.status === '未完成'
                 }"
                 @click="toggleStatus(event)">
              <span v-if="event.status === '完成'">√</span>
              <span v-if="event.status === '未完成'">-</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 弹窗表单 -->
    <Modal v-model="modalVisible" title="日程管理" @confirm="handleFormSubmit">
      <div class="modal-form">
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
          <button v-if="currentEvent.status === '未完成'" @click="toggleStatus(currentEvent)">完成</button>
          <button v-else @click="toggleStatus(currentEvent)">未完成</button>
        </div>
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
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import { DateClickArg } from "@fullcalendar/interaction";
import request from "@/utils/request"; // 自定义的请求实例
import Modal from "@/components/Modal.vue";
import { TaskData } from "@/types/api/UpdateTask.d.ts"; 

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
    const events = ref<EventInput[]>([]); // 所有日程
    const selectedDate = ref<string>(''); // 当前选中的日期
    const selectedEvents = ref<any[]>([]); // 当前选中日期的日程

    // 获取所有日程（用于日历）
    const fetchEvents = async () => {
      try {
        const response = await request.get("/ez-note/date/get-all");
        if (response.code === 0) {
          events.value = response.data.map((event: TaskData) => ({
            id: event.id.toString(),
            title: event.title,
            start: event.time.split("T")[0], // 提取日期部分
            backgroundColor: event.status === "完成" ? "lightblue" : "darkblue",
            extendedProps: {
              status: event.status,
            },
          }));

          // 获取今天的日期，并更新选中的日期及日程
          const today = new Date().toISOString().split("T")[0]; 
          selectedDate.value = today;
          selectedEvents.value = events.value.filter((event) => event.start === today);
        }
      } catch (error) {
        console.error("Error fetching events:", error);
      }
    };

    // 获取选中日期的日程（用于右侧日程栏）
    const fetchSelectedDayEvents = async (date: string) => {
      try {
        const response = await request.get(`/ez-note/date/get?time=${date}`);
        if (response.code === 0) {
          selectedEvents.value = response.data.map((event: TaskData) => ({
            id: event.id.toString(),
            title: event.title,
            time: event.time,
            status: event.status,
          }));
        }
      } catch (error) {
        console.error("Error fetching selected date events:", error);
      }
    };

    // 初始化日历
    const initializeCalendar = async () => {
      await fetchEvents(); // 获取所有事件
      const calendarEl = document.getElementById("calendar");

      if (calendarEl) {
        calendar.value = new Calendar(calendarEl, {
          plugins: [dayGridPlugin, interactionPlugin],
          initialView: "dayGridMonth",
          events: events.value,
          dateClick(info: DateClickArg) {
            selectedDate.value = info.dateStr; // 设置选中的日期
            fetchSelectedDayEvents(info.dateStr); // 获取并显示选中日期的事件
          },
        });

        calendar.value.render();
      } else {
        console.error("Calendar element not found");
      }
    };

    // 提交表单（新增或更新日程）
    const handleFormSubmit = async () => {
      try {
        if (currentEvent.value.id) {
          await request.post("/ez-note/date/modify", {
            date_id: Number(currentEvent.value.id),
            title: currentEvent.value.title,
            description: currentEvent.value.description,
            time: currentEvent.value.time,
          });
        } else {
          await request.post("/ez-note/date/create", {
            title: currentEvent.value.title,
            description: currentEvent.value.description,
            time: currentEvent.value.time,
          });
        }
        modalVisible.value = false;
        await fetchEvents(); // 更新所有日程
        fetchSelectedDayEvents(selectedDate.value); // 更新右侧显示的日程
      } catch (error) {
        console.error("Error saving event:", error);
      }
    };

    // 切换日程状态
    const toggleStatus = async (event: any) => {
      try {
        const newStatus = event.status === '完成' ? '未完成' : '完成';
        // 更新事件状态到后端
        await request.post("/ez-note/date/status", {
          date_id: Number(event.id),
          status: newStatus,
        });

        // 更新本地状态
        event.status = newStatus;
        event.backgroundColor = newStatus === '完成' ? 'lightblue' : 'darkblue';
        event.extendedProps.status = newStatus;

        // 同步更新右侧的事件列表
        selectedEvents.value = selectedEvents.value.map((e) => 
          e.id === event.id ? { ...e, status: newStatus, backgroundColor: event.backgroundColor } : e
        );

        // 刷新日历事件
        if (calendar.value) {
          calendar.value.refetchEvents(); // 刷新日历上的事件
        }
      } catch (error) {
        console.error("Error updating status:", error);
      }
    };

    // 删除事件
    const deleteEvent = async () => {
      if (currentEvent.value.id) {
        try {
          await request.post('/ez-note/date/delete', {
            date_id: currentEvent.value.id
          });
          modalVisible.value = false;
          await fetchEvents(); // 更新所有日程
          fetchSelectedDayEvents(selectedDate.value); // 更新右侧显示的日程
        } catch (error) {
          console.error("Error deleting event:", error);
        }
      }
    };

    // 打开创建日程弹窗
    const openCreateEventModal = () => {
      currentEvent.value = {
        id: null,
        title: '',
        description: '',
        time: '',
        status: '未完成',
      };
      modalVisible.value = true;
    };

    onMounted(() => {
      initializeCalendar(); // 初始化日历
      // 获取今天的日期，并传递给 fetchSelectedDayEvents
  const today = new Date().toISOString().split("T")[0]; // 获取今天的日期（yyyy-mm-dd）
  fetchSelectedDayEvents(today); // 自动触发，传递当天日期
    });

    return {
      modalVisible,
      currentEvent,
      selectedDate,
      selectedEvents,
      fetchEvents,
      fetchSelectedDayEvents,
      handleFormSubmit,
      toggleStatus,
      deleteEvent,
      openCreateEventModal,
    };
  },
});
</script>


<style scoped>
.schedule-container {
  display: flex;
  gap: 20px;
  padding: 20px;
}

.calendar-left {
  width: 70%;
}

.schedule-right {
  width: 30%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  position: relative;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.add-btn {
  font-size: 24px;
  background-color: #ff6347;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 50%;
  cursor: pointer;
}

.add-btn:hover {
  background-color: #ff4500;
}

.event-item {
  
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.event-item.complete {
  background-color: #d3d3d3; /* 灰色背景 */
  color: #707070; /* 深灰色字体 */
}

.event-item.pending {
  background-color: #fff; /* 白色背景 */
  color: #000; /* 默认字体颜色 */
}

.status-box {
  width: 24px;
  height: 24px;
  border: 2px solid #4caf50;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  cursor: pointer;
}

.status-box.complete {
  background-color: #4caf50; /* 绿色背景 */
}

.status-box.pending {
  background-color: #fff; /* 白色背景 */
  border: 2px solid #ddd; /* 灰色边框 */
}

.status-box-container {
  display: flex;
  justify-content: flex-end;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.modal-form input,
.modal-form textarea {
  width: 100%;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.modal-form button {
  padding: 10px;
  border: none;
  border-radius: 4px;
  background-color: #ff6347;
  color: white;
  cursor: pointer;
}

.modal-form button:hover {
  background-color: #ff4500;
}
</style>