Docker-compose: move to project folder in your bash-terminal of Docker and run command:<br>
docker-compose up<br>
<br>
Use http://192.168.99.100:8000/ to get to the project site<br>
<br>
To provide coordinates, you need to set your latitude and langitude in API endpoints<br>
As example: /api/v1/users/?lat=53.898262&lng=27.522101<br><br>
<br>
API endpoints:<br>
<br>
For getting access to authorized only/author only use Postman/frontend client providing authorization bearer token<br>
<br>
/api/v1/signup - Registration(via Postman/frontend client providing "name" "email" "password" in body)<br>
<br>
/api//token/ - Obtaining token for authorization(via Postman/frontend client providing "email" "password" in body)<br>
<br>
/api/v1/users/?lat=your_latitude&lng=your_langetude - User List for all (only first 25 users with 10 km distance from you)<br>
<br>
/api/v1/users/view_account/id/?lat=your_latitude&lng=your_longitude - User retrive for authorized only<br>
<br>
/api/v1/users/update_account/id - Update and retrieve user's account by its owner only<br>
<br>
/api/v1/chats/chat/ - List chats for its owners only from both sides<br>
<br>
/api/v1/posts/messages/ - List messages for authenticated only<br>
<br>
/api/v1/posts/messages/update_message/id - Retrieve and update message by its owner<br>

