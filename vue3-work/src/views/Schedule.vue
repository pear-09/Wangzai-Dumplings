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

  <!-- 背景图片 -->
  <div v-if="selectedEvents.length === 0" class="no-events">
    <img src="@/assets/no-events.png" alt="无日程" />
    <p>今天没有日程，休息一下吧！</p>
  </div>

  <!-- 日程列表 -->
  <div
    v-for="event in selectedEvents"
    :key="event.id"
    class="event-item"
    :class="{ complete: event.status === '完成', pending: event.status === '未完成' }"
  >
    <div class="event-box">
      <div class="event-title">{{ event.title }}</div>
      <div class="status-box-container">
        <div
          class="status-box"
          :class="{
            complete: event.status === '完成',
            pending: event.status === '未完成',
          }"
          @click="toggleStatus(event)"
        >
          <span v-if="event.status === '完成'">√</span>
          <span v-if="event.status === '未完成'">-</span>
        </div>
      </div>
    </div>
  </div>
</div>

    <!-- 弹窗表单 -->
    <Modal v-model="modalVisible" title="日程管理" @confirm="handleFormSubmit">
  <form class="modal-form" @submit.prevent="handleFormSubmit">
    <!-- 标题输入 -->
    <div class="form-group">
      <label for="title">标题：</label>
      <input
        id="title"
        type="text"
        v-model="currentEvent.title"
        placeholder="请输入标题"
        required
      />
    </div>

    <!-- 描述输入 -->
    <div class="form-group">
      <label for="description">描述：</label>
      <textarea
        id="description"
        v-model="currentEvent.description"
        placeholder="请输入描述"
      ></textarea>
    </div>

    <!-- 时间输入 -->
    <div class="form-group">
      <label for="time">时间：</label>
      <input
        id="time"
        type="datetime-local"
        v-model="currentEvent.time"
        required
      />
    </div>

    <!-- 状态切换按钮 -->
    <div class="form-group">
      <label>状态：</label>
      <div class="status-buttons">
        <button
          type="button"
          class="status-btn"
          :class="{ active: currentEvent.status === '完成' }"
          @click="toggleStatus(currentEvent)"
        >
          完成
        </button>
        <button
          type="button"
          class="status-btn"
          :class="{ active: currentEvent.status === '未完成' }"
          @click="toggleStatus(currentEvent)"
        >
          未完成
        </button>
      </div>
    </div>

    <!-- 删除按钮 -->
    <div class="form-actions" v-if="currentEvent.id">
      <button
        type="button"
        class="delete-btn"
        @click="deleteEvent"
      >
        删除
      </button>
    </div>

    <!-- 确定按钮 -->
    <div class="form-actions">
      <button type="submit" class="confirm-btn">保存</button>
    </div>
  </form>
</Modal>

  </div>
</template>
<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { Calendar } from "@fullcalendar/core";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import request from "@/utils/request";
import Modal from "@/components/Modal.vue";

export default defineComponent({
  name: "ScheduleView",
  components: { Modal },
  setup() {
    const modalVisible = ref(false);
    const currentEvent = ref({
      id: null,
      title: "",
      description: "",
      time: "",
      status: "未完成",
    });
    const calendar = ref<Calendar | null>(null);
    const events = ref([]);
    const selectedDate = ref("");
    const selectedEvents = ref([]);

    const fetchEvents = async () => {
      try {
        const response = await request.get("/ez-note/date/get-all");
        if (response.code === 0) {
          events.value = response.data.map((event) => ({
            id: event.id.toString(),
            title: event.title,
            start: event.time.split("T")[0],
            backgroundColor: event.status === "完成" ? "lightgray" : "white",
            extendedProps: { status: event.status },
          }));
          updateSelectedEvents(selectedDate.value || new Date().toISOString().split("T")[0]);
          refetchCalendarEvents();
        }
      } catch (error) {
        console.error("Error fetching events:", error);
      }
    };

    const updateSelectedEvents = (date) => {
      selectedDate.value = date;
      selectedEvents.value = events.value.filter((event) => event.start === date);
    };

    const refetchCalendarEvents = () => {
      if (calendar.value) {
        calendar.value.removeAllEvents();
        calendar.value.addEventSource(events.value);
        calendar.value.render();
      }
    };

    const initializeCalendar = async () => {
      await fetchEvents();
      const calendarEl = document.getElementById("calendar");
      if (calendarEl) {
        calendar.value = new Calendar(calendarEl, {
          plugins: [dayGridPlugin, interactionPlugin],
          initialView: "dayGridMonth",
          height: "100%", /* 日历高度填充容器 */
          events: events.value,
          dateClick(info) {
            updateSelectedEvents(info.dateStr);
          },
        });
        calendar.value.render();
      }
    };

    const handleFormSubmit = async () => {
      try {
        if (currentEvent.value.id) {
          // 更新日程
          await request.post("/ez-note/date/modify", {
            date_id: Number(currentEvent.value.id),
            title: currentEvent.value.title,
            description: currentEvent.value.description,
            time: currentEvent.value.time,
          });
        } else {
          // 新增日程
          await request.post("/ez-note/date/create", {
            title: currentEvent.value.title,
            description: currentEvent.value.description,
            time: currentEvent.value.time,
          });
        }
        modalVisible.value = false;
        await fetchEvents(); // 刷新事件数据
      } catch (error) {
        console.error("Error saving event:", error);
      }
    };

    const toggleStatus = async (event) => {
      try {
        const newStatus = event.status === "完成" ? "未完成" : "完成";
        await request.post("/ez-note/date/status", {
          date_id: Number(event.id),
          status: newStatus,
        });
        event.status = newStatus;
        updateSelectedEvents(selectedDate.value);
        refetchCalendarEvents(); // 更新日历视图
      } catch (error) {
        console.error("Error updating status:", error);
      }
    };

    const deleteEvent = async () => {
      if (currentEvent.value.id) {
        try {
          await request.post("/ez-note/date/delete", {
            date_id: currentEvent.value.id,
          });
          modalVisible.value = false;
          await fetchEvents(); // 刷新事件数据
        } catch (error) {
          console.error("Error deleting event:", error);
        }
      }
    };

    const openCreateEventModal = () => {
      currentEvent.value = { id: null, title: "", description: "", time: "", status: "未完成" };
      modalVisible.value = true;
    };

    onMounted(() => initializeCalendar());

    return {
      modalVisible,
      currentEvent,
      selectedDate,
      selectedEvents,
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
  justify-content: space-between;
  padding: 10px;
  height: 88vh; /* 整个容器适配屏幕高度 */
  box-sizing: border-box; /* 包含内边距 */
  overflow: hidden; /* 避免内部溢出 */
}

.calendar-left {
  width: 60%;
  height: 100%; /* 高度继承父容器 */
  overflow: auto; /* 如果内容超出，启用滚动条 */
}

.schedule-right {
  width: 35%;
  padding: 10px;
  border: 3px solid #9cc47c;
  border-radius: 4px;
  background-color: #ffffff;
  height: 95%; /* 高度继承父容器 */
  overflow-y: auto; /* 启用垂直滚动条，防止溢出 */
}


.no-events {
  text-align: center;
  padding: 20px;
}

.no-events img {
  width: 50%;
  margin-bottom: 10px;
}

.no-events p {
  color: #abdaf1;
}

.event-item.complete {
  background-color: #d3d3d3;
  color: #505050;
}

.event-item.pending {
  background-color: #fff;
}

.status-box.complete {
  background-color: #4caf50;
  color: white;
}

.add-btn {
  width: 40px;
  height: 40px;
  font-size: 24px;
  background: linear-gradient(135deg, #ff7f50, #ff6347);
  color: white;
  border: none;
  border-radius: 50%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-btn:hover {
  transform: scale(1.1); /* 悬停放大 */
  background: linear-gradient(135deg, #ff6347, #ff4500); /* 渐变颜色变深 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.add-btn:active {
  transform: scale(0.95); /* 点击时稍微缩小 */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.modal-form input,
.modal-form textarea {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.modal-form input:focus,
.modal-form textarea:focus {
  border-color: #7bd389;
  box-shadow: 0 0 6px rgba(123, 211, 137, 0.5);
  outline: none;
}

.modal-form textarea {
  resize: vertical;
  min-height: 100px;
}

.status-buttons {
  display: flex;
  gap: 10px;
}

.status-btn {
  padding: 8px 16px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f0f0f0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.status-btn.active {
  background-color: #7bd389;
  color: white;
  border-color: #7bd389;
}

.status-btn:hover {
  background-color: #e0f7ea;
}

.delete-btn {
  background-color: #ff6347;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.delete-btn:hover {
  background-color: #ff4500;
}

.confirm-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.confirm-btn:hover {
  background-color: #45a049;
}


</style>
