document.addEventListener('DOMContentLoaded', () => {
    const topicsList = document.getElementById('topicsList');
    const newTopicForm = document.getElementById('newTopicForm');
    const newTopicTitle = document.getElementById('newTopicTitle');
    const newTopicContent = document.getElementById('newTopicContent');

    newTopicForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const title = newTopicTitle.value.trim();
        const content = newTopicContent.value.trim();
        
        if (title && content) {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<strong>${title}</strong><p>${content}</p>`;
            topicsList.appendChild(listItem);

            newTopicTitle.value = '';
            newTopicContent.value = '';
        }
    });
});