let tasks = [
  { id: "1", content: "Задача 1" },
  { id: "2", content: "Задача 2" },
  { id: "3", content: "Задача 3" },
  { id: "4", content: "Задача 4" },
  { id: "5", content: "Задача 5" },
  { id: "6", content: "Задача 6" },
  { id: "7", content: "Задача 7" },
  { id: "8", content: "Задача 8" },
  { id: "9", content: "Задача 9" },
  { id: "10", content: "Задача 10" },
];

function CreateTask(i) {
  const li = document.createElement("li");
  li.classList.add("checkbox");
  const input = document.createElement("input");
  input.classList.add("checkbox__input");
  input.setAttribute("id", tasks[i].id);
  input.setAttribute("type", "checkbox");
  const label = document.createElement("label");
  label.classList.add("checkbox__label");
  label.setAttribute("for", tasks[i].id);
  label.innerText = tasks[i].content;
  const imgEditor = document.createElement("img");
  imgEditor.classList.add("checkbox__editor");
  imgEditor.src = $("urlPencil").val();
  const imgRemove = document.createElement("img");
  imgRemove.classList.add("checkbox__remove");
  imgRemove.src = $("urlClose").val();
  const imgContainer = document.createElement("div");
  imgContainer.classList.add("checkbox__container");
  const taskContainer = document.createElement("div");
  taskContainer.classList.add("checkbox__container");
  // добавление ребёнка элементу
  taskContainer.appendChild(input);
  taskContainer.appendChild(label);
  imgContainer.appendChild(imgEditor);
  imgContainer.appendChild(imgRemove);
  li.appendChild(taskContainer);
  li.appendChild(imgContainer);
  const parent = document.getElementById("todoList");
  parent.insertBefore(li, parent.children[i]);

  /* change - один из вариантов действий, на который мы вешаем слушатель (addEventListener), он слушает и на каждый change элемента
    вызывает функцию, которую мы передали слушателю*/
  document.getElementById(tasks[i].id).addEventListener("change", function () {
    const task = document.getElementById(tasks[i].id);
    if (task.checked) {
      task.parentElement.style.textDecoration = "line-through";
    } else {
      task.parentElement.style.textDecoration = "none";
    }
  });

  // Функция-обработчик события клика
  imgRemove.onclick = function () {
    tasks.splice[(i, 1)];
    li.remove();
  };

  imgEditor.onclick = function () {
    const parent = li.parentElement;
    CreateEditedTask(i, parent);
    li.remove();
  };
}

function CreateEditedTask(i, parent) {
  if (i >= tasks.length) {
    tasks.push({ id: `${i} New element`, content: "" });
  }
  const newLi = document.createElement("li");
  newLi.classList.add("checkbox");
  const textInput = document.createElement("input");
  textInput.type = "text";
  textInput.value = tasks[i].content;
  const imgCheck = document.createElement("img");
  imgCheck.classList.add("checkbox__save");
  imgCheck.src = "./images/check.svg";
  imgCheck.onclick = function () {
    tasks[i].content = textInput.value;
    newLi.remove();
    CreateTask(i);
  };
  newLi.appendChild(textInput);
  newLi.appendChild(imgCheck);
  parent.insertBefore(newLi, parent.children[i]); // в parent вставляем newLi перед (выше слой) parent.children[i]
}

for (let i = 0; i < tasks.length; i++) {
  CreateTask(i);
}

document.getElementById("removeAll").addEventListener("click", function () {
  tasks = [];
  const list = document.getElementById("todoList");
  while (list.firstChild) {
    list.removeChild(list.lastChild);
  }
});

document.getElementById("addNewTask").addEventListener("click", function () {
  const parent = document.getElementById("todoList");
  CreateEditedTask(tasks.length, parent);
  console.log(tasks.length);
});
