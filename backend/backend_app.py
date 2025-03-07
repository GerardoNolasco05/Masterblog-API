from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Hardcoded list of posts (simulating a database)
POSTS = [
    {"id": 1, "title": "First Post", "content": "This is the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the second post."},
]


# Route to list all blog posts
@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


# Route to add a new blog post
@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    # Validate input
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Missing title or content."}), 400

    # Generate a new unique ID
    new_id = max(post["id"] for post in POSTS) + 1 if POSTS else 1

    # Create the new post
    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }

    # Add to the list (simulating a database insert)
    POSTS.append(new_post)

    return jsonify(new_post), 201  # Return the new post with a 201 Created status


# Route to delete a blog post by ID
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS
    post = next((p for p in POSTS if p["id"] == post_id), None)

    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    # Remove the post from the list
    POSTS = [p for p in POSTS if p["id"] != post_id]

    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


# Route to update a blog post by ID
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()

    # Find the post by ID
    post = next((p for p in POSTS if p["id"] == post_id), None)

    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    # Update only if fields are provided
    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])

    return jsonify(post), 200  # Return the updated post with a 200 OK status


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

