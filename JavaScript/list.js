function updateProgress(containerList) {
    const checkboxes = containerList.querySelectorAll('.progress')
    const total = checkboxes.length
    const completed = [...checkboxes].filter(checkbox => checkbox.checked).length

    const percentage = total > 0 ? Math.round((completed / total) * 100) : 0

    const progressBar = containerList.querySelector('.progress-fill')
    const spanProgress = containerList.querySelector('.progress-text')
    if(progressBar) {
        progressBar.style.width = `${percentage}%`
    }

    if(spanProgress) {
        spanProgress.innerText = `${percentage}% completed`
    }
}

function createNewList(name, description) {
    const container = document.querySelector('.container')
    container.innerHTML += `       
        <div class="container-list">
            <div class="container-list-name">
                <i class="fa-solid fa-angle-right toggle-task"></i>

                <h1 class="list-name">${name}</h1>

                <i class="fa-regular fa-pen-to-square edit-list"></i>
                <i class="fa-solid fa-trash-can delete-list"></i>
                <i class="fa-solid fa-circle-info open-description"></i>

                <form class="container-edit-list hidden">
                    <input type="text" placeholder="Edit your list here">
                    <button type="submit" class="action-btn">
                    <i class="fa-solid fa-check"></i>
                    </button>
                </form>
            </div>

            <div class="modal-description hidden">
                <div class="modal-content">
                    <h1>List description</h1>
                    <div class="text-description">
                        <p>${description}</p>
                    </div>
                    <button class="close-modal">Close</button>
                </div>
            </div>

            <div class="progress-bar hidden">
                <div class="progress-fill"></div>
                <div class="progress-box">
                    <span class="progress-text">0% completed</span>
                </div>
            </div>

            <div class="button-new-task hidden">
                <button class="btn-new-task">New Task</button>
            </div>

            <div class="modal-new-task hidden">
                <form class="container-new-task">
                    <h1>Create a new task</h1>
                    <div class="info-new-task">
                        <input type="text" placeholder="Write the name of your task here" class="input-name-task">
                        <div class="date-time">
                            <input type="date" class="input-date-task">
                            <input type="time" class="input-time-task">
                        </div>
                    </div>
                    <div class="button-create-task">
                        <button type="submit" class="btn-create-task">Confirm</button>
                        <button type="submit" class="btn-cancel-task">Cancel</button>
                    </div>
                </form>
            </div>

            <div class="container-tasks hidden">
            </div>
        </div>
    `
}

function createNewTask(task, date, time, containerTasks) {
    const taskElement = document.createElement('div')
    taskElement.classList.add('task')
    taskElement.innerHTML = `
        <input type="checkbox" class="progress">
        <div class="info-task">
            <label class="task-description">${task}</label>
            <div class="container-task-datetime">
                <i class="fa-solid fa-calendar-days icon-datetime"></i>
                <div class="task-datetime">
                    <span class="task-date">${date}</span> - <span class="task-time">${time}</span>
                </div>
            </div>
        </div>

        <i class="fa-regular fa-pen-to-square edit-task"></i>
        <i class="fa-regular fa-copy copy-task"></i>
        <i class="fa-solid fa-trash-can delete-task"></i>

        <form class="container-edit-task hidden">
            <input type="text" placeholder="Edit your task here" class="edit-name-task">
            <button type="submit" class="action-btn">
            <i class="fa-solid fa-check"></i>
            </button>
        </form>
    `
    containerTasks.appendChild(taskElement)

    updateProgress(containerTasks.closest('.container-list'))
}

let itemToDelete = null

document.addEventListener('DOMContentLoaded', () => {
    const inputName = document.querySelector('.input-name')
    const inputDesc = document.querySelector('.input-desc')
    const btnNewList = document.querySelector('.btn-new-list')
    const container = document.querySelector('.container')
    
    btnNewList.addEventListener('click', (event) => {
        event.preventDefault()

        const name = inputName.value.trim()
        const description = inputDesc.value.trim()

        if (name && description) {
            createNewList(name, description)
            inputName.value = ''
            inputDesc.value = ''
        } else {
            alert('Please fill in the listing name and description!')
        }
    })
     
    container.addEventListener('click', (event) => {
        const target = event.target
        
        if (target.closest('.toggle-task')) {
            const button = target.closest('.toggle-task')
            const containerList = button.closest('.container-list')
            const progressBar = containerList.querySelector('.progress-bar')
            const newTask = containerList.querySelector('.button-new-task')
            const containerTasks = containerList.querySelector('.container-tasks')
            
            progressBar.classList.toggle('hidden')
            newTask.classList.toggle('hidden')
            containerTasks.classList.toggle('hidden')
            
            button.classList.toggle('fa-angle-right')
            button.classList.toggle('fa-angle-down')
        }

        if (target.closest('.edit-list')) {
            const button = target.closest('.edit-list')
            const containerList = button.closest('.container-list-name')
            const toggleTask = containerList.querySelector('.toggle-task')
            const listText = containerList.querySelector('.list-name')
            const deleteBtn = containerList.querySelector('.delete-list')
            const editForm = containerList.querySelector('.container-edit-list')
            const input = editForm.querySelector('input')
            
            input.value = listText.innerText
            
            toggleTask.classList.add('hidden')
            listText.classList.add('hidden')
            button.classList.add('hidden')
            deleteBtn.classList.add('hidden')
            editForm.classList.remove('hidden')
        }

        if (target.closest('.open-description')) {
            const button = target.closest('.open-description')
            const containerList = button.closest('.container-list')
            const modal = containerList.querySelector('.modal-description')
            modal.classList.remove('hidden')
        }
        
        if (target.closest('.close-modal')) {
            const button = target.closest('.close-modal')
            const modal = button.closest('.modal-description')
            modal.classList.add('hidden')
        }
        
        if (target.closest('.btn-new-task')) {
            const button = target.closest('.btn-new-task')
            const containerList = button.closest('.container-list')
            const modal = containerList.querySelector('.modal-new-task')
            modal.classList.remove('hidden')
        }

        if (target.closest('.btn-cancel-task')) {
            const button = target.closest('.btn-cancel-task')
            const modal = button.closest('.modal-new-task')
            const inputName = modal.querySelector('.input-name-task')
            const inputDate  = modal.querySelector('.input-date-task')
            const inputTime  = modal.querySelector('.input-time-task')

            inputName.value = ''
            inputDate.value = ''
            inputTime.value = ''

            modal.classList.add('hidden')
        }

        if (target.classList.contains('progress')) {
            const containerList = target.closest('.container-list')
            updateProgress(containerList)

            const task = target.closest('.task')
            const taskLabel = task.querySelector('.task-description')
            const taskDatetime = task.querySelector('.container-task-datetime')

            if (target.checked) {
                taskLabel.classList.add('done')
                taskDatetime.classList.add('done')
            } else {
                taskLabel.classList.remove('done')
                taskDatetime.classList.remove('done')
            }
        }

        if (target.closest('.edit-task')) {
            const button = target.closest('.edit-task')
            const task = button.closest('.task')
            const checkbox = task.querySelector('.progress')
            const taskText = task.querySelector('.task-description')
            const copyBtn = task.querySelector('.copy-task')
            const deleteBtn = task.querySelector('.delete-task')
            const infoTask = task.querySelector('.info-task')
            const editForm = task.querySelector('.container-edit-task')
            const input = editForm.querySelector('.edit-name-task')
            
            input.value = taskText.innerText
            
            checkbox.classList.add('hidden')
            infoTask.classList.add('hidden')
            button.classList.add('hidden')
            copyBtn.classList.add('hidden')
            deleteBtn.classList.add('hidden')
            editForm.classList.remove('hidden')
        }

        if (target.closest('.copy-task')) {
            const button = target.closest('.copy-task')
            const task = button.closest('.task')
            const containerTasks = task.closest('.container-tasks')
            const nameTask = task.querySelector('.task-description').innerText
            const dateTask = task.querySelector('.task-date').innerText
            const timeTask = task.querySelector('.task-time').innerText

            createNewTask(nameTask, dateTask, timeTask, containerTasks)
        }

        if (target.closest('.delete-list')) {
            itemToDelete = target.closest('.container-list')
            document.querySelector('.modal-delete').classList.remove('hidden')
        }

        if (target.closest('.delete-task')) {
            itemToDelete = target.closest('.task')
            document.querySelector('.modal-delete').classList.remove('hidden')
        }
    })
    
    document.querySelector('.btn-confirm-delete').addEventListener('click', () => {
        if (itemToDelete) {
            const isTask = itemToDelete.classList.contains('task')
            const containerList = isTask ? itemToDelete.closest('.container-list') : null

            itemToDelete.remove()
            itemToDelete = null

            if (isTask && containerList) {
                updateProgress(containerList)
            }
        }
        document.querySelector('.modal-delete').classList.add('hidden')
    })

    document.querySelector('.btn-cancel-delete').addEventListener('click', () => {
        itemToDelete = null
        document.querySelector('.modal-delete').classList.add('hidden')
    })

    document.addEventListener('submit', (event) => {
        if (event.target.matches('.container-edit-list')) {
            event.preventDefault()
            
            const form = event.target
            const list = form.closest('.container-list-name')
            const newValue = form.querySelector('input').value.trim()

            const toggleTask = list.querySelector('.toggle-task')
            const listText = list.querySelector('.list-name')
            const editBtn = list.querySelector('.edit-list')
            const deleteBtn = list.querySelector('.delete-list')

            if (newValue !== '') {
                listText.innerText = newValue
            }

            toggleTask.classList.remove('hidden')
            listText.classList.remove('hidden')
            editBtn.classList.remove('hidden')
            deleteBtn.classList.remove('hidden')

            form.classList.add('hidden')
        }
    })
    
    document.addEventListener('submit', (event) => {
        if (event.target.matches('.container-new-task')) {
            event.preventDefault()
            
            const form = event.target
            const containerList = form.closest('.container-list')
            const modal = containerList.querySelector('.modal-new-task')
            const inputName = form.querySelector('.input-name-task')
            const inputDate  = form.querySelector('.input-date-task')
            const inputTime  = form.querySelector('.input-time-task')

            const taskText = inputName.value.trim()
            const taskDate = inputDate.value
            const taskTime = inputTime.value
            
            if (taskText && taskDate && taskTime) {
                const taskContainer = containerList.querySelector('.container-tasks')
                createNewTask(taskText, taskDate, taskTime, taskContainer)
                inputName.value = ''
                inputDate.value = ''
                inputTime.value = ''
                updateProgress(containerList)
                modal.classList.add('hidden')
            }
        }
    })
    
    document.addEventListener('submit', (event) => {
        if (event.target.matches('.container-edit-task')) {
            event.preventDefault()
            
            const form = event.target
            const task = form.closest('.task')
            const newValue = form.querySelector('.edit-name-task').value.trim()

            const checkbox = task.querySelector('.progress')
            const taskText = task.querySelector('.task-description')
            const editBtn = task.querySelector('.edit-task')
            const copyBtn = task.querySelector('.copy-task')
            const deleteBtn = task.querySelector('.delete-task')
            const infoTask = task.querySelector('.info-task')

            if (newValue !== '') {
                taskText.innerText = newValue
            }

            checkbox.classList.remove('hidden')
            infoTask.classList.remove('hidden')
            editBtn.classList.remove('hidden')
            copyBtn.classList.remove('hidden')
            deleteBtn.classList.remove('hidden')

            form.classList.add('hidden')
        }
    })
})
