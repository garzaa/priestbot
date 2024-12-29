# priestbot

priestbot is a Catholic-coded confession bot. he has various features:

1. Confession: DM him and he will anonymously repost your confession to the server. He will also assign you a penance.
2. Budget Nitro Reacts: Tag him in response to a message (or don't, if you want it on your own message) with a trigger word and he'll react with that animated emoji. Add "with delete" to have your original message removed afterwards to reduce bot command spam.

If there's anyone else out there who wants to run their own Priestbot:
- make sure imagemagick is available on the command line as magick.exe
- `pip install -r requirements.txt`
- put your bot's OAuth token as `TOKEN` in a `.env` file next to `priestbot.py`
- change the confession channel ID to the ID of your own channel
- substitute the animated emojis with your server's
- write your own damn penances
