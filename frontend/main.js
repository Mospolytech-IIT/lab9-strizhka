const API_BASE = "http://127.0.0.1:8000";

let currentUserId = null;

document.querySelector("#create-user-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.querySelector("#username").value;
    const email = document.querySelector("#email").value;
    const password = document.querySelector("#password").value;

    await fetch(`${API_BASE}/users/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
    });
    loadUsers();
});

async function loadUsers() {
    const response = await fetch(`${API_BASE}/users/`);
    const users = await response.json();
    const usersList = document.querySelector("#users-list");
    if (usersList) {
        usersList.innerHTML = "";
        users.forEach((user) => {
            const li = document.createElement("li");
            li.innerHTML = `
                ${user.username} (${user.email})
                <button onclick="deleteUser(${user.id})">Удалить</button>
                <button onclick='openUserEdit(${JSON.stringify(user)})'>Редактировать</button>
            `;
            usersList.appendChild(li);
        });
    }
}

async function deleteUser(userId) {
    await fetch(`${API_BASE}/users/${userId}`, { method: "DELETE" });
    loadUsers();
}

document.querySelector("#create-post-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = document.querySelector("#title").value;
    const content = document.querySelector("#content").value;
    const userId = document.querySelector("#user-id").value;

    await fetch(`${API_BASE}/posts/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, content, user_id: userId }),
    });
    loadPosts();
});

async function loadPosts() {
    const response = await fetch(`${API_BASE}/posts/`);
    const posts = await response.json();
    const postsList = document.querySelector("#posts-list");
    if (postsList) {
        postsList.innerHTML = "";
        posts.forEach((post) => {
            const li = document.createElement("li");
            li.innerHTML = `
                ${post.title} (${post.content})
                <button onclick="deletePost(${post.id})">Удалить</button>
                <button onclick='openPostEdit(${JSON.stringify(post)})'>Редактировать</button>
            `;
            postsList.appendChild(li);
        });
    }
}

async function deletePost(postId) {
    await fetch(`${API_BASE}/posts/${postId}`, { method: "DELETE" });
    loadPosts();
}

function openUserEdit(user) {
    currentUserId = user.id;
    document.querySelector("#edit-username").value = user.username;
    document.querySelector("#edit-email").value = user.email;
    document.querySelector("#edit-password").value = "";
    document.querySelector("#edit-user-modal").style.display = "block";
}

function closeUserEdit() {
    document.querySelector("#edit-user-modal").style.display = "none";
}

async function saveUserEdit() {
    const username = document.querySelector("#edit-username").value;
    const email = document.querySelector("#edit-email").value;
    const password = document.querySelector("#edit-password").value;

    await fetch(`${API_BASE}/users/${currentUserId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
    });

    closeUserEdit();
    loadUsers();
}

let currentPostId = null;

function openPostEdit(post) {
    currentPostId = post.id;
    document.querySelector("#edit-title").value = post.title;
    document.querySelector("#edit-content").value = post.content;
    document.querySelector("#edit-post-modal").style.display = "block";
}

function closePostEdit() {
    document.querySelector("#edit-post-modal").style.display = "none";
}

async function savePostEdit() {
    const title = document.querySelector("#edit-title").value;
    const content = document.querySelector("#edit-content").value;

    await fetch(`${API_BASE}/posts/${currentPostId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, content }),
    });

    closePostEdit();
    loadPosts();
}


if (document.querySelector("#users-list")) loadUsers();
if (document.querySelector("#posts-list")) loadPosts();
