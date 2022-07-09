### What is that?
wasd_notifier is a bot for VKontakte based on [vkbottle](https://github.com/vkbottle/vkbottle) that provides stream notifications for streaming service [wasd.tv](https://wasd.tv). 

### Features:
 - Receive a notification when streamer from your subscription list starts the stream
 
![](https://cdn.discordapp.com/attachments/713748391196098612/995299732203241492/unknown.png)
 - Subscribe to channel by typing the channel name (it checks if the channel exists)
 
![](https://cdn.discordapp.com/attachments/713748391196098612/995299584614080522/unknown.png)

![](https://cdn.discordapp.com/attachments/713748391196098612/995300401643536394/unknown.png)
- Disable/enable all notifications command

![](https://cdn.discordapp.com/attachments/713748391196098612/995299848876204102/unknown.png)
- Unsubscribe channels

![](https://cdn.discordapp.com/attachments/713748391196098612/995299919621521488/unknown.png)
- View your subscriptions

![](https://cdn.discordapp.com/attachments/713748391196098612/995299955956789248/unknown.png)

### Development / Usage:
 1. Clone the repo:
```
git clone https://github.com/descensiontohell/wasd_notifier.git && cd wasd_notifier
```
2. Create sample VK group on https://vk.com/groups then head to Manage:
	- Enable Long Poll API
	- Allow community messages
	- Enable bot abilities
	- Obtain API access token 
3. Set according variables in `.env` file:
```
TOKEN=
  
POSTGRES_USER= 
POSTGRES_PASSWORD=
```
4. Run the containers:
```
docker-compose up
```
5. Head to Group -> Write message
5. Rebuild the app after changes:
```
docker-compose down && docker-compose up --build
```
