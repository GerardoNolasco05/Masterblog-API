from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Internal data storage
POSTS_DATA = [
    {"id": 1, "title": "First", "content": "This is the first post."},
    {"id": 2, "title": "Second", "content": "This is the second post."},
    {"id": 3, "title": "Third", "content": "This is the third post."}
]

# Utility function to retrieve posts
def get_posts_data():
    """Returns the current list of posts."""
    return POSTS_DATA

def find_post_by_id(post_id):
    """Finds a post by ID."""
    return next((p for p in get_posts_data() if p["id"] == post_id), None)

def add_new_post(title, content):
    """Adds a new post and returns the created post."""
    posts = get_posts_data()
    new_id = max((post["id"] for post in posts), default=0) + 1
    new_post = {"id": new_id, "title": title, "content": content}
    posts.append(new_post)
    return new_post

def remove_post(post_id):
    """Removes a post and returns the updated list."""
    posts = get_posts_data()
    updated_posts = [p for p in posts if p["id"] != post_id]
    posts.clear()
    posts.extend(updated_posts)  # Updates in place to keep reference
    return updated_posts

def update_existing_post(post_id, new_data):
    """Updates an existing post by merging with new data."""
    post = find_post_by_id(post_id)
    if post:
        post.update(new_data)
    return post

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Get all posts with optional sorting by title or content."""
    sort_field = request.args.get('sort', '').lower()
    sort_direction = request.args.get('direction', '').lower()

    valid_sort_fields = ['title', 'content']
    valid_directions = ['asc', 'desc']

    if sort_field and sort_field not in valid_sort_fields:
        return jsonify({"error": "Invalid sort field. Use 'title' or 'content'."}), 400

    if sort_direction and sort_direction not in valid_directions:
        return jsonify({"error": "Invalid sort direction. Use 'asc' or 'desc'."}), 400

    posts = get_posts_data()
    sorted_posts = sorted(posts, key=lambda post: post.get(sort_field, ""), reverse=(sort_direction == 'desc')) if sort_field else posts

    return jsonify(sorted_posts), 200

@app.route('/api/posts', methods=['POST'])
def add_post():
    """Add a new post with title and content."""
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Title and content are required."}), 400

    new_post = add_new_post(data["title"], data["content"])
    return jsonify(new_post), 201

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post by ID."""
    post = find_post_by_id(post_id)

    if not post:
        return jsonify({"error": f"Post with ID {post_id} not found."}), 404

    remove_post(post_id)
    return jsonify({"message": f"Post {post_id} deleted."}), 200

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update a post by ID."""
    data = request.get_json()
    post = update_existing_post(post_id, data)

    if not post:
        return jsonify({"error": f"Post with ID {post_id} not found."}), 404

    return jsonify(post), 200

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Search posts by title or content."""
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    filtered_posts = [
        post for post in get_posts_data()
        if (title_query in post["title"].lower() if title_query else True) and
           (content_query in post["content"].lower() if content_query else True)
    ]

    return jsonify(filtered_posts), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
