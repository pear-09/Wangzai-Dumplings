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
          <div class="status-indicator" @click="toggleStatus(event)">
            <span class="status-icon">
              {{ event.status === '完成' ? '✓' : '' }}
            </span>
          </div>
          <div class="event-content">
            <div class="event-header">
              <div class="event-title">{{ event.title }}</div>
              <div class="event-actions">
                <button class="edit-btn" @click="openEditEventModal(event)">
                  <i class="fas fa-edit"></i>编辑
                </button>
              </div>
            </div>
            <div v-if="event.description" class="event-description">
              {{ event.description }}
            </div>
            <div class="event-time">
              {{ formatEventTime(event.time) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 弹窗表单 -->
    <Modal 
      v-model="modalVisible" 
      :title="modalTitle"
      :show-close="false"      
      :mask-closable="false"   
      :show-footer="false"
    >
      <div class="modal-form">
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
          <span class="error-message" v-if="showErrors && !currentEvent.title.trim()">
            标题不能为空
          </span>
        </div>

        <!-- 描述输入 -->
        <div class="form-group">
          <label for="description">描述：</label>
          <textarea
            id="description"
            v-model="currentEvent.description"
            placeholder="请输入描述"
            required
          ></textarea>
          <span class="error-message" v-if="showErrors && !currentEvent.description.trim()">
            描述不能为空
          </span>
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

        <!-- 按钮组 -->
        <div class="form-actions">
          <div class="action-left">
            <button
              v-if="currentEvent.id"
              type="button"
              class="delete-btn"
              @click="deleteEvent"
            >
              删除
            </button>
          </div>
          <div class="action-right">
            <button type="button" class="cancel-btn" @click="handleCancel">
              取消
            </button>
            <button type="button" class="save-btn" @click="handleFormSubmit">
              保存
            </button>
          </div>
        </div>
      </div>
    </Modal>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Calendar } from '@fullcalendar/core'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import request from '@/utils/request'
import Modal from '@/components/Modal.vue'

// 响应式状态
const modalVisible = ref(false)
const currentEvent = ref({
  id: null,
  title: '',
  description: '',
  time: '',
  status: '未完成'
})
const calendar = ref<Calendar | null>(null)
const events = ref([])
const selectedDate = ref('')
const selectedEvents = ref([])

// 计算属性
const modalTitle = computed(() => currentEvent.value.id ? '编辑日程' : '新建日程')

// 格式化时间
const formatEventTime = (time: string) => {
  try {
    const date = new Date(time);
    if (isNaN(date.getTime())) {
      return '时间未设置';
    }

    // 获取本地时区的时间
    const localDate = new Date(date.getTime() + (date.getTimezoneOffset() * 60000));

    // 获取年月日时分
    const year = localDate.getFullYear();
    const month = localDate.getMonth() + 1;
    const day = localDate.getDate();
    const hours = String(localDate.getHours()).padStart(2, '0');
    const minutes = String(localDate.getMinutes()).padStart(2, '0');

    // 判断是否是今年
    const currentYear = new Date().getFullYear();
    const showYear = year !== currentYear;

    // 组装显示文本
    let dateText = showYear ? 
      `${year}年${month}月${day}日` : 
      `${month}月${day}日`;

    return `${dateText} ${hours}:${minutes}`;
  } catch (error) {
    console.error('Error formatting time:', error);
    return '时间格式错误';
  }
}

// 打开编辑模态框
const openEditEventModal = (event) => {
  showErrors.value = false // 重置错误显示状态
  
  // 创建一个新的日期对象
  const eventDate = new Date(event.time)
  
  // 补偿时区差，获取正确的本地时间
  const timezoneOffset = eventDate.getTimezoneOffset() * 60000
  const localDate = new Date(eventDate.getTime() + timezoneOffset)
  
  // 格式化日期时间字符串
  const year = localDate.getFullYear()
  const month = String(localDate.getMonth() + 1).padStart(2, '0')
  const day = String(localDate.getDate()).padStart(2, '0')
  const hours = String(localDate.getHours()).padStart(2, '0')
  const minutes = String(localDate.getMinutes()).padStart(2, '0')
  const localTime = `${year}-${month}-${day}T${hours}:${minutes}`
  
  currentEvent.value = {
    id: event.id,
    title: event.title,
    description: event.description,
    time: localTime,
    status: event.status
  }
  modalVisible.value = true
}

// 获取所有日程
const fetchEvents = async () => {
  try {
    const response = await request.get('/ez-note/date/get-all')
    if (response.code === 0) {
      events.value = response.data
        .map((event: any) => ({
          id: event.id.toString(),
          title: event.title,
          description: event.description,
          time: event.time,
          start: event.time.split('T')[0],
          // 修改事件显示样式
          backgroundColor: event.status === '完成' ? '#f5f5f5' : '#e8f5e9',
          borderColor: event.status === '完成' ? '#bdbdbd' : '#81c784',
          textColor: event.status === '完成' ? '#757575' : '#2e7d32',
          status: event.status
        }))
        .sort((a, b) => {
          const timeA = new Date(a.time).getTime()
          const timeB = new Date(b.time).getTime()
          return timeA - timeB
        })
      updateSelectedEvents(selectedDate.value || new Date().toISOString().split('T')[0])
      refetchCalendarEvents()
    }
  } catch (error) {
    console.error('Error fetching events:', error)
  }
}

// 删除日程
const deleteEvent = async () => {
  if (currentEvent.value.id) {
    try {
      const response = await request.post('/ez-note/date/delete', {
        date_id: currentEvent.value.id,
      })
      if (response.code === 0) {
        modalVisible.value = false
        await fetchEvents()
      }
    } catch (error) {
      console.error('Error deleting event:', error)
    }
  }
}

// 更新选中日期的日程
const updateSelectedEvents = (date: string) => {
  selectedDate.value = date
  // 过滤出选中日期的事件并按时间排序
  selectedEvents.value = events.value
    .filter((event) => event.start === date)
    .sort((a, b) => {
      const timeA = new Date(a.time).getTime()
      const timeB = new Date(b.time).getTime()
      return timeA - timeB // 升序排列，从早到晚
      // 如果想要降序（从晚到早），可以改为 return timeB - timeA
    })
}

// 刷新日历事件
const refetchCalendarEvents = () => {
  if (calendar.value) {
    calendar.value.removeAllEvents()
    calendar.value.addEventSource(events.value)
    calendar.value.render()
  }
}

// 初始化日历
const initializeCalendar = async () => {
  await fetchEvents()
  const calendarEl = document.getElementById('calendar')
  if (calendarEl) {
    calendar.value = new Calendar(calendarEl, {
      plugins: [dayGridPlugin, interactionPlugin],
      initialView: 'dayGridMonth',
      height: '100%',
      events: events.value,
      
      // 自定义按钮处理
      customButtons: {
        today: {
          text: '今天',
          click: () => {
            // 切换到今天
            calendar.value?.today()
            // 获取今天的日期，格式为 YYYY-MM-DD
            const today = new Date().toISOString().split('T')[0]
            // 更新右侧日程列表为今天的日期
            updateSelectedEvents(today)
          }
        }
      },
      
      // 修改头部工具栏配置，将按钮移到右边
      headerToolbar: {
        left: '',
        center: 'title',
        right: 'prev,today,next'
      },
      
      dateClick(info) {
        updateSelectedEvents(info.dateStr)
      },
      eventOrder: 'time',
      
      // 基础样式配置
      eventDisplay: 'block',
      eventBackgroundColor: '#e8f5e9', // 浅绿色背景
      eventBorderColor: '#81c784', // 中绿色边框
      eventTextColor: '#2e7d32', // 深绿色文字
      
      // 日期单元格样式
      dayCellDidMount: (arg) => {
        const today = new Date()
        const cellDate = arg.date
        const isCurrentMonth = cellDate.getMonth() === today.getMonth() &&
                              cellDate.getFullYear() === today.getFullYear()
        
        // 给单元格添加自定义属性，用于标识日期类型
        arg.el.setAttribute('data-date-type', 
          arg.isToday ? 'today' : 
          isCurrentMonth ? 'current' : 'other'
        )
        
        // 今天的样式
        if (arg.isToday) {
          arg.el.style.backgroundColor = '#fff8e1'
          arg.el.style.boxShadow = 'inset 0 0 0 2px #ffecb3'
        }
        
        // 当前月份的样式
        if (isCurrentMonth) {
          arg.el.style.cursor = 'pointer'
          arg.el.style.backgroundColor = arg.isToday ? '#fff8e1' : '#ffffff'
          
          // 添加自定义悬停效果
          const addHoverEffect = () => {
            if (!arg.isToday) {
              arg.el.style.backgroundColor = '#f1f8e9'
            }
            // 添加上浮和阴影效果
            arg.el.style.transform = 'translateY(-2px)'
            arg.el.style.boxShadow = arg.isToday 
              ? '0 4px 12px rgba(255, 236, 179, 0.4)'
              : '0 4px 12px rgba(0, 0, 0, 0.1)'
            arg.el.style.zIndex = '1'
          }
          
          const removeHoverEffect = () => {
            if (!arg.isToday) {
              arg.el.style.backgroundColor = '#ffffff'
            }
            // 移除上浮和阴影效果
            arg.el.style.transform = 'none'
            arg.el.style.boxShadow = arg.isToday 
              ? 'inset 0 0 0 2px #ffecb3'
              : 'none'
            arg.el.style.zIndex = 'auto'
          }
          
          // 添加事件监听器
          arg.el.addEventListener('mouseenter', addHoverEffect)
          arg.el.addEventListener('mouseleave', removeHoverEffect)
        } else {
          // 非当前月份的样式
          arg.el.style.backgroundColor = '#fafafa'
          arg.el.style.color = '#bdbdbd'
          
          // 非当前月份的悬停效果
          arg.el.addEventListener('mouseenter', () => {
            arg.el.style.backgroundColor = '#f5f5f5'
            arg.el.style.transform = 'translateY(-2px)'
            arg.el.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.05)'
            arg.el.style.zIndex = '1'
          })
          
          arg.el.addEventListener('mouseleave', () => {
            arg.el.style.backgroundColor = '#fafafa'
            arg.el.style.transform = 'none'
            arg.el.style.boxShadow = 'none'
            arg.el.style.zIndex = 'auto'
          })
        }
      },
      
      // 今天单元格样式
      dayCellClassNames: (arg) => {
        const today = new Date()
        const isPast = arg.date < today && !arg.isToday
        const isCurrentMonth = arg.date.getMonth() === today.getMonth()
        
        const classes = []
        if (isPast) classes.push('past-day')
        if (isCurrentMonth) classes.push('current-month')
        if (arg.isToday) classes.push('today')
        
        return classes
      },
      
      // 自定义事件渲染 - 修改已完成事项的颜色
      eventDidMount: (info) => {
        if (info.event.extendedProps.status === '完成') {
          // 已完成事件样式 - 使用灰色调
          info.el.style.backgroundColor = '#f5f5f5' // 浅灰色背景
          info.el.style.borderColor = '#bdbdbd' // 灰色边框
          info.el.style.color = '#757575' // 深灰色文字
        } else {
          // 未完成事件样式 - 保持绿色
          info.el.style.backgroundColor = '#e8f5e9'
          info.el.style.borderColor = '#81c784'
          info.el.style.color = '#2e7d32'
        }
        
        // 悬停效果
        info.el.addEventListener('mouseenter', () => {
          if (info.event.extendedProps.status === '完成') {
            info.el.style.backgroundColor = '#eeeeee' // 悬停时的灰色
          } else {
            info.el.style.backgroundColor = '#c8e6c9' // 悬停时的绿色
          }
          info.el.style.transform = 'translateY(-1px)'
          info.el.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)'
        })
        
        info.el.addEventListener('mouseleave', () => {
          if (info.event.extendedProps.status === '完成') {
            info.el.style.backgroundColor = '#f5f5f5' // 恢复浅灰色
          } else {
            info.el.style.backgroundColor = '#e8f5e9' // 恢复绿色
          }
          info.el.style.transform = 'none'
          info.el.style.boxShadow = 'none'
        })
      },
      
      // 其他配置
      buttonText: {
        today: '今天',
        month: '月',
        week: '周',
        day: '日'
      },
      locale: 'zh-cn',
      firstDay: 1,
      selectable: true,
      eventTimeFormat: {
        hour: '2-digit',
        minute: '2-digit',
        meridiem: false,
        hour12: false
      }
    })
    
    // 设置默认选中今天的日期
    const today = new Date().toISOString().split('T')[0]
    updateSelectedEvents(today)
    
    // 添加月份切换事件监听
    calendar.value.on('datesSet', (arg) => {
      // 获取当前显示的月份
      const currentDate = arg.view.currentStart
      // 获取今天的日期
      const today = new Date()
      
      // 如果当前显示的月份是本月，更新选中日期为今天
      if (currentDate.getMonth() === today.getMonth() && 
          currentDate.getFullYear() === today.getFullYear()) {
        const todayStr = today.toISOString().split('T')[0]
        updateSelectedEvents(todayStr)
      }
    })
    
    // 渲染日历
    calendar.value.render()
  }
}

// 添加一个控制错误显示的响应式变量
const showErrors = ref(false)

// 表单提交处理
const handleFormSubmit = async () => {
  // 设置显示错误标志
  showErrors.value = true

  // 验证表单
  if (!currentEvent.value.title.trim() || !currentEvent.value.description.trim()) {
    return // 如果验证失败，直接返回
  }

  try {
    if (!currentEvent.value.time) {
      currentEvent.value.time = new Date().toISOString()
    } else {
      // 创建日期对象并调整时区
      const date = new Date(currentEvent.value.time)
      // 补偿时区差
      const timezoneOffset = date.getTimezoneOffset() * 60000
      currentEvent.value.time = new Date(date.getTime() - timezoneOffset).toISOString()
    }
    
    if (currentEvent.value.id) {
      const response = await request.post('/ez-note/date/modify', {
        date_id: Number(currentEvent.value.id),
        title: currentEvent.value.title.trim(),
        description: currentEvent.value.description.trim(),
        time: currentEvent.value.time,
        status: currentEvent.value.status
      })
      if (response.code === 0) {
        modalVisible.value = false
        await fetchEvents()
      }
    } else {
      const response = await request.post('/ez-note/date/create', {
        title: currentEvent.value.title.trim(),
        description: currentEvent.value.description.trim(),
        time: currentEvent.value.time,
        status: '未完成'
      })
      if (response.code === 0) {
        modalVisible.value = false
        await fetchEvents()
      }
    }
  } catch (error) {
    console.error('Error saving event:', error)
  }
}

// 添加取消处理函数
const handleCancel = () => {
  showErrors.value = false // 重置错误显示状态
  modalVisible.value = false // 关闭模态框
}

// 切换日程状态
const toggleStatus = async (event: any) => {
  try {
    const newStatus = event.status === '完成' ? '未完成' : '完成'
    const response = await request.post('/ez-note/date/status', {
      date_id: Number(event.id),
      status: newStatus,
    })
    if (response.code === 0) {
      // 直接更新当前事件的状态
      event.status = newStatus
      
      // 更新日历中对应事件的显示
      if (calendar.value) {
        const calendarEvent = calendar.value.getEventById(event.id)
        if (calendarEvent) {
          if (newStatus === '完成') {
            calendarEvent.setProp('backgroundColor', '#f5f5f5') // 浅灰色背景
            calendarEvent.setProp('borderColor', '#bdbdbd') // 灰色边框
            calendarEvent.setProp('textColor', '#757575') // 深灰色文字
          } else {
            calendarEvent.setProp('backgroundColor', '#e8f5e9') // 浅绿色背景
            calendarEvent.setProp('borderColor', '#81c784') // 中绿色边框
            calendarEvent.setProp('textColor', '#2e7d32') // 深绿色文字
          }
          
          // 更新事件的扩展属性
          calendarEvent.setExtendedProp('status', newStatus)
        }
      }
      
      // 更新选中日期的事件列表
      const eventIndex = selectedEvents.value.findIndex(e => e.id === event.id)
      if (eventIndex !== -1) {
        selectedEvents.value[eventIndex] = {
          ...selectedEvents.value[eventIndex],
          status: newStatus
        }
      }
    }
  } catch (error) {
    console.error('Error updating status:', error)
  }
}


// 打开创建日程弹窗
const openCreateEventModal = () => {
  showErrors.value = false // 重置错误显示状态
  const now = new Date()
  // 补偿时区差，获取本地时间
  const timezoneOffset = now.getTimezoneOffset() * 60000
  const localTime = new Date(now.getTime() - timezoneOffset).toISOString().slice(0, 16)

  currentEvent.value = {
    id: null,
    title: '',
    description: '',
    time: localTime,
    status: '未完成'
  }
  modalVisible.value = true
}

// 生命周期钩子
onMounted(() => {
  initializeCalendar()
})
</script>


<style scoped>
/* 容器样式 */
.schedule-container {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  height: 88vh;
  box-sizing: border-box;
  overflow: hidden;
  background-color: #f5f9f5; /* 整体背景添加淡绿色 */
}

/* 日历部分样式 */
.calendar-left {
  width: 60%;
  height: 100%;
  overflow: auto;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 15px;
}

/* 日程部分样式 */
.schedule-right {
  width: 35%;
  padding: 20px;
  border: 2px solid #81c784;
  border-radius: 12px;
  background-color: #ffffff;
  height: 95%;
  overflow-y: auto;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

/* 头部样式 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e8f5e9;
}

.header h3 {
  color: #2e7d32;
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

/* 添加按钮样式 */
.add-btn {
  width: 40px;
  height: 40px;
  font-size: 24px;
  background: linear-gradient(135deg, #66bb6a, #43a047);
  color: white;
  border: none;
  border-radius: 50%;
  box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-btn:hover {
  transform: scale(1.1);
  background: linear-gradient(135deg, #43a047, #2e7d32);
  box-shadow: 0 6px 12px rgba(76, 175, 80, 0.4);
}

.add-btn:active {
  transform: scale(0.95);
  box-shadow: 0 2px 6px rgba(76, 175, 80, 0.3);
}

/* 无日程状态样式 */
.no-events {
  text-align: center;
  padding: 40px 20px;
}

.no-events img {
  width: 60%;
  margin-bottom: 20px;
  opacity: 0.8;
}

.no-events p {
  color: #81c784;
  font-size: 1.1rem;
  margin: 0;
}

/* 事件项样式 */
.event-item {
  margin-bottom: 15px;
  border-radius: 12px;
  background-color: #e8f5e9; /* 未完成状态的背景色 */
  border-left: 4px solid #81c784;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

/* 完成状态样式 */
.event-item.complete {
  background-color: #f5f5f5; /* 使用脚本中定义的已完成状态灰色 */
  border-left: 4px solid #bdbdbd; /* 使用脚本中定义的边框灰色 */
}

/* 未完成状态样式 */
.event-item.pending {
  background-color: #e8f5e9;
  border-left: 4px solid #81c784;
}

/* 悬停效果 */
.event-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

/* 完成状态悬停效果 */
.event-item.complete:hover {
  background-color: #eeeeee; /* 匹配脚本中的悬停灰色 */
}

/* 未完成状态悬停效果 */
.event-item.pending:hover {
  background-color: #c8e6c9; /* 匹配脚本中的悬停绿色 */
}

.event-box {
  display: flex;
  padding: 15px;
}

/* 状态指示器样式 */
.status-indicator {
  width: 24px;
  height: 24px;
  border: 2px solid #a1d99b;
  border-radius: 50%;
  margin-right: 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  background-color: #ffffff;
}

.complete .status-indicator {
  background-color: #4caf50;
  border-color: #4caf50;
}

.status-icon {
  color: white;
  font-size: 14px;
  font-weight: bold;
}

/* 内容区域样式 */
.event-content {
  flex: 1;
}

.event-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.event-title {
  font-size: 16px;
  font-weight: 600;
  color: #2e7d32;
}

.complete .event-title {
  color: #558b2f;
  text-decoration: line-through;
}

.event-actions {
  display: flex;
  gap: 8px;
}

.edit-btn {
  background: none;
  border: none;
  color: #2e7d32;
  padding: 6px 12px;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
}

.edit-btn:hover {
  background-color: #c8e6c9;
  color: #1b5e20;
}

.event-description {
  font-size: 14px;
  color: #4caf50;
  margin-bottom: 8px;
  line-height: 1.4;
}

.event-time {
  font-size: 12px;
  color: #66bb6a;
}

.complete .event-description,
.complete .event-time {
  color: #81c784;
}

/* 模态框表单样式 */
.modal-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 16px;
  font-weight: 600;
  color: #2e7d32;
}

.modal-form input,
.modal-form textarea {
  padding: 12px;
  font-size: 14px;
  border: 1px solid #c8e6c9;
  border-radius: 8px;
  background-color: #f9fff9;
  transition: all 0.3s ease;
}

.modal-form input:focus,
.modal-form textarea:focus {
  border-color: #66bb6a;
  box-shadow: 0 0 6px rgba(102, 187, 106, 0.3);
  outline: none;
  background-color: #ffffff;
}

.modal-form textarea {
  resize: vertical;
  min-height: 100px;
}

/* 按钮组样式 */
.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.action-left {
  flex: 1;
}

.action-right {
  display: flex;
  gap: 10px;
}

.delete-btn {
  background-color: #ef5350;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.delete-btn:hover {
  background-color: #e53935;
  transform: translateY(-1px);
}

.save-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-btn:hover {
  background-color: #43a047;
  transform: translateY(-1px);
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #2e7d32;
  border: 1px solid #c8e6c9;
  padding: 10px 20px;
  font-size: 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background-color: #e8f5e9;
  transform: translateY(-1px);
}

/* 错误信息样式 */
.error-message {
  color: #f44336;
  font-size: 12px;
  margin-top: 4px;
}

/* 滚动条样式 */
.schedule-right::-webkit-scrollbar {
  width: 6px;
}

.schedule-right::-webkit-scrollbar-track {
  background: #f1f8e9;
  border-radius: 3px;
}

.schedule-right::-webkit-scrollbar-thumb {
  background: #a5d6a7;
  border-radius: 3px;
}

.schedule-right::-webkit-scrollbar-thumb:hover {
  background: #81c784;
}

/* 日历相关样式 */
.schedule-container :deep(.fc) {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  position: relative;
}

.schedule-container :deep(.fc-day-today) {
  background-color: #fff8e1 !important;
  box-shadow: inset 0 0 0 2px #ffecb3 !important;
}

.schedule-container :deep(.fc-button-primary) {
  background-color: #66bb6a !important;
  border-color: #66bb6a !important;
  border-radius: 6px !important;
  padding: 8px 16px !important;
  transition: all 0.3s ease !important;
}

.schedule-container :deep(.fc-button-primary:hover) {
  background-color: #4caf50 !important;
  border-color: #4caf50 !important;
  box-shadow: 0 2px 6px rgba(76, 175, 80, 0.3) !important;
}

.schedule-container :deep(.fc-button-active) {
  background-color: #43a047 !important;
  border-color: #43a047 !important;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
}

.schedule-container :deep(.fc-event) {
  cursor: pointer;
  border-radius: 6px;
  padding: 4px 8px;
  margin: 2px 0;
  transition: all 0.3s ease;
}

.schedule-container :deep(.fc-day-past) {
  background-color: #fafafa;
}

.schedule-container :deep(.fc-day-header) {
  background-color: #e8f5e9;
  padding: 10px 0 !important;
  font-weight: 600;
  color: #2e7d32;
}

.schedule-container :deep(.fc-toolbar-title) {
  color: #2e7d32;
  font-weight: bold;
  font-size: 1.5rem !important;
}

.schedule-container :deep(.fc-day) {
  transition: background-color 0.3s ease;
}

.schedule-container :deep(.fc-day:hover) {
  background-color: #f1f8e9;
}

.schedule-container :deep(.fc-daygrid-day-number) {
  color: #2e7d32;
  font-weight: 500;
  padding: 8px !important;
}

.schedule-container :deep(.fc-day-today .fc-daygrid-day-number) {
  color: #f57c00;
  font-weight: 600;
}

/* 当前月份的日期样式 */
.schedule-container :deep(.current-month) {
  cursor: pointer !important;
}

.schedule-container :deep(.current-month:not(.fc-day-today):hover) {
  background-color: #f1f8e9 !important;
}

/* 过去日期的样式 */
.schedule-container :deep(.past-day:not(.current-month)) {
  background-color: #fafafa !important;
  color: #bdbdbd !important;
}

/* 非当前月份的日期样式 */
.schedule-container :deep(.fc-day-other) {
  background-color: #fafafa !important;
  color: #bdbdbd !important;
}

/* 周头部样式 */
.schedule-container :deep(.fc-col-header-cell) {
  background-color: #e8f5e9;
  padding: 10px 0 !important;
}

.schedule-container :deep(.fc-col-header-cell-cushion) {
  color: #2e7d32;
  font-weight: 600;
  padding: 8px !important;
}

/* 事件样式优化 */
.schedule-container :deep(.fc-event-main) {
  padding: 2px 4px;
}

.schedule-container :deep(.fc-event-time) {
  font-size: 0.9em;
  opacity: 0.8;
}

.schedule-container :deep(.fc-event-title) {
  font-weight: 500;
}

/* 工具栏样式 */
.schedule-container :deep(.fc-toolbar) {
  margin-bottom: 1.5em !important;
}

.schedule-container :deep(.fc-toolbar-chunk) {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 今天按钮特殊样式 */
.schedule-container :deep(.fc-today-button) {
  font-weight: 600 !important;
}

/* 日期格子样式 */
.schedule-container :deep(.fc-daygrid-day-frame) {
  padding: 4px !important;
}

/* 更多事件弹出按钮样式 */
.schedule-container :deep(.fc-daygrid-more-link) {
  color: #66bb6a !important;
  font-weight: 500;
  background-color: #e8f5e9;
  padding: 2px 4px;
  border-radius: 4px;
  margin: 2px 0;
}

.schedule-container :deep(.fc-daygrid-more-link:hover) {
  background-color: #c8e6c9;
  text-decoration: none !important;
}

/* 周末日期样式 */
.schedule-container :deep(.fc-day-sat),
.schedule-container :deep(.fc-day-sun) {
  background-color: #fafafa;
}

/* 当前时间线样式 */
.schedule-container :deep(.fc-timegrid-now-indicator-line) {
  border-color: #f57c00 !important;
}

.schedule-container :deep(.fc-timegrid-now-indicator-arrow) {
  border-color: #f57c00 !important;
}

/* 列表视图样式 */
.schedule-container :deep(.fc-list-day-cushion) {
  background-color: #e8f5e9 !important;
}

.schedule-container :deep(.fc-list-event:hover td) {
  background-color: #f1f8e9 !important;
}

/* 空状态样式 */
.schedule-container :deep(.fc-daygrid-day-events:empty) {
  min-height: 2em;
}

/* 日期数字容器样式 */
.schedule-container :deep(.fc-daygrid-day-top) {
  justify-content: center;
  padding-top: 4px;
}

/* 日期悬浮效果 */
.schedule-container :deep(.fc-daygrid-day) {
  transition: all 0.3s ease !important;
}

.schedule-container :deep(.fc-daygrid-day:hover) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 1;
}

/* 当前月份日期的悬浮效果 */
.schedule-container :deep(.current-month:not(.fc-day-today):hover) {
  background-color: #f1f8e9 !important;
}

/* 今天日期的悬浮效果 */
.schedule-container :deep(.fc-day-today:hover) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 236, 179, 0.4) !important;
}

/* 非当前月份日期的悬浮效果 */
.schedule-container :deep(.fc-day-other:hover) {
  background-color: #f5f5f5 !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}


</style>
