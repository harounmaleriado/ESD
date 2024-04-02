new Vue({
    el: '#app',
    data: {
        posts: [],
        newPost: {
            title: '',
            content: ''
        },
        commentTitle: '',
        commentContent: ''
    },
    mounted() {
        this.loadPosts();
    },
    methods: {
        loadPosts() {
            axios.get('http://localhost:8000/posts')
                .then(response => {
                    this.posts = response.data;
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        },
        submitPost() {
            axios.post('http://localhost:8000/posts', this.newPost)
                .then(() => {
                    this.newPost.title = '';
                    this.newPost.content = '';
                    this.loadPosts();
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        },
        submitComment(postId) {
            const commentData = {
                title: this.commentTitle,
                content: this.commentContent
            };
            axios.post(`http://localhost:8000/posts/comments/${postId}`, commentData)
                .then(() => {
                    this.commentTitle = '';
                    this.commentContent = '';
                    this.loadPosts(); // Reload posts to show the new comments
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    }
});

