const API_BASE = "http://127.0.0.1:8000";

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
            `;
            postsList.appendChild(li);
        });
    }
}

async function deletePost(postId) {
    await fetch(`${API_BASE}/posts/${postId}`, { method: "DELETE" });
    loadPosts();
}

if (document.querySelector("#users-list")) loadUsers();
if (document.querySelector("#posts-list")) loadPosts();
