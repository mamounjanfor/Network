#Python, JavaScript, HTML, and CSS


New Post Feature:
Implemented the ability for signed-in users to create a new text-based post.
Users can fill in a text area and submit the post using a dedicated button.
The "New Post" feature can either be part of the "All Posts" page or on a separate page, as shown in the provided screenshot.


All Posts Page:
Created a navigation link that leads users to a page displaying all posts from all users.
Posts are shown with the most recent ones first, including the poster's username, post content, post date and time, and the number of likes (initially set to 0).


Profile Page:
Developing profile pages accessible by clicking on a username.
The profile page shows the user's follower count, the number of people they follow, and all of their posts in reverse chronological order.
Added functionality for signed-in users to follow or unfollow other users, except themselves.


Following Feature:
Introduced a "Following" link in the navigation bar that takes signed-in users to a page displaying posts from users they follow.
This page mimics the "All Posts" page but only shows posts from followed users.


Pagination:
Implemented pagination on pages displaying posts, limiting the view to 10 posts per page.
Added "Next" and "Previous" buttons to navigate between pages of posts.


Edit Post Functionality:
Allowed users to edit their posts by clicking an "Edit" button or link.
Editing replaces the post content with a textarea for editing, with changes savable without reloading the page.
Ensured security measures to prevent users from editing other people's posts.


Like and Unlike System:
Users can like or unlike a post through a button or link.
Utilized JavaScript to asynchronously update the server about the like status and then update the like count displayed on the page without a page reload.
