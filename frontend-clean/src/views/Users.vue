<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsers, createUser, updateUser } from '@/api/admin'

const users = ref([])
const loading = ref(false)

const dialogVisible = ref(false)
const dialogTitle = ref('新增员工')
const userForm = ref({
  id: null,
  username: '',
  password: '',
  real_name: '',
  role_id: 2   // 1=admin 2=waiter
})
const formRef = ref(null)

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, message: '至少2位', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 4, message: '至少4位', trigger: 'blur' }
  ],
  real_name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  role_id: [{ required: true, message: '请选择角色', trigger: 'change' }]
}

const roleMap = { admin: '管理员', waiter: '服务员' }
const roleOptions = [
  { label: '管理员', value: 1 },
  { label: '服务员', value: 2 }
]

const fetchUsers = async () => {
  loading.value = true
  try {
    users.value = await getUsers()
  } catch {
    // 已处理
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  dialogTitle.value = '新增员工'
  userForm.value = { id: null, username: '', password: '', real_name: '', role_id: 2 }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑员工'
  userForm.value = {
    id: row.id,
    username: row.username,
    password: '',
    real_name: row.real_name,
    role_id: row.role_id
  }
  dialogVisible.value = true
}

const handleSave = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    try {
      if (userForm.value.id) {
        const payload = { real_name: userForm.value.real_name }
        if (userForm.value.password) payload.password = userForm.value.password
        await updateUser(userForm.value.id, payload)
        ElMessage.success('已更新')
      } else {
        await createUser(userForm.value)
        ElMessage.success('已创建')
      }
      dialogVisible.value = false
      fetchUsers()
    } catch {
      // 已处理
    }
  })
}

const handleToggleStatus = async (row) => {
  ElMessage.info('当前后端暂不支持状态切换，请直接修改密码来禁用')
}

onMounted(fetchUsers)
</script>

<template>
  <div class="users-page">
    <!-- 页面标题 - 鎏金效果 -->
    <h1 class="page-title">员工管理</h1>

    <!-- 操作栏 - 鎏金按钮 -->
    <div class="action-bar">
      <el-button type="primary" @click="handleAdd" class="add-btn">
        新增员工
      </el-button>
    </div>

    <!-- 员工表格 - 鎏金高级风格 -->
    <div class="table-container">
      <el-table :data="users" v-loading="loading" class="users-table">
        <el-table-column prop="id" label="编号" width="80" align="center">
          <template #default="{ row }">
            <span class="table-id">{{ row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" width="140" align="center">
          <template #default="{ row }">
            <span class="table-text">{{ row.username }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="real_name" label="姓名" width="140" align="center">
          <template #default="{ row }">
            <span class="table-name">{{ row.real_name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="role" label="角色" width="120" align="center">
          <template #default="{ row }">
            <div class="role-tag" :class="row.role">
              {{ roleMap[row.role] || row.role }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120" align="center">
          <template #default="{ row }">
            <div class="status-tag" :class="row.status === 1 ? 'active' : 'disabled'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button size="small" @click="handleEdit(row)" class="edit-btn">
                编辑
              </el-button>
              <el-button size="small" @click="handleToggleStatus(row)" class="toggle-btn">
                {{ row.status === 1 ? '禁用' : '启用' }}
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 空状态提示 -->
      <div v-if="!loading && users.length === 0" class="empty-state">
        暂无员工数据
      </div>
    </div>

    <!-- 编辑弹窗 - 鎏金高级风格 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="480px" class="user-dialog">
      <el-form ref="formRef" :model="userForm" :rules="rules" label-width="100px" class="user-form">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" :disabled="!!userForm.id" placeholder="请输入用户名" class="form-input" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="userForm.password" type="password" show-password placeholder="请输入密码" class="form-input" />
          <span v-if="userForm.id" class="form-hint">不修改请留空</span>
        </el-form-item>
        <el-form-item label="姓名" prop="real_name">
          <el-input v-model="userForm.real_name" placeholder="请输入姓名" class="form-input" />
        </el-form-item>
        <el-form-item label="角色" prop="role_id">
          <el-select v-model="userForm.role_id" placeholder="请选择角色" class="form-select">
            <el-option v-for="o in roleOptions" :key="o.value" :label="o.label" :value="o.value" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false" class="cancel-btn">取消</el-button>
          <el-button type="primary" @click="handleSave" class="save-btn">保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped lang="scss">
.users-page {
  // 页面标题 - 鎏金效果
  .page-title {
    font-size: 28px;
    font-weight: 700;
    color: #E6B87D;
    margin-bottom: 32px;
    letter-spacing: 3px;
    text-shadow: 0 0 20px rgba(230, 184, 125, 0.4);
    position: relative;

    // 标题下方暖色装饰线
    &::after {
      content: '';
      position: absolute;
      bottom: -8px;
      left: 0;
      width: 120px;
      height: 3px;
      background: linear-gradient(to right, #D94836, #E6B87D);
      border-radius: 2px;
    }
  }
}

// 操作栏 - 鎏金按钮
.action-bar {
  margin-bottom: 24px;

  .add-btn {
    background: linear-gradient(135deg, #D94836, #F27044);
    border: none;
    border-radius: 9999px;
    font-weight: 600;
    letter-spacing: 2px;
    font-size: 14px;
    box-shadow: 0 4px 16px rgba(217, 72, 54, 0.25);
    transition: all 300ms ease;

    &:hover {
      box-shadow: 0 6px 24px rgba(217, 72, 54, 0.35);
      transform: translateY(-2px);
    }
  }
}

// 表格容器 - 鎏金高级风格
.table-container {
  background: rgba(26, 21, 18, 0.4);
  border: 1px solid rgba(230, 184, 125, 0.15);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 16px rgba(15, 12, 10, 0.2);
  position: relative;

  // 顶部鎏金装饰线
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 20px;
    right: 20px;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(230, 184, 125, 0.3), transparent);
  }
}

// 表格样式 - 鎏金高级风格
.users-table {
  background: transparent;
  border-radius: 12px;

  :deep(.el-table__header-wrapper) {
    th {
      background: rgba(26, 21, 18, 0.3);
      border-color: rgba(230, 184, 125, 0.15);

      .cell {
        font-size: 15px;
        font-weight: 600;
        color: #E6B87D;
        letter-spacing: 2px;
        text-shadow: 0 0 8px rgba(230, 184, 125, 0.2);
      }
    }
  }

  :deep(.el-table__body-wrapper) {
    tr {
      background: rgba(26, 21, 18, 0.15);
      border-color: rgba(230, 184, 125, 0.1);

      &:hover > td {
        background: rgba(242, 112, 68, 0.08);
      }

      td {
        border-color: rgba(230, 184, 125, 0.1);
      }
    }
  }
}

// 表格内文字样式 - 鎏金高级感
.table-id {
  font-size: 14px;
  font-weight: 600;
  font-family: 'SF Mono', 'Consolas', monospace;
  color: #E6B87D;
  text-shadow: 0 0 6px rgba(230, 184, 125, 0.2);
}

.table-text {
  font-size: 14px;
  font-weight: 500;
  color: #F8F5F2;
  letter-spacing: 1px;
}

.table-name {
  font-size: 15px;
  font-weight: 600;
  color: #E6B87D;
  text-shadow: 0 0 8px rgba(230, 184, 125, 0.3);
  letter-spacing: 2px;
}

// 角色标签 - 鎏金风格
.role-tag {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1px;
  display: inline-flex;
  align-items: center;
  justify-content: center;

  &.admin {
    background: rgba(217, 72, 54, 0.15);
    border: 1px solid rgba(217, 72, 54, 0.3);
    color: #D94836;
    text-shadow: 0 0 6px rgba(217, 72, 54, 0.3);
  }

  &.waiter {
    background: rgba(230, 184, 125, 0.1);
    border: 1px solid rgba(230, 184, 125, 0.2);
    color: #E6B87D;
    text-shadow: 0 0 6px rgba(230, 184, 125, 0.2);
  }
}

// 状态标签 - 鎏金风格
.status-tag {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1px;
  display: inline-flex;
  align-items: center;
  justify-content: center;

  &.active {
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.3);
    color: #22C55E;
    text-shadow: 0 0 6px rgba(34, 197, 94, 0.3);
  }

  &.disabled {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #EF4444;
    text-shadow: 0 0 6px rgba(239, 68, 68, 0.3);
  }
}

// 操作按钮 - 鎏金风格
.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;

  .edit-btn {
    background: rgba(230, 184, 125, 0.08);
    border: 1px solid rgba(230, 184, 125, 0.15);
    color: #E6B87D;
    font-weight: 500;
    letter-spacing: 1px;
    border-radius: 6px;
    transition: all 250ms ease;

    &:hover {
      background: rgba(230, 184, 125, 0.15);
      border-color: rgba(230, 184, 125, 0.25);
      color: #F8F5F2;
      transform: translateY(-1px);
    }
  }

  .toggle-btn {
    background: rgba(217, 72, 54, 0.08);
    border: 1px solid rgba(217, 72, 54, 0.15);
    color: #D94836;
    font-weight: 500;
    letter-spacing: 1px;
    border-radius: 6px;
    transition: all 250ms ease;

    &:hover {
      background: rgba(217, 72, 54, 0.15);
      border-color: rgba(217, 72, 54, 0.25);
      color: #F8F5F2;
      transform: translateY(-1px);
    }
  }
}

// 空状态提示
.empty-state {
  text-align: center;
  padding: 48px 24px;
  color: #BFAFA6;
  font-size: 15px;
  letter-spacing: 2px;
  font-weight: 500;
}

// 弹窗样式 - 鎏金高级风格
.user-dialog {
  :deep(.el-dialog) {
    background: rgba(26, 21, 18, 0.95);
    border: 1px solid rgba(230, 184, 125, 0.2);
    border-radius: 16px;
    box-shadow: 0 16px 48px rgba(15, 12, 10, 0.4);

    .el-dialog__header {
      background: linear-gradient(135deg, rgba(217, 72, 54, 0.1), rgba(230, 184, 125, 0.06));
      border-bottom: 1px solid rgba(230, 184, 125, 0.15);
      padding: 20px 24px;

      .el-dialog__title {
        font-size: 18px;
        font-weight: 700;
        color: #E6B87D;
        letter-spacing: 3px;
        text-shadow: 0 0 12px rgba(230, 184, 125, 0.3);
      }
    }

    .el-dialog__body {
      padding: 24px;
    }
  }
}

// 表单样式 - 鎏金风格
.user-form {
  :deep(.el-form-item__label) {
    font-size: 14px;
    font-weight: 600;
    color: #E6B87D;
    letter-spacing: 2px;
    text-shadow: 0 0 6px rgba(230, 184, 125, 0.2);
  }

  :deep(.el-input__wrapper) {
    background: rgba(26, 21, 18, 0.4);
    border: 1px solid rgba(230, 184, 125, 0.15);
    border-radius: 8px;
    box-shadow: none;

    &:hover {
      border-color: rgba(230, 184, 125, 0.25);
    }

    &.is-focus {
      border-color: rgba(217, 72, 54, 0.3);
      box-shadow: 0 0 12px rgba(217, 72, 54, 0.15);
    }

    .el-input__inner {
      color: #F8F5F2;
      font-size: 14px;
      letter-spacing: 1px;

      &::placeholder {
        color: #6B5B52;
      }
    }
  }

  :deep(.el-select) {
    .el-input__wrapper {
      background: rgba(26, 21, 18, 0.4);
      border: 1px solid rgba(230, 184, 125, 0.15);
    }
  }

  .form-hint {
    font-size: 12px;
    color: #6B5B52;
    letter-spacing: 1px;
    margin-top: 4px;
    display: block;
  }
}

// 弹窗底部按钮 - 鎏金风格
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;

  .cancel-btn {
    background: rgba(26, 21, 18, 0.4);
    border: 1px solid rgba(230, 184, 125, 0.15);
    color: #BFAFA6;
    font-weight: 500;
    letter-spacing: 1px;
    border-radius: 8px;
    transition: all 250ms ease;

    &:hover {
      background: rgba(26, 21, 18, 0.6);
      border-color: rgba(230, 184, 125, 0.25);
      color: #F8F5F2;
    }
  }

  .save-btn {
    background: linear-gradient(135deg, #D94836, #F27044);
    border: none;
    font-weight: 600;
    letter-spacing: 2px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(217, 72, 54, 0.2);
    transition: all 250ms ease;

    &:hover {
      box-shadow: 0 6px 16px rgba(217, 72, 54, 0.3);
      transform: translateY(-1px);
    }
  }
}
</style>