<template>
  <div class="schedule-container">
    <div id="calendar"></div>
    <!-- 弹窗表单，用于增删改 -->
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
import axios from "axios";
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
    }>({
      id: null,
      title: "",
      description: "",
      time: "",
    });

    const calendar = ref<Calendar | null>(null);
    const events = ref<EventInput[]>([]);
    const fetchEvents = async () => {
  try {
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/ez-note/date/get`
    );
    if (response.data.code === 0) {
      // 输出原始数据
      console.log("Raw data from API:", response.data.data);

      events.value = response.data.data.map((event: TaskData) => ({
        id: event.id.toString(),
        title: event.title,
        start: event.time,
        extendedProps: {
          description: event.description,
        },
      }));

      // 输出处理后的事件数据
      console.log("Processed events:", events.value);
    }
  } catch (error) {
    console.error("Error fetching events:", error);
  }
};


    const initializeCalendar = async () => {
      await fetchEvents();
      const calendarEl = document.getElementById("calendar");

      if (calendarEl) {
        calendar.value = new Calendar(calendarEl, {
          plugins: [dayGridPlugin, interactionPlugin],
          initialView: "dayGridMonth",
          events: events.value,
          dateClick(info: DateClickArg) {
            currentEvent.value = {
              id: null,
              title: "",
              description: "",
              time: info.dateStr,
            };
            modalVisible.value = true;
          },
          eventClick(info: EventClickArg) {
            const eventId = info.event.id || ""; // 确保 eventId 为 string
            const event = events.value.find((e) => e.id === eventId);
            if (event) {
              currentEvent.value = {
                id: event.id ?? null, // 处理可能的 undefined
                title: event.title as string,
                description: event.extendedProps?.description || "",
                time: event.start as string,
              };
              modalVisible.value = true;
            }
          },
        });
        calendar.value.render();
      } else {
        console.error("Calendar element not found");
      }
    };

  const handleFormSubmit = async () => {
  try {
    if (currentEvent.value.id) {
      // Update event
      await axios.post(`${import.meta.env.VITE_API_URL}/ez-note/date/modify`, {
        date_id: Number(currentEvent.value.id),
        title: currentEvent.value.title,
        description: currentEvent.value.description,
        time: currentEvent.value.time,
      });
    } else {
      // Create event
      await axios.post(`${import.meta.env.VITE_API_URL}/ez-note/date/create`, {
        title: currentEvent.value.title,
        description: currentEvent.value.description,
        time: currentEvent.value.time,
      });
    }
    modalVisible.value = false;
    // Refresh calendar events
    if (calendar.value) {
      await fetchEvents();
      calendar.value.removeAllEvents();
      calendar.value.addEventSource(events.value);
    }
  } catch (error) {
    console.error("Error saving event:", error);
  }
};


    onMounted(() => {
      initializeCalendar();
    });

    return {
      modalVisible,
      currentEvent,
      handleFormSubmit,
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
</style>
