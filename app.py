from flask import Flask, render_template, request
from data import directory_items
from blog_data import blog_posts
from about_data import about_content
from favorites_data import favorite_item_ids

app = Flask(__name__)

@app.route('/')
def index():
    search_query = request.args.get('search')
    category_filter = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    items_per_page = 6 # As seen in the image "Showing 6 of 864 results"

    filtered_items = directory_items

    # Apply search filter
    if search_query:
        filtered_items = [item for item in filtered_items if search_query.lower() in item['name'].lower() or search_query.lower() in item['description'].lower()]

    # Apply category filter
    if category_filter and category_filter != 'All':
        filtered_items = [item for item in filtered_items if item['category'] == category_filter]

    # Implement pagination
    total_items = len(filtered_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    paginated_items = filtered_items[start_index:end_index]

    # Pass paginated items and pagination info to the index template
    return render_template('index.html', items=paginated_items, search_query=search_query, category_filter=category_filter, page=page, total_pages=total_pages, total_items=total_items)

# Add routes for other functionalities later
@app.route('/directory')
def directory():
    # Placeholder for directory listing functionality
    return render_template('directory.html')

@app.route('/blog')
def blog():
    # Pass blog posts to the blog template
    return render_template('blog.html', posts=blog_posts)

@app.route('/blog/<int:post_id>')
def blog_detail(post_id):
    # Find the blog post with the matching ID
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post:
        return render_template('blog_detail.html', post=post)
    else:
        # Handle post not found, maybe render a 404 page
        return "Blog post not found", 404


@app.route('/contact')
def contact():
    # Placeholder for contact page
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    # Placeholder for privacy policy page
    return render_template('privacy.html')

@app.route('/about')
def about():
    # Pass about content to the about template
    return render_template('about.html', about_content=about_content)

@app.route('/favorites')
def favorites():
    # Get favorite items based on IDs
    favorite_items = [item for item in directory_items if item['id'] in favorite_item_ids]
    # Pass favorite items to the favorites template
    return render_template('favorites.html', favorite_items=favorite_items)

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    # Find the item with the matching ID
    item = next((item for item in directory_items if item['id'] == item_id), None)
    if item:
        return render_template('item_detail.html', item=item)
    else:
        # Handle item not found, maybe render a 404 page
        return "Item not found", 404


if __name__ == '__main__':
    app.run(debug=True)