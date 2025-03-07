from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Hardcoded list of posts (simulating a database)
POSTS = [
    {"id": 1, "title": "First", "content": "This is the first post."},
    {"id": 2, "title": "Second", "content": "This is the second post."},
    {"id": 3, "title": "Third", "content": "This is the third post."}
]

# Route to list all blog posts with optional sorting
@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_field = request.args.get('sort', '').lower()  # Get sort field (optional)
    sort_direction = request.args.get('direction', '').lower()  # Get sort direction (optional)

    valid_sort_fields = ['title', 'content']
    valid_directions = ['asc', 'desc']

    # Validate sort field
    if sort_field and sort_field not in valid_sort_fields:
        return jsonify({"error": "Invalid sort field. Use 'title' or 'content'."}), 400

    # Validate sort direction
    if sort_direction and sort_direction not in valid_directions:
        return jsonify({"error": "Invalid sort direction. Use 'asc' or 'desc'."}), 400

    sorted_posts = POSTS[:]  # Copy list to avoid modifying original

    # Apply sorting if parameters are provided
    if sort_field:
        reverse = sort_direction == 'desc'
        sorted_posts = sorted(sorted_posts, key=lambda post: post[sort_field], reverse=reverse)

    return jsonify(sorted_posts), 200  # Return sorted list

# Route to add a new blog post
@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Missing title or content."}), 400

    new_id = max(post["id"] for post in POSTS) + 1 if POSTS else 1
    new_post = {"id": new_id, "title": data["title"], "content": data["content"]}
    POSTS.append(new_post)

    return jsonify(new_post), 201

# Route to delete a blog post by ID
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS
    post = next((p for p in POSTS if p["id"] == post_id), None)

    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    POSTS = [p for p in POSTS if p["id"] != post_id]

    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

# Route to update a blog post by ID
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    post = next((p for p in POSTS if p["id"] == post_id), None)

    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])

    return jsonify(post), 200

# Route to search for blog posts by title or content
@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    # Filter posts based on title and/or content
    filtered_posts = [
        post for post in POSTS
        if (title_query in post["title"].lower() if title_query else True) and
           (content_query in post["content"].lower() if content_query else True)
    ]

    return jsonify(filtered_posts), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)



