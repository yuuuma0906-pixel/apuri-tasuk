<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>課題管理アプリ</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f4f7fb;
      margin: 0;
    }

    header {
      background: #3f7cff;
      color: white;
      text-align: center;
      padding: 25px;
    }

    .container {
      width: 90%;
      max-width: 900px;
      margin: 30px auto;
      background: white;
      padding: 25px;
      border-radius: 12px;
    }

    h2 {
      color: #3f7cff;
    }

    input, select, button {
      padding: 10px;
      margin: 5px;
      border-radius: 6px;
      border: 1px solid #ccc;
    }

    button {
      background: #3f7cff;
      color: white;
      border: none;
      cursor: pointer;
    }

    button:hover {
      background: #245ee8;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }

    th, td {
      border: 1px solid #ccc;
      padding: 10px;
      text-align: center;
    }

    th {
      background: #3f7cff;
      color: white;
    }

    .danger {
      background: #ff4d4d;
    }

    .warning {
      color: red;
      font-weight: bold;
    }

    .safe {
      color: green;
      font-weight: bold;
    }
  </style>
</head>

<body>

  <header>
    <h1>Campus Task Manager</h1>
    <p>大学生のための課題・テスト管理アプリ</p>
  </header>

  <div class="container">
    <h2>課題を追加</h2>

    <input type="text" id="className" placeholder="授業名">
    <input type="text" id="taskName" placeholder="課題名">
    <input type="date" id="deadline">

    <select id="status">
      <option value="未提出">未提出</option>
      <option value="作成中">作成中</option>
      <option value="提出済み">提出済み</option>
    </select>

    <button onclick="addTask()">追加</button>

    <h2>課題一覧</h2>

    <table>
      <thead>
        <tr>
          <th>授業名</th>
          <th>課題名</th>
          <th>提出期限</th>
          <th>残り日数</th>
          <th>状況</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody id="taskList">
      </tbody>
    </table>
  </div>

  <script>
    let tasks = JSON.parse(localStorage.getItem("tasks")) || [];

    function addTask() {
      const className = document.getElementById("className").value;
      const taskName = document.getElementById("taskName").value;
      const deadline = document.getElementById("deadline").value;
      const status = document.getElementById("status").value;

      if (className === "" || taskName === "" || deadline === "") {
        alert("授業名・課題名・提出期限を入力してください");
        return;
      }

      const task = {
        className: className,
        taskName: taskName,
        deadline: deadline,
        status: status
      };

      tasks.push(task);
      saveTasks();
      showTasks();

      document.getElementById("className").value = "";
      document.getElementById("taskName").value = "";
      document.getElementById("deadline").value = "";
      document.getElementById("status").value = "未提出";
    }

    function showTasks() {
      tasks.sort((a, b) => new Date(a.deadline) - new Date(b.deadline));

      const taskList = document.getElementById("taskList");
      taskList.innerHTML = "";

      tasks.forEach((task, index) => {
        const today = new Date();
        const deadlineDate = new Date(task.deadline);
        const diffTime = deadlineDate - today;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        let dayText = "";
        let dayClass = "";

        if (diffDays < 0) {
          dayText = "期限切れ";
          dayClass = "warning";
        } else if (diffDays === 0) {
          dayText = "今日まで";
          dayClass = "warning";
          alert(task.taskName + " は今日が提出期限です！");
        } else if (diffDays <= 3) {
          dayText = "あと" + diffDays + "日";
          dayClass = "warning";
        } else {
          dayText = "あと" + diffDays + "日";
          dayClass = "safe";
        }

        taskList.innerHTML += `
          <tr>
            <td>${task.className}</td>
            <td>${task.taskName}</td>
            <td>${task.deadline}</td>
            <td class="${dayClass}">${dayText}</td>
            <td>
              <select onchange="changeStatus(${index}, this.value)">
                <option value="未提出" ${task.status === "未提出" ? "selected" : ""}>未提出</option>
                <option value="作成中" ${task.status === "作成中" ? "selected" : ""}>作成中</option>
                <option value="提出済み" ${task.status === "提出済み" ? "selected" : ""}>提出済み</option>
              </select>
            </td>
            <td>
              <button class="danger" onclick="deleteTask(${index})">削除</button>
            </td>
          </tr>
        `;
      });
    }

    function changeStatus(index, newStatus) {
      tasks[index].status = newStatus;
      saveTasks();
      showTasks();
    }

    function deleteTask(index) {
      tasks.splice(index, 1);
      saveTasks();
      showTasks();
    }

    function saveTasks() {
      localStorage.setItem("tasks", JSON.stringify(tasks));
    }

    showTasks();
  </script>

</body>
</html>